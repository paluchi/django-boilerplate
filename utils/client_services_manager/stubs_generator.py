import ast
import glob
import inspect
import json
import os
from typing import Any, Dict, List, Tuple, Callable


class StubsGenerator:  # noqa: WPS214
    """Build stubs for the dynamic generated methods."""

    def __init__(self, methods_file_path: str, _find_dto_class: Callable) -> None:
        """Initialize a new instance of the StubsGenerator class."""
        class_file_path = inspect.getfile(self.__class__)
        self.methods_file_path = methods_file_path
        self.class_file_path = class_file_path
        self._find_dto_class = _find_dto_class

    def _generate_stubs(self) -> None:
        """Generate stubs for the methods defined in the methods.json file and the class itself."""
        methods = self._read_methods()
        class_file_dir, class_file_name = self._get_class_file_info()
        stubs_file_path = self._create_stubs_file_path(class_file_dir, class_file_name)

        dto_imports, stubs = self._initialize_stubs()

        # Generate stubs for the class itself
        class_stubs = self._generate_class_stubs(dto_imports)
        stubs += class_stubs

        # Generate stubs from methods defined in the JSON file
        stubs += self._generate_method_stubs(methods, dto_imports)

        # Process any additional method files
        stubs += self._process_method_files(class_file_dir, dto_imports)

        self._write_stubs_to_file(stubs_file_path, dto_imports, stubs)

    def _generate_class_stubs(self, dto_imports: List[str]) -> str:
        """Generate stubs for the class defined in the .py file."""
        class_stubs = ""

        with open(self.class_file_path, "r") as class_file:
            class_contents = class_file.read()
            class_ast = ast.parse(class_contents)

        for node in class_ast.body:
            if isinstance(node, ast.ClassDef) and node.name == self.__class__.__name__:
                class_stubs += f"class {node.name}:\n"
                for body_item in node.body:
                    if isinstance(body_item, ast.FunctionDef):
                        class_stubs += self._generate_stub_for_function(
                            body_item,
                            dto_imports,
                            self.class_file_path,
                        )
                # Add two newlines after the class definition for readability
                class_stubs += "\n\n"

        return class_stubs

    def _read_methods(self) -> Dict[str, Any]:
        """Read the methods.json file and return its contents."""
        with open(self.methods_file_path, "r") as methods_file:
            return json.load(methods_file)

    def _get_class_file_info(self) -> Tuple[str, str]:
        """Return the directory and file name of the class file."""
        class_file = inspect.getfile(self.__class__)
        return os.path.dirname(class_file), os.path.basename(class_file)

    def _create_stubs_file_path(self, class_file_dir: str, class_file_name: str) -> str:
        """Create the path for the stubs file."""
        stubs_file_name = os.path.splitext(class_file_name)[0] + ".pyi"
        return os.path.join(class_file_dir, stubs_file_name)

    def _initialize_stubs(self) -> Tuple[List[str], str]:
        """Initialize the stubs file with the necessary imports and header."""
        dto_imports = ["from typing import Any"]
        stubs = "# This file is generated. Do not edit directly.\n\n"
        return dto_imports, stubs

    def _generate_method_stubs(
        self,
        methods: Dict[str, Any],
        dto_imports: List[str],
    ) -> str:
        """Generate stubs for the methods defined in the methods.json file."""
        stubs = ""
        for method_name, details in methods.items():
            dto_class = self._find_dto_class(method_name)
            class_name = dto_class.__name__ if dto_class else "Any"
            if dto_class:
                module_name = method_name  # or however you determine the module name
                dto_imports.append(f"from .methods.{module_name} import {class_name}")

            param_list = ", ".join(
                [f"{req_param}: str" for req_param in details["params"]],
            )
            param_list = f"self, {param_list}" if param_list else "self"
            docstring = f'"""Call the "{details["endpoint"]}" endpoint with parameters: {details["params"]}."""'
            method_def = f"\tdef {method_name}({param_list}) -> {class_name}:"
            method_doc = f"\t\t{docstring}\n\t\tpass\n\n"

            stubs += method_def + "\n" + method_doc
        return stubs

    def _process_method_files(self, class_file_dir: str, dto_imports: List[str]) -> str:
        """Process the method files and generate stubs for each method."""
        methods_dir = os.path.join(class_file_dir, "methods")
        stubs_list = [
            self._process_method_file(file_path, dto_imports)
            for file_path in glob.glob(os.path.join(methods_dir, "*.py"))
        ]
        return "".join(stubs_list)

    def _process_method_file(self, file_path: str, dto_imports: List[str]) -> str:
        """Process a single method file and generate stubs for each method."""
        with open(file_path, "r") as method_file:
            return self._generate_stubs_from_file_contents(
                method_file.read(),
                dto_imports,
                file_path,
            )

    def _generate_stubs_from_file_contents(
        self,
        file_contents: str,
        dto_imports: List[str],
        file_path: str,
    ) -> str:
        """Generate stubs for each method in a file."""
        stubs = ""
        parsed_ast = ast.parse(file_contents)
        for node in parsed_ast.body:
            if isinstance(node, ast.FunctionDef):
                stubs += self._generate_stub_for_function(node, dto_imports, file_path)
        return stubs

    def _generate_stub_for_function(
        self,
        node: ast.FunctionDef,
        dto_imports: List[str],
        file_path: str,
    ) -> str:
        """Generate a stub for a single method."""
        function_name = node.name
        docstring = ast.get_docstring(node) or "No description"
        formatted_docstring = f'"""{docstring}"""'
        arg_names = [arg.arg for arg in node.args.args]
        function_args = ", ".join(arg_names)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        dto_class = self._find_dto_class(file_name)
        class_name = dto_class.__name__ if dto_class else "Any"
        if dto_class:
            dto_imports.append(f"from .methods.{file_name} import {class_name}")

        return (
            f"\tdef {function_name}({function_args}) -> {class_name}:\n"
            f"\t\t{formatted_docstring}\n"
            f"\t\tpass\n\n"
        )

    def _write_stubs_to_file(
        self,
        stubs_file_path: str,
        dto_imports: List[str],
        stubs: str,
    ) -> None:
        """Write the stubs to the stubs file."""
        with open(stubs_file_path, "w") as stub_file:
            stub_file.write("\n".join(dto_imports) + "\n\n" + stubs)
