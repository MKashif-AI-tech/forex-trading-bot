from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 


app = FastAPI()

signals_db = [
    {"id": 1, "symbol": "EURUSD", "price": 1.0856, "direction": "buy", "zone_type": "demand",
     "risk": {"stop_loss" : 1.0800, "take_profit": 1.0900}},
    {"id": 2, "symbol": "GBPUSD", "price": 1.2650, "direction": "sell", "zone_type": "supply","risk": {"stop_loss" : 1.2700, "take_profit": 1.2600}},
    {"id": 3, "symbol": "EURUSD", "price": 1.0901, "direction": "buy", "zone_type": "demand", "risk": {"stop_loss" : 1.0850, "take_profit": 1.0950}}
]

class Risk(BaseModel):
    stop_loss: float
    take_profit: float

class TradeSignal(BaseModel):
    symbol: str
    price: float
    direction: str
    zone_type: str
    risk: Risk


@app.post("/tradesignal")
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

@app.get("/signals")
def get_signals():

    return signals_db

@app.put("/tradesignal/{id}")
def update_tradesignal(id: int, signal: TradeSignal):
    for s in signals_db:
        if s["id"] == id:
            s["id"] = id
            s["symbol"] = signal.symbol
            s["price"] = signal.price
            s["direction"] = signal.direction
            s["zone_type"] = signal.zone_type
            s["risk"] = signal.risk.model_dump()
            return {"message": "Trade signal updated successfully", "data": s}

    raise HTTPException(status_code=404, detail="Trade signal not found")