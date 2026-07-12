from collections.abc import Callable
from typing import Optional, Any
from pydantic import BaseModel, PositiveInt

class ZariModel(BaseModel):
    name: str
    namep: str
    default_str_length: Optional[PositiveInt] = None
    gen_sql: bool = False
    dummy_data: bool = False
    
    props: list[ZariProp]

class ZariProp(BaseModel):
    name: str # Name of the property.
    display_name: str | None = None # Human readable name of the property.
    type: str # The SQL data type.
    length: Optional[PositiveInt] = None # The length in characters for text, or precision for numeric types.
    precision: Optional[PositiveInt] = None  # Only applies for numeric types.
    default_value: Optional[str] = None # (default: NULL) Value to use if left in blank.
    optional: bool = True # (default: y). Whether the property is mandatory or optional.
    dummy_data: Optional[bool] = None # (default: None). Override the model's config for this specific property.
    dummy_method: Optional[Callable] = None # (default: None). The method used to generate dummy data. Consider checking the Faker docs (https://faker.readthedocs.io/en/master/).
    dummy_args: Optional[dict[str, Any]] = None # (default: None). Map of arguments for dummy_method.
    validations: Optional[list] = None # (default:None). List of valid values for the model.