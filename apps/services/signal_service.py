from fastapi import HTTPException,status,APIRouter
from apps.data import signals_db
from apps.schemas import TradeSignal
from typing import Optional

router = APIRouter()
@router.get("/")
def root():
    return {"message": "Forex Trading Bot API"}


@router.post("/tradesignal" ,status_code=status.HTTP_201_CREATED)
def create_tradesignal(signal: TradeSignal):
    create = {
        "id": len(signals_db) + 1,
        "symbol": signal.symbol,
        "price": signal.price,
        "direction": signal.direction,
        "zone_type": signal.zone_type,
        "risk": signal.risk.model_dump()
    }
    signals_db.append(create)
    return {"message": "Trade signal created", "data": create}


@router.get("/signals")
def get_signals(symbol: Optional[str] = None):
    return [s for s in signals_db if not symbol or s["symbol"].lower() == symbol.lower()]


@router.get("/signals/{id}")
def get_signal_by_id(id: int):
    
    for s in signals_db:
        if s["id"] == id:
            return s
    raise HTTPException(status_code=404, detail=f"Signal with id {id} not found")
    


@router.put("/tradesignal/{id}")
def update_tradesignal(id: int, signal: TradeSignal):
    for s in signals_db:
        if s["id"] == id:
            s["symbol"] = signal.symbol
            s["price"] = signal.price
            s["direction"] = signal.direction
            s["zone_type"] = signal.zone_type
            s["risk"] = signal.risk.model_dump()
            return {"message": "Signal updated", "data": s}
    raise HTTPException(status_code=404, detail=f"Signal with id {id} not found")


@router.delete("/tradesignal/{id}")
def delete_tradesignal(id: int):
    for index, s in enumerate(signals_db):
        if s["id"] == id:
            signals_db.pop(index)
            return {"message": f"Signal {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Signal with id {id} not found")
