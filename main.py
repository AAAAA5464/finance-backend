from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import schemas, services

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 ROLE CHECK FUNCTION
def check_role(role, allowed_roles):
    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")


# CREATE (ADMIN ONLY)
@app.post("/transactions")
def create(
    data: schemas.TransactionCreate,
    role: str = "viewer",
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])
    return services.create_transaction(db, data)


# READ (ALL ROLES)
@app.get("/transactions")
def read_all(role: str = "viewer", db: Session = Depends(get_db)):
    return services.get_all_transactions(db)


# FILTER (ANALYST + ADMIN)
@app.get("/transactions/filter")
def filter_data(
    role: str = "viewer",
    type: str = Query(None),
    category: str = Query(None),
    date: str = Query(None),
    db: Session = Depends(get_db)
):
    check_role(role, ["analyst", "admin"])
    return services.filter_transactions(db, type, category, date)


# READ ONE
@app.get("/transactions/{txn_id}")
def read_one(txn_id: int, role: str = "viewer", db: Session = Depends(get_db)):
    return services.get_transaction(db, txn_id)


# UPDATE (ADMIN ONLY)
@app.put("/transactions/{txn_id}")
def update(
    txn_id: int,
    data: schemas.TransactionUpdate,
    role: str = "viewer",
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])
    return services.update_transaction(db, txn_id, data)


# DELETE (ADMIN ONLY)
@app.delete("/transactions/{txn_id}")
def delete(txn_id: int, role: str = "viewer", db: Session = Depends(get_db)):
    check_role(role, ["admin"])
    return services.delete_transaction(db, txn_id)


# SUMMARY (ALL)
@app.get("/summary")
def summary(role: str = "viewer", db: Session = Depends(get_db)):
    return services.get_summary(db)


# CATEGORY
@app.get("/category-summary")
def category_summary(role: str = "viewer", db: Session = Depends(get_db)):
    return services.category_breakdown(db)


# MONTHLY
@app.get("/monthly-summary")
def monthly(role: str = "viewer", db: Session = Depends(get_db)):
    return services.monthly_summary(db)


# RECENT
@app.get("/recent")
def recent(role: str = "viewer", db: Session = Depends(get_db)):
    return services.recent_transactions(db)