from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import  Optional

app=FastAPI()

signals_db = [
    {"id": 1, "symbol": "EURUSD", "price": 1.0856, "direction": "buy", "zone_type": "demand", },
    {"id": 2, "symbol": "GBPUSD", "price": 1.2650, "direction": "sell", "zone_type": "supply"},
    {"id": 3, "symbol": "EURUSD", "price": 1.0901, "direction": "buy", "zone_type": "demand", }
]
class TradeSignal(BaseModel):
   
    symbol: str
    price: float
    direction: str
    zone_type: str

@app.post("/tradesignal")
def create_tradesignal( signal: TradeSignal):
    
    create={
        "id": len(signals_db) + 1,
        "symbol": signal.symbol,
        "price": signal.price,
        "direction": signal.direction,
        "zone_type": signal.zone_type
    }
    signals_db.append(create)

    return {"message": "Trade signal created successfully", "data": create    
    }

@app.put("/tradesignal/{id}")
def update_tradesignal(id: int, signal: TradeSignal):
    for s in signals_db:
        if s["id"] == id:
            s["id"] = id
            s["symbol"] = signal.symbol
            s["price"] = signal.price
            s["direction"] = signal.direction
            s["zone_type"] = signal.zone_type
            return {"message": "Trade signal updated successfully", "data": s}

    raise HTTPException(status_code=404, detail="Trade signal not found")

@app.delete("/tradesignal")
def delete_tradesignal(id: int):
    for index, s in enumerate(signals_db):
        if s["id"] == id:
            signals_db.pop(index)
            return {"message": "Trade signal deleted successfully", "data": s}

    raise HTTPException(status_code=404, detail="Trade signal not found")

@app.get_signals("/signals")
def get_signals(direction:Optional[str]=None):

    return [s for s in signals_db if not direction or s["direction"].lower()==direction.lower()]

@app.get("/signals/{symb}")
def get_signalby_symbol(symb:str):
    matches=[s for s in signals_db if s["symbol"].lower()==symb.lower()]
    return matches

