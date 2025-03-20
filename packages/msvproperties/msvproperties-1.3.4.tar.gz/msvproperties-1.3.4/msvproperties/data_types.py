from pydantic_core import core_schema
from datetime import datetime


class Date(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type, handler: core_schema.ValidatorFunctionWrapHandler
    ) -> core_schema.CoreSchema:
        schema = handler.generate_schema(str)
        return core_schema.no_info_after_validator_function(cls.validate_date, schema)

    @staticmethod
    def validate_date(value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date must be in YYYY-MM-DD format, got {value}")
        return value
