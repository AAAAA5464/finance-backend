from pydantic import BaseModel, validator

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    notes: str

    @validator("type")
    def validate_type(cls, value):
        if value not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return value


class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    category: str | None = None
    date: str | None = None
    notes: str | None = None