from pydantic import BaseModel, Field

class TableModel(BaseModel):
    name: str
    seats: int
    lockation: str

class ReservationModel(BaseModel):
    customer_name: str
    table_id: int
