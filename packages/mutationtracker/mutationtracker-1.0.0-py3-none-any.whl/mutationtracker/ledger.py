from collections import OrderedDict

from mutationtracker.utils import do_nothing, is_private_name, is_ignored_caller_module
from mutationtracker.mutation import Mutation
from mutationtracker.caller import Caller


class MutationLedger:
    """
    MutationLedger objects hold data about mutations to an object, and groups it by attribute, by caller and by
    datetime. It also keeps track of the original creator of an instance, the last caller to have changed it and the
    last caller that filled it as attribute value to another object containing the MutationLedger class.

    Additionally, the mutation might optionally be logged (e.g. printed to console) if the user sets a log function.
    By default, no messages are printed.
    """

    def __init__(
        self,
        mutated_object: any,
        init_args: tuple[any],
        init_kwargs: dict[str, any],
        log_function: callable = do_nothing,
    ):
        self.created_by: str | None = None
        self.last_mutation_by: str | None = None
        self.filled_by: str | None = None
        self.all_mutations: list[Mutation] = []
        self.grouped_by_caller: OrderedDict[str, list[Mutation]] = OrderedDict()
        self.grouped_by_caller_without_line_number: OrderedDict[str, list[Mutation]] = (
            OrderedDict()
        )
        self._log_function: callable = log_function
        self._mutated_object: any = mutated_object
        self._init_args: tuple[any] = init_args
        self._init_kwargs: dict[str, any] = init_kwargs

    def add(
        self,
        attribute_name: str,
        attribute_value: any,
        caller_module: str,
        caller_class: str | None,
        caller_function: str,
        line_number: int,
        full_trace: list[str],
    ) -> None:
        if is_private_name(attribute_name) or is_ignored_caller_module(caller_module):
            return
        caller = self._create_caller(
            caller_module,
            caller_class,
            caller_function,
            line_number,
            full_trace,
        )
        mutation = self._create_mutation(
            attribute_name,
            attribute_value,
            caller,
        )
        self._set_filler(caller, attribute_value)
        self._set_last_mutation(caller)
        self._add_mutation(mutation)
        mutation.log(self._log_function)

    def set_creator(
        self,
        caller_module: str,
        caller_class: str | None,
        caller_function: str,
        line_number: int,
        full_trace: list[str],
    ) -> None:
        caller = self._create_caller(
            caller_module,
            caller_class,
            caller_function,
            line_number,
            full_trace,
        )
        if self.created_by is None and not is_ignored_caller_module(caller.module_name):
            self.created_by = caller
            self._log_creation()

    def set_logger(self, log_function: callable) -> None:
        self._log_function = log_function

    def set_filler(self, caller: Caller) -> None:
        self.filled_by = caller

    def count_mutations(self) -> int:
        return len(self.all_mutations)

    def log_all(self) -> None:
        self._log_function(
            f"{5 * '='} All mutations for {self._mutated_object.__class__.__name__} "
            f"instance {self._mutated_object} {5 * '='}"
        )
        self._log_function(f"Created by: {self.created_by}")
        self._log_function(f"Last mutation by: {self.last_mutation_by}")
        self._log_function(f"Filled by: {self.filled_by}")
        self._log_function(f"Number of attribute mutations: {self.count_mutations()}")
        for mutation in self.all_mutations:
            mutation.log(self._log_function)

    @property
    def grouped_by_attribute(self):
        return self._group_by("attribute_name")

    @property
    def grouped_by_timestamp(self):
        return self._group_by("timestamp")

    def _add_mutation(self, mutation: Mutation):
        self.all_mutations.append(mutation)
        self._add_mutation_by_caller(mutation)

    def _add_mutation_by_caller(self, mutation: Mutation) -> None:
        """
        This grouped attribute is not property like the others because somehow Pycharm debugger occasionally
        fails to resolve the variable and throws UnableToResolveVariableException in debugger, which is inconvenient
        to the user. Might be changed to property when this bug gets resolved.
        """
        self.grouped_by_caller[mutation.caller.name] = self.grouped_by_caller.get(
            mutation.caller.name, []
        )[:] + [mutation]
        self.grouped_by_caller_without_line_number[
            mutation.caller.name_without_line_number
        ] = self.grouped_by_caller_without_line_number.get(
            mutation.caller.name_without_line_number, []
        )[
            :
        ] + [
            mutation
        ]

    def _set_last_mutation(self, caller: Caller) -> None:
        self.last_mutation_by = caller

    def _log_creation(self):
        self._log_function(
            f"A new {self._mutated_object.__class__.__name__} instance is being created "
            f"by {self.created_by}: args={self._init_args}, kwargs={self._init_kwargs}"
        )

    @staticmethod
    def _set_filler(caller: Caller, attribute_value: any) -> None:
        if hasattr(attribute_value, "MUTATIONS") and isinstance(
            attribute_value.MUTATIONS, MutationLedger
        ):
            attribute_value.MUTATIONS.set_filler(caller)

    @staticmethod
    def _create_caller(
        caller_module: str,
        caller_class: str | None,
        caller_function: str,
        line_number: int,
        full_trace: list[str],
    ) -> Caller:
        return Caller(
            caller_module, caller_class, caller_function, line_number, full_trace
        )

    def _create_mutation(
        self, attribute_name: str, attribute_value: any, caller: Caller
    ):
        mutation = Mutation(
            self._mutated_object, attribute_name, attribute_value, caller
        )
        return mutation

    def _group_by(self, attribute_name: str, nested_attribute_name: str | None = None):
        grouped_dict = OrderedDict()
        for mutation in self.all_mutations:
            attribute_value = getattr(mutation, attribute_name)
            if nested_attribute_name:
                attribute_value = getattr(attribute_value, nested_attribute_name)
            if attribute_value in grouped_dict:
                grouped_dict[attribute_value].append(mutation)
            else:
                grouped_dict[attribute_value] = [mutation]
        return grouped_dict

    def __repr__(self):
        return (
            f"All {self.count_mutations()} mutations in object created by {self.created_by} "
            f"(last by {self.last_mutation_by})"
        )
