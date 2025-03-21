from typing import List, Optional

import libcst as cst
from typing_extensions import override, Self


class InitializeModelTransformer(cst.CSTTransformer):
    """
    AST transformer to add/modify initialize_model method in a class.
    """

    def __init__(
        self: Self,
        target_class_name: str,
        model_field_name: str,
        repository: str,
        model_name: str,
        version: str,
        framework_name: str,
    ):
        super().__init__()
        self.__target_class_name: str = target_class_name
        self.__model_field_name: str = model_field_name
        self.__repository: str = repository
        self.__model_name: str = model_name
        self.__version: str = version
        self.__framework_name: str = framework_name
        self.__is_modified: bool = False
        self.__method_name: str = "initialize_model"
        self.__current_class_name: Optional[str] = None

    @property
    def is_modified(self: Self) -> bool:
        return self.__is_modified

    @override
    def visit_ClassDef(self: Self, node: cst.ClassDef) -> bool:
        """
        Visit the ClassDef node and add/modify the initialize_model method.

        :param node: The ClassDef node
        :return: True if this class should be visited, False otherwise
        """
        if node.name.value == self.__target_class_name:
            self.__current_class_name = node.name.value
            return True

        return False

    @override
    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        if original_node.name.value != self.__target_class_name:
            return updated_node

        self.__current_class_name = None

        # Check if initialize_model already exists
        is_initialize_model_method_exists: bool = False
        initialize_method_index: int = -1

        for i, statement in enumerate(updated_node.body.body):
            if (
                isinstance(statement, cst.FunctionDef)
                and statement.name.value == self.__method_name
            ):
                is_initialize_model_method_exists = True
                initialize_method_index = i
                break

        if is_initialize_model_method_exists:
            new_body: List[cst.BaseStatement] = list(updated_node.body.body)
            new_body[initialize_method_index] = self.__create_initialize_model_method()
            self.__is_modified = True
            return updated_node.with_changes(
                body=updated_node.body.with_changes(body=tuple(new_body))
            )

        # If initialize_model doesn't exist, add it at the end
        new_body = list(updated_node.body.body)
        new_body.append(self.__create_initialize_model_method())
        self.__is_modified = True

        return updated_node.with_changes(
            body=updated_node.body.with_changes(body=tuple(new_body))
        )

    def __create_initialize_model_method(self: Self) -> cst.FunctionDef:
        """
        Create the CST for the initialize_model method.
        """
        docstring = cst.SimpleString(
            value='"""This method is called on the inference phase to load the model"""'
        )
        import_comment = cst.Comment(
            value="# We add this import in case it wasn't imported earlier"
        )

        load_model_call: cst.Call = self.__create_load_model_call()
        assignment: cst.Assign = self.__create_model_assignment_line(load_model_call)

        return cst.FunctionDef(
            name=cst.Name(self.__method_name),
            params=cst.Parameters(
                params=[cst.Param(cst.Name("self"))],
            ),
            body=cst.IndentedBlock(
                body=[
                    cst.SimpleStatementLine(body=[cst.Expr(value=docstring)]),
                    cst.SimpleStatementLine(body=[cst.Expr(value=import_comment)]),
                    cst.SimpleStatementLine(
                        body=[
                            cst.Import(names=[cst.ImportAlias(name=cst.Name("frogml"))])
                        ]
                    ),
                    cst.EmptyLine(),
                    cst.SimpleStatementLine(body=[assignment]),
                ],
            ),
            leading_lines=[cst.EmptyLine()],
        )

    def __create_load_model_call(self: Self) -> cst.Call:
        """
        Create the call to frogml.{{framework_name}}.load_model(...)

        :return: The call to frogml.{{framework_name}}.load_model(...)
        """
        return cst.Call(
            func=cst.Attribute(
                value=cst.Attribute(
                    value=cst.Name("frogml"),
                    attr=cst.Name(self.__framework_name),
                ),
                attr=cst.Name("load_model"),
            ),
            args=[
                cst.Arg(
                    keyword=cst.Name("repository"),
                    value=cst.SimpleString(f'"{self.__repository}"'),
                    equal=cst.AssignEqual(
                        whitespace_before=cst.SimpleWhitespace(value=""),
                        whitespace_after=cst.SimpleWhitespace(value=""),
                    ),
                ),
                cst.Arg(
                    keyword=cst.Name("model_name"),
                    value=cst.SimpleString(f'"{self.__model_name}"'),
                    equal=cst.AssignEqual(
                        whitespace_before=cst.SimpleWhitespace(value=""),
                        whitespace_after=cst.SimpleWhitespace(value=""),
                    ),
                ),
                cst.Arg(
                    keyword=cst.Name("version"),
                    value=cst.SimpleString(f'"{self.__version}"'),
                    equal=cst.AssignEqual(
                        whitespace_before=cst.SimpleWhitespace(value=""),
                        whitespace_after=cst.SimpleWhitespace(value=""),
                    ),
                ),
            ],
        )

    def __create_model_assignment_line(
        self: Self, load_model_call: cst.Call
    ) -> cst.Assign:
        """
        Create the assignment: self_model = frogml.{{framework_name}}.load_model(...)

        :param load_model_call: The load_model call

        :return: The assignment line
        """
        return cst.Assign(
            targets=[
                cst.AssignTarget(
                    target=cst.Attribute(
                        value=cst.Name("self"),
                        attr=cst.Name(self.__model_field_name),
                    )
                )
            ],
            value=load_model_call,
        )
