from sqlalchemy import Column, Float, Integer, String

from apps.database import Base


class TradeSignalDB(Base):
    __tablename__ = "trade_signals"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    direction = Column(String, nullable=False)
    zone_type = Column(String, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    risk_percent = Column(Float, nullable=False)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)