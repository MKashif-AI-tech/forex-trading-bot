from fastapi import APIRouter, HTTPException, status
from apps.schemas import TradeSignal
from apps.services import signal_service
from typing import Optional


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Forex Trading Bot API"}


@router.post("/tradesignal", status_code=status.HTTP_201_CREATED)
def create_tradesignal(signal: TradeSignal):
    data = signal_service.create_tradesignal(signal)
    return {
        "message": "Trade signal created",
        "data": data,
    }


@router.get("/signals")
def get_signals(symbol: Optional[str] = None):
    return signal_service.get_signals(symbol)


@router.get("/tradesignal/{signal_id}")
def get_signal_by_id(signal_id: int):
    signal = signal_service.get_signal_by_id(signal_id)
    if signal is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal


@router.put("/tradesignal/{signal_id}")
def update_tradesignal(signal_id: int, signal: TradeSignal):
    updated = signal_service.update_tradesignal(signal_id, signal)
    if updated is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    return {
        "message": "Signal updated",
        "data": updated,
    }


@router.delete("/tradesignal/{signal_id}")
def delete_tradesignal(signal_id: int):
    deleted = signal_service.delete_tradesignal(signal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Signal not found")
    return {
        "message": f"Signal {signal_id} deleted"
    }
