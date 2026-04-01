from models import Transaction
from fastapi import HTTPException


def create_transaction(db, data):
    txn = Transaction(**data.dict())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def get_all_transactions(db):
    return db.query(Transaction).all()


def get_transaction(db, txn_id):
    txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


def update_transaction(db, txn_id, data):
    txn = get_transaction(db, txn_id)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(txn, key, value)

    db.commit()
    db.refresh(txn)
    return txn


def delete_transaction(db, txn_id):
    txn = get_transaction(db, txn_id)
    db.delete(txn)
    db.commit()
    return {"message": "Deleted successfully"}


def filter_transactions(db, type=None, category=None, date=None):
    query = db.query(Transaction)

    if type:
        query = query.filter(Transaction.type == type)

    if category:
        query = query.filter(Transaction.category == category)

    if date:
        query = query.filter(Transaction.date == date)

    return query.all()

def get_summary(db):
    transactions = db.query(Transaction).all()

    total_income = 0
    total_expense = 0

    for t in transactions:
        if t.type == "income":
            total_income += t.amount
        else:
            total_expense += t.amount

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }

def category_breakdown(db):
    transactions = db.query(Transaction).all()

    result = {}

    for t in transactions:
        if t.category not in result:
            result[t.category] = 0
        result[t.category] += t.amount

    return result

def monthly_summary(db):
    transactions = db.query(Transaction).all()

    result = {}

    for t in transactions:
        month = t.date[:7]   

        if month not in result:
            result[month] = {
                "income": 0,
                "expense": 0
            }

        if t.type == "income":
            result[month]["income"] += t.amount
        else:
            result[month]["expense"] += t.amount

    return result

def recent_transactions(db):
    return db.query(Transaction).order_by(Transaction.id.desc()).limit(5).all()

