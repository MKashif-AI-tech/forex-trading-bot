from typing import Optional

from sqlalchemy.orm import Session

from apps.models import TradeSignalDB
from apps.schemas import TradeSignal, UserResponse


def signal_to_dict(signal: TradeSignalDB):
    return {
        "id": signal.id,
        "symbol": signal.symbol,
        "price": signal.price,
        "direction": signal.direction,
        "zone_type": signal.zone_type,
        "risk": {
            "stop_loss": signal.stop_loss,
            "take_profit": signal.take_profit
        }
    }


def create_tradesignal(
    db: Session,
    signal: TradeSignal,
    current_user: UserResponse
):
    db_signal = TradeSignalDB(
        symbol=signal.symbol,
        price=signal.price,
        direction=signal.direction,
        zone_type=signal.zone_type,
        stop_loss=signal.risk.stop_loss,
        take_profit=signal.risk.take_profit,
        owner_id=current_user.id
    )

    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)

    return signal_to_dict(db_signal)


def get_signals(
    db: Session,
    current_user: UserResponse,
    symbol: Optional[str] = None
):
    query = db.query(TradeSignalDB).filter(
        TradeSignalDB.owner_id == current_user.id
    )

    if symbol:
        query = query.filter(
            TradeSignalDB.symbol == symbol.upper()
        )

    return [
        signal_to_dict(signal)
        for signal in query.all()
    ]


def get_signal_by_id(
    db: Session,
    signal_id: int,
    current_user: UserResponse
):
    signal = db.query(TradeSignalDB).filter(
        TradeSignalDB.id == signal_id,
        TradeSignalDB.owner_id == current_user.id
    ).first()

    if signal is None:
        return None

    return signal_to_dict(signal)


def update_tradesignal(
    db: Session,
    signal_id: int,
    signal: TradeSignal,
    current_user: UserResponse
):
    db_signal = db.query(TradeSignalDB).filter(
        TradeSignalDB.id == signal_id,
        TradeSignalDB.owner_id == current_user.id
    ).first()

    if db_signal is None:
        return None

    db_signal.symbol = signal.symbol
    db_signal.price = signal.price
    db_signal.direction = signal.direction
    db_signal.zone_type = signal.zone_type
    db_signal.stop_loss = signal.risk.stop_loss
    db_signal.take_profit = signal.risk.take_profit

    db.commit()
    db.refresh(db_signal)

    return signal_to_dict(db_signal)


def delete_tradesignal(
    db: Session,
    signal_id: int,
    current_user: UserResponse
):
    db_signal = db.query(TradeSignalDB).filter(
        TradeSignalDB.id == signal_id,
        TradeSignalDB.owner_id == current_user.id
    ).first()

    if db_signal is None:
        return False

    db.delete(db_signal)
    db.commit()

    return True