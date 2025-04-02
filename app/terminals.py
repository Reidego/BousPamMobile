from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import os
import crud_utils
import models
import schemas
from database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


terminal_router = APIRouter(prefix='/terminals', tags=['Взаимодействие с терминалами'])

@terminal_router.put("/payment/") #, response_model=schemas.Product
def payment_by_user_id(operation: schemas.OperationPaymentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    db_terminal = crud_utils.get_terminal_by_id(db, terminal_id=operation.id_terminal)
    if db_terminal is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{operation.id_terminal}\' not found")
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    if db_terminal.hash != operation.terminal_hash:
        raise HTTPException(status_code=404, detail=f"Incorrect terminal hash")
    delta_time = datetime.now() - operation.request_time.replace(tzinfo=None)
    #crud_utils.create_operation_payment(db, operation, 'payment')
    balance_change = crud_utils.get_price_by_terminal_id(db, operation.id_terminal)
    if delta_time < timedelta(minutes=1):
        if db_user.balance < abs(balance_change):
            raise HTTPException(status_code=400, detail=f"Insufficient funds to make the payment")
        else:
            return crud_utils.create_operation_payment(db, operation, 'payment')
    return crud_utils.create_operation_payment(db, operation, 'payment')
