from fastapi import FastAPI, HTTPException
import uvicorn
from models import create_DB, TableORM, ReservationORM
from Pydantc_shema import TableModel, ReservationModel

app = FastAPI()
create_DB()

@app.get("/")
def home_page():
    return {"massage": "main_pagea"}


#end-poins for tables:


@app.get("/tables", tags="t")
def show_tables():
    ans = TableORM.get_all_tables()
    if ans:
        return ans
    raise HTTPException(status_code=404, detail="base of tables is empty")

@app.get("/tables/{id}", tags="t")
def show_table_by_id(id: int):
    ans = TableORM.get_table(id)
    if ans:
        return ans
    raise HTTPException(status_code=404, detail="table not found")


@app.post("/tables/add_new_table", tags="t")
def add_new_table_(table: TableModel):
    TableORM.add_new_table(name=table.name, seats=table.seats, lockation=table.lockation)
    return {"massege": "compete"}

@app.delete("/tables/del_table/{id}", tags="t")
def delete_teble_by_id(id: int):
    if TableORM.get_table(id):
        TableORM.delitte_table(id)
        return {"massage": "complete"}
    else:
        raise HTTPException(status_code=404, detail="string not found")


#end-poins for reservation:


@app.get("/reservations", tags="r")
def get_all_reservations():
    ans = ReservationORM.get_all_reservation()
    if ans:
        return ans
    raise HTTPException(status_code=404, detail="base of reservations is empty")

@app.get("/reservations_with_table/{id}", tags="r")
def get_reservation_with_table_by_id(id: int):
    ans = ReservationORM.select_reservation_with_table(id)
    if ans:
        return ans
    raise HTTPException(status_code=404, detail="reservation not found")



@app.get("/reservations/{id}", tags="r")
def get_reservation_by_id(id: int):
    ans = ReservationORM.get_reservation(id)
    if ans:
        return ans
    raise HTTPException(status_code=404, detail="reservation not found")


@app.post("/reservations/add_new_reservation", tags="r")
def add_new_reservation(reservation: ReservationModel):
    ReservationORM.add_new_reservation(customer_name=reservation.customer_name, table_id=reservation.table_id)
    return {"massage": "complete"}

@app.delete("/reservations/del_res/{id}", tags="r")
def del_reservation_by_id(id: int):
    if ReservationORM.get_reservation(id=id):
        ReservationORM.delete_reservation(id=id)
        return {"massage": "complete"}
    else:
        raise HTTPException(status_code=404, detail="string not found")



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)