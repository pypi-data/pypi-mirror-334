from abc import ABC
from enum import Enum
from typing import Union
from uuid import uuid4

class ClassType(Enum):
    BOX = "box"
    RBOX = "rbox"
    POLYLINE = "polyline"
    POLYGON = "polygon"
    KEYPOINT = "keypoint"
    CUBOID2D = "cuboid2d"
    CUBOID = "cuboid"

    @staticmethod
    def is_valid_class_type(class_type: Union[str, 'ClassType']):
        if isinstance(class_type, ClassType):
            return True
        elif isinstance(class_type, str):
            return class_type in [member.value for member in ClassType]
        else:
            return False


class Label(ABC):
    def __init__(self, attributes):
        self.id = attributes.get("id", str(uuid4()))

        class_name = attributes.get("class_name", None)
        class_id = attributes.get("class_id", None)

        if class_name is not None and class_id is not None:
            self.class_name = class_name
            self.class_id = class_id

        self.properties_def = attributes.get("properties_def", [])
        self.properties = attributes.get("properties", [])
        self.tracking_id = attributes.get("tracking_id", None)
        self.annotation_type = None

    def to_dict(self):
        pass
