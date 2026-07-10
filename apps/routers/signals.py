from fastapi import APIRouter, Depends, HTTPException, status
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.schemas import TradeSignal, UserResponse
from apps.security import get_current_user
from apps.services import signal_service
from typing import Optional


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Forex Trading Bot API"}


@router.post("/tradesignal")
def create_tradesignal(signal: TradeSignal, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    data = signal_service.create_tradesignal(db, signal)
    return {
        "message": "Trade signal created",
        "data": data,
        "user": current_user.username,  # Optional: if you want to use user info in the response
    }


@router.get("/signals")
def get_signals( symbol: Optional[str] = None,    db: Session = Depends(get_db),    current_user: UserResponse = Depends(get_current_user)):
    
    return signal_service.get_signals(db, symbol)

@router.get("/tradesignal/{signal_id}")
def get_signal_by_id(signal_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    signal = signal_service.get_signal_by_id(db, signal_id)
    if signal is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal


@router.put("/tradesignal/{signal_id}")
def update_tradesignal(signal_id: int, signal: TradeSignal, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    updated = signal_service.update_tradesignal(db, signal_id, signal)
    if updated is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    return {
        "message": "Signal updated",
        "data": updated,
    }


@router.delete("/tradesignal/{signal_id}")
def delete_tradesignal(signal_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    deleted = signal_service.delete_tradesignal(db, signal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Signal not found")
    return {
        "message": f"Signal {signal_id} deleted"
    }
