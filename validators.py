from fastapi import FastAPI
from pydantic import BaseModel, field_validator, model_validator

app = FastAPI()


class TradeSignal(BaseModel):
    symbol: str
    price: float
    volume: float
    direction: str
    stop_loss: float
    take_profit: float
    zone_type: str

    @field_validator('zone_type')
    @classmethod
    def validate_zone(cls, value):
        allowed_zone = ["demand", "supply"]
        value = value.lower()
        if value not in allowed_zone:
            raise ValueError(f"zone_type must be one of {allowed_zone}")
        return value

    @field_validator('direction')
    @classmethod
    def validate_direction(cls, value):
        allowed_directions = ["buy", "sell"]
        value = value.lower()
        if value not in allowed_directions:
            raise ValueError(f"direction must be one of {allowed_directions}")
        return value

    @model_validator(mode="after")
    def validate_entry(self):
        if self.zone_type == "demand" and self.direction != "buy":
            raise ValueError(
                f"{self.direction} is not an allowed direction for 'demand' zone."
            )
        if self.zone_type == "supply" and self.direction != "sell":
            raise ValueError(
                f"{self.direction} is not an allowed direction for 'supply' zone."
            )
        return self


@app.get("/")
def root():
    return {"message": "Welcome to the Trade Signal API"}


@app.post("/tradesignal")
def create_tradesignal(signal: TradeSignal):
    return {
        "received": True,
        "pair": signal.symbol,
        "price": signal.price,
        "volume": signal.volume,
        "stop_loss": signal.stop_loss,
        "take_profit": signal.take_profit,
        "zone_type": signal.zone_type,
        "direction": signal.direction
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}