import inspect
import traceback

from mutationtracker.metaclass.access import Access
from mutationtracker.ledger import MutationLedger
from mutationtracker.utils import do_nothing


def track_mutations(log_function: callable = do_nothing):
    """
    Classes decorated by track_mutations will have their mutations automatically logged in property MUTATIONS which
    might ease the pain of debugging an object's mutations throughout a large codebase. The MUTATIONS attribute holds
    mutation history in several ways: by attribute, by caller (both with and without line no.) and by datetime. It also
    explicitly keeps track of where an object was initially created, where it was lastly mutated and where it was
    'filled' as attribute to another class (if applicable).

    Additionally, the user might use the option to log a message everytime any child instance gets mutated by using the
    keyword argument `log_function`. It takes any callable, but most likely will be print, logger.debug or logger.info.
    By default, no message is printed to the console or any log output destination.

    Please note that if a mutable value is assigned to an attribute, it is deepcopied into the MUTATIONS attribute,
    but might be further manipulated in the original referenced object. Therefore, in some cases, the mutation tracking
    could be missing some mutations as mutable values might bypass the __setattr__ method upon which the tracker is
    built. The MUTATIONS attribute will always keep the value as it was at the time __setattr__ was called.

    The full mutation history can be logged at once by calling `your_class_instance.log_all_mutations()`.

    :param log_function: Optional callable for logging purposes. If not provided, logging will be disabled.
    """

    def decorator(decorated_class):
        class MutationTrackedObject(decorated_class, metaclass=Access):
            """
            Slightly altered version of the stand-alone MutationTrackedObject to work as part of `track_mutations`
            decorator
            """

            @Access.final
            def log_all_mutations(self):
                self._MUTATIONS.log_all()

            @property
            @Access.final
            def MUTATIONS(self):
                return self._MUTATIONS

            @Access.final
            def __new__(cls, *init_args: any, **init_kwargs: dict[str, any]):
                #  create instance and add mutations instance to private attribute
                instance = super().__new__(cls)
                instance.__class__.__name__ = decorated_class.__name__
                instance._MUTATIONS = MutationLedger(
                    instance,
                    init_args,
                    init_kwargs,
                    log_function=log_function,
                )
                #  get creator caller info
                frame = inspect.currentframe().f_back
                caller_name = frame.f_code.co_name
                caller_module = getattr(
                    inspect.getmodule(frame), "__name__", "ModuleNotFound"
                )
                caller_class = (
                    frame.f_code.co_qualname.split(".")[0]
                    if "." in frame.f_code.co_qualname
                    and "<locals>" not in frame.f_code.co_qualname
                    else None
                )
                caller_line_number = frame.f_lineno
                full_trace = traceback.format_stack()[:-1]
                #  set creator in MUTATIONS
                instance._MUTATIONS.set_creator(
                    caller_module,
                    caller_class,
                    caller_name,
                    caller_line_number,
                    full_trace,
                )
                return instance

            @Access.final
            def __setattr__(self, attribute_name: str, attribute_value: any):
                #  get caller info
                frame = inspect.currentframe().f_back
                caller_name = frame.f_code.co_name
                caller_module = getattr(
                    inspect.getmodule(frame), "__name__", "ModuleNotFound"
                )
                caller_class = (
                    frame.f_code.co_qualname.split(".")[0]
                    if "." in frame.f_code.co_qualname
                    and "<locals>" not in frame.f_code.co_qualname
                    else None
                )
                caller_line_number = frame.f_lineno
                full_trace = traceback.format_stack()[:-1]
                #  change private Mutations object and call log function
                if hasattr(self, "_MUTATIONS"):
                    self._MUTATIONS.add(
                        attribute_name,
                        attribute_value,
                        caller_module,
                        caller_class,
                        caller_name,
                        caller_line_number,
                        full_trace,
                    )
                #  set actual attribute value
                super().__setattr__(attribute_name, attribute_value)

        return MutationTrackedObject

    return decorator
