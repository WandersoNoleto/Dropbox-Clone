import re
from typing import List

from pydantic import BaseModel, Field, validator


class ConverterInput(BaseModel):
    price: float = Field(gt=0)
    to_currencies: List[str]

    @validator('to_currencies')
    def validate_to_currencies(cls, to_currencies):
        for currency in to_currencies:
            if not re.match('^[A-Z]{3}$', currency):
                raise ValueError(f'Invalid currency: {currency}')
        
        return to_currencies


class ConvertOutput(BaseModel):
    message: str
    data: List[dict]
    