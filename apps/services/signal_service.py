from typing import Optional
from unittest import result
from sqlalchemy.orm import Session

from apps.database import get_db
from apps.models import TradeSignalDB
from apps.schemas import TradeSignal


def signal_to_dict(signal: TradeSignalDB):
    return {
        "id": signal.id,
        "symbol": signal.symbol,
        "price": signal.price,
        "direction": signal.direction,
        "zone_type": signal.zone_type,
        "risk": {
            "stop_loss": signal.stop_loss,
            "take_profit": signal.take_profit,
            "risk_percent": signal.risk_percent,
        },
    }


def create_tradesignal(db: Session, signal: TradeSignal ):
    db_signal = TradeSignalDB(
        symbol=signal.symbol,
        price=signal.price,
        direction=signal.direction,
        zone_type=signal.zone_type,
        stop_loss=signal.risk.stop_loss,
        take_profit=signal.risk.take_profit,
        risk_percent=signal.risk.risk_percent,
    )

    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)

    return signal_to_dict(db_signal)


def get_signals( db: Session,symbol: Optional[str] = None):
    query = db.query(TradeSignalDB)

    if symbol:
        query = query.filter(TradeSignalDB.symbol == symbol.upper())
    result = []

    for signal in query.all():
        result.append(signal_to_dict(signal))

    return result


def get_signal_by_id( db: Session,signal_id: int):
    signal = db.get(TradeSignalDB, signal_id)

    if signal is None:
        return None

    return signal_to_dict(signal)


def update_tradesignal(db: Session,signal_id: int, signal: TradeSignal):
    db_signal = db.get(TradeSignalDB, signal_id)

    if db_signal is None:
        return None

    db_signal.symbol = signal.symbol
    db_signal.price = signal.price
    db_signal.direction = signal.direction
    db_signal.zone_type = signal.zone_type
    db_signal.stop_loss = signal.risk.stop_loss
    db_signal.take_profit = signal.risk.take_profit
    db_signal.risk_percent = signal.risk.risk_percent

    db.commit()
    db.refresh(db_signal)

    return signal_to_dict(db_signal)


def delete_tradesignal(db: Session, signal_id: int = None):
    db_signal = db.get(TradeSignalDB, signal_id)

    if db_signal is None:
        return False

    db.delete(db_signal)
    db.commit()

    return True
