import ast
import glob
import inspect
import json
import os
import textwrap
import types
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

import astor

from .stubs_generator import StubsGenerator


class ClientServicesManager(StubsGenerator):  # noqa: WPS214
    """
    Manager for dynamically creating methods for interacting with services.

    This class simplifies service interaction by dynamically generating methods
    from JSON-defined and file-defined services, in conjunction to optional DTOs.

    Real time stub generation is also supported, which allows for IDE autocompletion and type checking.

    It boosts scalability and coding efficiency.

    Attributes:
        methods_file_path (str): The path to the JSON file containing service
            definitions.
    """

    def __init__(self, methods_file_path: Optional[str] = None) -> None:
        """Initialize a new instance of the ClientServicesManager class."""
        # Determine the methods.json path based on the class of the instance if not provided
        if methods_file_path is None:
            methods_file_path = os.path.join(
                os.path.dirname(inspect.getfile(self.__class__)),
                "methods",
                "methods.json",
            )

        super().__init__(methods_file_path, self._find_dto_class)

        if not hasattr(self, "_default_service_method_handler"):
            raise AttributeError(
                "The instance must have a '_default_service_method_handler' method",
            )
        self.default_handler = self._default_service_method_handler
        self.services = self._load_service_config()
        self._create_service_methods()
        self._load_and_bind_methods_from_files()
        self._generate_stubs()

    def _load_and_bind_methods_from_files(self) -> None:
        methods_dir = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            "methods",
        )
        for file_path in glob.glob(os.path.join(methods_dir, "*.py")):
            with open(file_path, "r") as method_file:
                file_contents = method_file.read()

            # Execute the entire file's source code in the local namespace
            local_namespace: Any = {}
            exec(file_contents, local_namespace)

            # Bind each object defined in the file as a method or store classes/variables
            for name, namespace_obj in local_namespace.items():
                if callable(namespace_obj):
                    # Bind functions as methods
                    bound_method = types.MethodType(namespace_obj, self)
                    setattr(self, name, bound_method)
                else:
                    # Store variables as attributes of the object
                    setattr(self, name, namespace_obj)

    def _load_service_config(self) -> Dict[str, Any]:
        with open(self.methods_file_path, "r") as method_file:
            return json.load(method_file)

    def _create_service_methods(self) -> None:
        for method_name, service_info in self.services.items():
            endpoint = service_info["endpoint"]
            param_names: List[str] = service_info.get("params", [])
            headers = service_info.get("headers", {})
            method_handler = getattr(self, method_name, self.default_handler)

            if method_handler is None:
                raise AttributeError(
                    f"Method handler for '{method_name}' is not defined",
                )

            bound_method = self._create_service_method(
                method_name,
                endpoint,
                method_handler,
                param_names,
                headers,
            ).__get__(self, self.__class__)
            setattr(self, method_name, bound_method)

    def _create_service_method(  # noqa: WPS211
        self,
        method_name: str,
        endpoint: str,
        method_handler: Callable,
        param_names: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Callable:
        dto_class = self._find_dto_class(method_name)

        def created_service_method(  # noqa: WPS430
            _: Any,
            *args: Optional[Any],
            **kwargs: Optional[Dict[str, Any]],
        ) -> Any:
            req_params, custom_headers = self._prepare_request_params_and_headers(
                args,
                kwargs,
                param_names,
                headers,
            )
            response = method_handler(endpoint, req_params, custom_headers)
            return self._process_response_with_dto_class(response, dto_class)

        return created_service_method

    def _prepare_request_params_and_headers(
        self,
        args: Optional[Any],
        kwargs: Optional[Dict[str, Any]],
        param_names: Optional[List[str]],
        headers: Optional[Dict[str, str]],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        req_params = dict(zip(param_names, args or [])) if param_names else {}
        custom_headers = headers.copy() if headers else {}

        if kwargs:
            req_params.update(kwargs.get("params", {}))
            custom_headers.update(kwargs.get("headers", {}))

        return req_params, custom_headers

    def _process_response_with_dto_class(
        self,
        response: Any,
        dto_class: Optional[Type],
    ) -> Any:
        if dto_class:
            return dto_class(**response)
        return response

    def _find_dto_class(self, method_name: str) -> Optional[type]:
        # Construct the file path for the method
        methods_dir = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            "methods",
        )
        file_path = os.path.join(methods_dir, f"{method_name}.py")

        try:
            with open(file_path, "r") as dto_file:
                file_contents = dto_file.read()
        except FileNotFoundError:
            # If the file does not exist, no DTO class is found
            return None

        # Parse the file and find the DTO class
        parsed_ast = ast.parse(file_contents)
        for node in parsed_ast.body:
            if isinstance(node, ast.ClassDef) and "dto" in node.name.lower():
                class_source = textwrap.dedent(astor.to_source(node))
                class_name = node.name
                # Execute the class definition in a safe namespace
                namespace: Dict[str, Any] = {}
                exec(class_source, globals(), namespace)
                return namespace.get(class_name)

        return None
