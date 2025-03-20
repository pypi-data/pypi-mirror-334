class Access(type):
    """
    Metaclass Access intends to prevent children of a specific class to override certain methods used by the base class.
    """

    __SENTINEL = object()

    def __new__(mcs, name, bases, class_dict):
        private: set = {
            key
            for base in bases
            for key, value in vars(base).items()
            if callable(value) and mcs.__is_final(value)
        }
        if any(key in private for key in class_dict):
            raise RuntimeError("Certain methods may not be overridden!")
        return super().__new__(mcs, name, bases, class_dict)

    @classmethod
    def __is_final(mcs, method):
        try:
            return method.__final is mcs.__SENTINEL
        except AttributeError:
            return False

    @classmethod
    def final(mcs, method):
        method.__final = mcs.__SENTINEL
        return method
