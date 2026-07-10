from pydantic import BaseModel, Field, field_validator, model_validator

class Risk(BaseModel):
    stop_loss: float
    take_profit: float
    risk_percent: float = Field(gt=0, le=5, description="Risk percent must be greater than 0")


class TradeSignal(BaseModel):
    symbol: str=Field(pattern="^[A-Z]{6}$", description="Symbol must be 6 uppercase letters")
    price: float=Field(gt=0, description="Price must be greater than 0")
    direction: str=Field(min_length=3, max_length=4, description="Direction must be 'buy' or 'sell'")
    zone_type: str
    risk: Risk

   

    @field_validator('zone_type')
    @classmethod
    def validate_zone(cls, value):
        allowed = ["DEMAND", "SUPPLY"]
        value = value.upper()
        if value not in allowed:
            raise ValueError(f"zone_type must be one of {allowed}")
        return value
    
    @field_validator("direction")
    @classmethod
    def normalize_direction(cls, value):
        value = value.lower()

        if value not in ["buy","sell"]:
            raise ValueError("Direction must be 'buy' or 'sell'")

        return value
    # @field_validator("symbol")
    # @classmethod
    # def clean_symbol(cls, value):
    #     return value.upper()

    @model_validator(mode="after")
    def validate_zone_direction(self):

        direction = self.direction.lower()

        if self.zone_type == "demand" and direction != "buy":
            raise ValueError("Demand zone requires buy direction")
        if self.zone_type == "supply" and direction != "sell":
            raise ValueError("Supply zone requires sell direction")
        
        if direction=="buy":
            if self.risk.stop_loss >= self.price:
                raise ValueError("Stop loss must be less than the price for buy direction")
            if self.risk.take_profit <= self.price:
                raise ValueError("Take profit must be greater than the price for buy direction")
            
        if direction=="sell":
            if self.risk.stop_loss <= self.price:
                raise ValueError("Stop loss must be greater than the price for sell direction")
            if self.risk.take_profit >= self.price:
                raise ValueError("Take profit must be less than the price for sell direction")
        return self

class UserCreate(BaseModel):
    username: str=Field(min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: str=Field(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", description="Invalid email format")
    password: str=Field(min_length=6, description="Password must be at least 6 characters")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str