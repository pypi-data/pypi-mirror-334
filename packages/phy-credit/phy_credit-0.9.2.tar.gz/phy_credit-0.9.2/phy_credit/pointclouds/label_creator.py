from abc import ABC
from typing import Optional
from uuid import uuid4

from ..common.label_creator import LabelCreator
from ..common.utils import set_properties, unique_string_builder, is_sublist
from .label import Cuboid
from ..common.label import ClassType


class CuboidCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)
        self.label = Cuboid()

    def get_default_cuboid_coord(self):
        return {
            "position": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "rotation_quaternion": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "size": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            }
        }

    def create(
        self,
        class_name: str,
        frames: list,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: Optional[int] = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID,
        ) in self.object_classes_map.keys()
        coord = frames[0]["annotation"]["coord"]
        assert is_sublist(
            ["position", "rotation_quaternion", "size"],
            coord.keys(),
        )
        return Cuboid(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["id"],
            frames=frames,
            meta=meta if meta else self.get_meta(
                class_name, ClassType.CUBOID),
            properties_def=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )
    
    def from_dict(self, cuboid):
        class_name = cuboid["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID,
        ) in self.object_classes_map.keys()
        frames = cuboid["frames"]

        return Cuboid(
            id=cuboid["id"] if "id" in cuboid else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["id"],
            frames=frames,
            properties_def=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["properties"],
            properties=cuboid["properties"] if "properties" in cuboid else [],
            tracking_id=cuboid["tracking_id"] if "tracking_id" in cuboid else 0,
        )

    def set_class(self, class_name):
        class_id = self.object_classes_map[
            unique_string_builder(
                class_name,
                ClassType.CUBOID,
            )
        ].get("id")

        if class_id is None:
            raise ValueError(f"Class name {class_name} not found in object classes map")
        
        self.label.class_name = class_name
        self.label.class_id = class_id

    def set_tracking_id(self, tracking_id):
        self.label.tracking_id = tracking_id
    # if frame information exists, update the frame information
    # else, add the frame information
    def set_annotation(self, frame_num, position=None, rotation_quaternion=None, size=None, frame_properties=None):
        target_frame = None
        for frame_info in self.label.frames:
            if frame_info["num"] == frame_num:
                target_frame = frame_info
                break
        
        if target_frame is None: 
            target_frame = {
                "num": frame_num,
                "annotation": {
                    "coord": self.get_default_cuboid_coord()
                },
                "properties": []
            }
            self.label.frames.append(target_frame)


        if position is not None:
            target_frame["annotation"]["coord"]["position"] = position
        if rotation_quaternion is not None:
            target_frame["annotation"]["coord"]["rotation_quaternion"] = rotation_quaternion
        if size is not None:
            target_frame["annotation"]["coord"]["size"] = size
        if frame_properties is not None:
            target_frame["properties"] = frame_properties

    def set_properties(self, properties, frame_num=None):
        if frame_num is None:
            self.label.properties = properties
        else:
            if self.label.frames.get(frame_num) is None:
                raise ValueError(f"Frame number {frame_num} not found in cuboid")
            else:
                self.label.frames[frame_num]["properties"] = properties

class PointcloudsAnnotationBuilder(ABC):
    def __init__(self, object_classes_map):
        self.object_classes_map = object_classes_map
    
    def get_cuboid_creator(self):
        return CuboidCreator(self.object_classes_map)

    def from_dict(self, label):
        creators = [
            CuboidCreator(self.object_classes_map),
        ]
        for creator in creators:
            try:
                return creator.from_dict(label)
            except:
                continue
        return None

