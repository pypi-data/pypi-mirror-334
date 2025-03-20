class Caller:
    def __init__(
        self,
        module_name: str,
        class_name: str | None,
        function_name: str,
        line_number: int,
        stack: list[str],
    ):
        self.module_name: str = module_name
        self.class_name: str | None = class_name
        self.function_name: str = function_name
        self.line_number: int = line_number
        self.stack: list[str] = stack

    @property
    def name(self):
        return self._get_name(
            self.module_name, self.class_name, self.function_name, self.line_number
        )

    @property
    def name_without_line_number(self):
        return self.name.split(":")[0]

    @property
    def stack_string(self):
        return "".join(self.stack)

    @staticmethod
    def _get_name(
        module_name: str,
        class_name: str | None,
        function_name: str,
        line_number: int,
    ) -> str:
        if class_name:
            return f"{module_name}.{class_name}.{function_name}:{line_number}"
        return f"{module_name}.{function_name}:{line_number}"

    def __repr__(self):
        return f"{self.name}"
