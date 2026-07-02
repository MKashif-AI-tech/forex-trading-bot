from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

app = FastAPI()

signals_db = [
    {"id": 1, "symbol": "EURUSD", "price": 1.0856, "direction": "buy",
     "zone_type": "demand", "risk": {"stop_loss": 1.0800, "take_profit": 1.0900, "risk_percent": 1.0}},
    {"id": 2, "symbol": "GBPUSD", "price": 1.2650, "direction": "sell",
     "zone_type": "supply", "risk": {"stop_loss": 1.2700, "take_profit": 1.2600, "risk_percent": 1.0}},
    {"id": 3, "symbol": "EURUSD", "price": 1.0901, "direction": "buy",
     "zone_type": "demand", "risk": {"stop_loss": 1.0850, "take_profit": 1.0950, "risk_percent": 1.0}}
]


class Risk(BaseModel):
    stop_loss: float
    take_profit: float
    risk_percent: float = 1.0


class TradeSignal(BaseModel):
    symbol: str
    price: float
    direction: str
    zone_type: str
    risk: Risk

    @field_validator('zone_type')
    @classmethod
    def validate_zone(cls, value):
        allowed = ["demand", "supply"]
        value = value.lower()
        if value not in allowed:
            raise ValueError(f"zone_type must be one of {allowed}")
        return value


    @model_validator(mode="after")
    def validate_zone_direction(self):
        if self.zone_type == "demand" and self.direction != "buy":
            raise ValueError("Demand zone requires buy direction")
        if self.zone_type == "supply" and self.direction != "sell":
            raise ValueError("Supply zone requires sell direction")
        return self


@app.get("/")
def root():
    return {"message": "Forex Trading Bot API"}


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
def get_signals(direction: Optional[str] = None):
    return [s for s in signals_db if not direction
            or s["direction"].lower() == direction.lower()]


@app.get("/signals/{symbol}")
def get_signal_by_symbol(symbol: str):
    matches = [s for s in signals_db if s["symbol"].lower() == symbol.lower()]
    if not matches:
        raise HTTPException(status_code=404, detail=f"{symbol} not found")
    
    return matches


@app.put("/tradesignal/{id}")
def update_tradesignal(id: int, signal: TradeSignal):
    for s in signals_db:
        if s["id"] == id:
            s["symbol"] = signal.symbol
            s["price"] = signal.price
            s["direction"] = signal.direction
            s["zone_type"] = signal.zone_type
            s["risk"] = signal.risk.model_dump()
            return {"message": "Signal updated", "data": s}
    raise HTTPException(status_code=404, detail="Signal not found")


@app.delete("/tradesignal/{id}")
def delete_tradesignal(id: int):
    for index, s in enumerate(signals_db):
        if s["id"] == id:
            signals_db.pop(index)
            return {"message": f"Signal {id} deleted"}
    raise HTTPException(status_code=404, detail="Signal not found")