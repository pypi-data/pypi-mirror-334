from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mutationtracker.caller import Caller


class Mutation:
    def __init__(
        self,
        mutated_object: any,
        attribute_name: str,
        attribute_value: any,
        caller: "Caller",
    ):
        self.attribute_name: str = attribute_name
        self.old_value: any = deepcopy(
            getattr(mutated_object, attribute_name, "AttributeDoesNotExist")
        )
        self.new_value: any = deepcopy(attribute_value)
        self.caller = caller
        self.timestamp: datetime = datetime.now()
        self._mutated_object = mutated_object

    def log(self, log_callable) -> None:
        try:
            object_repr = f"({self._mutated_object})"
        except AttributeError:
            object_repr = "(repr unavailable)"
        message = (
            f"Change in {self._mutated_object.__class__.__name__} instance {object_repr} "
            f"attribute {self.attribute_name}: to {self.new_value} "
            f"from {self.old_value} (by {self.caller.name})"
        )
        log_callable(message)

    def __repr__(self):
        return (
            f"Set {self.attribute_name} to {self.new_value} from {self.old_value} "
            f"by {self.caller.name} at {self.timestamp}"
        )
