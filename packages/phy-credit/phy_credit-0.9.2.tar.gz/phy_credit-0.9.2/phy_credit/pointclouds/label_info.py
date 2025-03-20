from uuid import uuid4

from .. import __version__
from ..common.video_utils import (
    calculate_annotated_frame_count,
    calculate_video_properties_count,
)
from ..common.utils import unique_string_builder
from .label_creator import PointcloudsAnnotationBuilder, CuboidCreator
from ..exceptions import InvalidObjectException

class LabelInfo:
    @classmethod
    def _get_opt_map(cls, options):
        res = {}
        for opt in options:
            if "children" in opt:
                res.update(LabelInfo._get_opt_map(opt["children"]))
            else:
                res[opt["name"]] = opt
        return res

    @classmethod
    def _set_properties(cls, properties_def, properties):
        prop_def_map = {
            prop_def["name"]: prop_def for prop_def in properties_def
        }
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop["name"]]
            if prop_def["type"] in ["radio", "dropdown", "checkbox"]:
                opt_map = LabelInfo._get_opt_map(prop_def["options"])
                if prop_def["type"] == "checkbox":
                    converted_properties.append(
                        {
                            "type": prop_def["type"],
                            "property_id": prop_def["id"],
                            "property_name": prop_def["name"],
                            "option_ids": [
                                opt_map[val]["id"] for val in prop["value"]
                            ],
                            "option_names": [
                                opt_map[val]["name"] for val in prop["value"]
                            ],
                        }
                    )
                else:
                    converted_properties.append(
                        {
                            "type": prop_def["type"],
                            "property_id": prop_def["id"],
                            "property_name": prop_def["name"],
                            "option_id": opt_map[prop["value"]]["id"],
                            "option_name": opt_map[prop["value"]]["name"],
                        }
                    )
            elif prop_def["type"] == "free response":
                converted_properties.append(
                    {
                        "type": prop_def["type"],
                        "property_id": prop_def["id"],
                        "property_name": prop_def["name"],
                        "value": prop["value"],
                    }
                )
        return converted_properties

    @classmethod
    def _get_properties(cls, properties_def, properties):
        prop_def_map = {
            prop_def["name"]: prop_def for prop_def in properties_def
        }
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop["property_name"]]
            if prop_def["type"] in ["radio", "dropdown"]:
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["option_name"],
                    }
                )
            elif prop_def["type"] == "checkbox":
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["option_names"],
                    }
                )
            elif prop_def["type"] == "free response":
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["value"],
                    }
                )
        return converted_properties

    def __init__(self, label_interface, result=None):
        self.label_interface = label_interface
        self.object_classes_map = {
            unique_string_builder(
                object_class["name"],
                object_class["annotation_type"]
            ): object_class for object_class in label_interface.object_tracking.object_classes
        }
        if result is None:
            self.result = {}
            self.init_objects()
            self.init_categories()
        else:
            self.result = result

    def init_objects(self):
        self.result["objects"] = []

    def init_categories(self):
        self.result["categories"] = {"frames": [], "properties": []}

    def get_next_tracking_id(self):
        next_tracking_id = 0
        for obj in self.result["objects"]:
            if obj["tracking_id"] > next_tracking_id:
                next_tracking_id = obj["tracking_id"]
        next_tracking_id += 1

        return next_tracking_id

    def _get_property_info(self, properties_def, property_name):
        for prop_def in properties_def:
            if prop_def["name"] == property_name:
                return prop_def
        return None

    def _get_option_id(self, property_info, option_name):
        for opt in property_info["options"]:
            if opt["name"] == option_name:
                return opt["id"]
        return None

    # for example, if you want to add "Motion" property with "Walking" option,
    # you may give input property_dict as { "Motion": "Walking" } (radio type), { "Is carrying": ["Child", "Baggage"]} (checkbox type)
    def build_properties(self, class_name, annotation_type, property_dict, is_per_frame=False):
        result_properties = []

        unique_class_string = unique_string_builder(
            class_name,
            annotation_type
        )

        for property_name, option_value in property_dict.items():
            if option_value is None:
                continue
            
            property_info = self._get_property_info(
                self.object_classes_map[unique_class_string]["properties"],
                property_name
            )

            if property_info is None:
                continue
            if is_per_frame and not property_info["per_frame"]:
                continue
            if not is_per_frame and property_info["per_frame"]:
                continue

            if property_info["type"] in ["radio", "dropdown"]:
                option_id = self._get_option_id(
                    property_info,
                    option_value
                )
                if option_id is None:
                    continue
                
                result_properties.append({
                    "type": property_info["type"],
                    "property_id": property_info["id"],
                    "property_name": property_name,
                    "option_id": option_id,
                    "option_name": option_value
                })
            elif property_info["type"] == "checkbox":
                if not isinstance(option_value, list):
                    continue
                valid_option_names = []
                valid_option_ids = []
                for option_name in option_value:
                    option_id = self._get_option_id(
                        property_info,
                        option_name
                    )
                    if option_id is not None:
                        valid_option_names.append(option_name)
                        valid_option_ids.append(option_id)
                
                if len(valid_option_ids) == 0:
                    continue
                
                result_properties.append({
                    "type": property_info["type"],
                    "property_id": property_info["id"],
                    "property_name": property_name,
                    "option_id": valid_option_ids,
                    "option_name": valid_option_names
                })

            elif property_info["type"] == "free response":
                if not isinstance(option_value, str):
                    continue
                result_properties.append({
                    "type": property_info["type"],
                    "property_id": property_info["id"],
                    "property_name": property_name,
                    "value": option_value
                })
            else:
                continue

        return result_properties        

    def add_object(self, label):
        self.result["objects"].append(label)

    def remove_object(self, object_id):
        self.result["objects"] = [
            obj for obj in self.result["objects"] if obj["id"] != object_id
        ]

    def get_object_by_id(self, object_id):
        for obj in self.result["objects"]:
            if obj["id"] == object_id:
                return obj
        return None        

    def get_objects(self):
        ocm = self.object_classes_map
        try:
            if "objects" not in self.result:
                return []
            if not isinstance(self.result["objects"], list):
                return []
            return self.result["objects"]
        except Exception as e:
            return []

    def set_simple_categories(self, frames=None, properties=None):
        self.result["categories"] = {
            "frames": [
                {
                    "num": frame["num"],
                    "properties": LabelInfo._set_properties(
                        self.label_interface.categorization.properties,
                        frame["properties"],
                    ),
                }
                for frame in (frames if frames is not None else [])
            ],
            "properties": LabelInfo._set_properties(
                self.label_interface.categorization.properties,
                properties if properties is not None else [],
            ),
        }

    def get_simple_categories(self):
        try:
            simple_categories = {
                "frames": [
                    {
                        "num": frame["num"],
                        "properties": LabelInfo._get_properties(
                            self.label_interface.categorization.properties,
                            frame["properties"],
                        ),
                    }
                    for frame in self.result["categories"]["frames"]
                ],
                "properties": LabelInfo._get_properties(
                    self.label_interface.categorization.properties,
                    self.result["categories"]["properties"],
                ),
            }
            return simple_categories
        except:
            return {
                "frames": [],
                "properties": [],
            }

    def build_tags(self):
        classes_count = {}
        anno_count = {}
        classes_name = {}
        for obj in self.result["objects"]:
            cid = obj["class_id"]
            classes_count[cid] = classes_count.get(cid, 0) + 1
            anno_count[cid] = anno_count.get(cid, 0) + len(obj["frames"])
            classes_name[cid] = obj["class_name"]
        class_val = list(classes_name.values())

        categories_id = []
        if (
            "categories" in self.result
            and "properties" in self.result["categories"]
        ):
            properties_list = [self.result["categories"]["properties"]] + [
                frame["properties"]
                for frame in self.result["categories"]["frames"]
            ]
            for properties in properties_list:
                for prop in properties:
                    if "option_id" in prop:
                        categories_id.append(prop["option_id"])
                    elif "option_ids" in prop:
                        for o_id in prop["option_ids"]:
                            categories_id.append(o_id)
            class_val.extend(categories_id)

        return {
            "classes_id": list(classes_count.keys()),
            "class": class_val,
            "classes_count": [
                {
                    "id": k,
                    "name": classes_name[k],
                    "count": v,
                }
                for k, v in classes_count.items()
            ],
            "classes_properties_count": calculate_video_properties_count(
                self.result["objects"]
            ),
            "classes_annotation_count": [
                {
                    "id": k,
                    "name": classes_name[k],
                    "count": v,
                }
                for k, v in anno_count.items()
            ],
            "categories_id": categories_id,
            "annotated_frame_count": calculate_annotated_frame_count(
                self.result["objects"]
            ),
        }

    def build_info(self):
        ocm = self.object_classes_map
        return {
            "version": __version__,
            "meta": {
                "image_info": {},
                "edit_info": {
                    "objects": [
                        {
                            "id": obj["id"],
                            "color": ocm[unique_string_builder(
                                obj["class_name"],
                                obj["annotation_type"]
                            )]["color"],
                            "visible": True,
                            "selected": False,
                            "tracking_id": obj["tracking_id"],
                        }
                        for obj in self.result["objects"]
                    ]
                },
            },
            "result": self.result,
            "tags": self.build_tags(),
        }
    
    def get_cuboid_creator(self):
        return CuboidCreator(self.object_classes_map)

