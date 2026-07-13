from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.database import get_db
from apps.schemas import TradeSignal, UserResponse
from apps.security import get_current_user
from apps.services import signal_service

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Forex Trading Bot API"}


@router.post("/tradesignal")
def create_tradesignal(
    signal: TradeSignal,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    data = signal_service.create_tradesignal(
        db=db,
        signal=signal,
        current_user=current_user
    )

    return {
        "message": "Trade signal created",
        "data": data,
        "user": current_user.username
    }


@router.get("/signals")
def get_signals(
    symbol: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return signal_service.get_signals(
        db=db,
        current_user=current_user,
        symbol=symbol
    )


@router.get("/tradesignal/{signal_id}")
def get_signal_by_id(
    signal_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    signal = signal_service.get_signal_by_id(
        db=db,
        signal_id=signal_id,
        current_user=current_user
    )

    if signal is None:
        raise HTTPException(
            status_code=404,
            detail="Signal not found"
        )

    return signal


@router.put("/tradesignal/{signal_id}")
def update_tradesignal(
    signal_id: int,
    signal: TradeSignal,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    updated = signal_service.update_tradesignal(
        db=db,
        signal_id=signal_id,
        signal=signal,
        current_user=current_user
    )

    if updated is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission or signal not found."
        )

    return {
        "message": "Signal updated",
        "data": updated
    }


@router.delete("/tradesignal/{signal_id}")
def delete_tradesignal(
    signal_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    deleted = signal_service.delete_tradesignal(
        db=db,
        signal_id=signal_id,
        current_user=current_user
    )

    if not deleted:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission or signal not found."
        )

    return {
        "message": f"Signal {signal_id} deleted"
    }