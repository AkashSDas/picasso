class NonUpdateableColumnError(AttributeError):
    """
    This is an exception that is raised when a non-updateable column is
    attempted to be updated.
    """

    def __init__(
        self,
        cls: str,
        column: str,
        old_value: str,
        new_value: str,
        message: str | None = None,
    ) -> None:
        self.cls = cls
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

        if message is None:
            self.message = (
                f"Cannot update column {column} on model {cls} from "
                f"{old_value} to {new_value}: column is non-updateable."
            )
