from abc import ABC, abstractmethod
from .utils import unique_string_builder, get_name_from_unique_string


class LabelCreator(ABC):
    def __init__(self, object_classes_map):
        self.object_classes_map = object_classes_map
        self.label = None

    @abstractmethod
    def create(self):
        pass
    @abstractmethod
    def from_dict(self):
        pass

    def get_meta(self, class_name, class_type):
        return {
            "z_index": 1,
            "visible": True,
            "alpha": 1,
            "color": self.object_classes_map[unique_string_builder(
                class_name, class_type
            )]["color"],
        }
    
    def get_class_names(self):
        return [get_name_from_unique_string(x) for x in list(self.object_classes_map.keys())]
    
    def build(self):                
        if self.label is None:
            raise NotImplementedError("Label is not defined")

        if self.label.class_name is None:
            raise ValueError("class_name is not defined")

        if self.label.tracking_id is None:
            raise ValueError("tracking_id is not defined")

        return self.label.to_dict()
