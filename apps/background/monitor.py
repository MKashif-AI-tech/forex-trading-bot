import asyncio

from apps.database import SessionLocal
from apps.services.signal_service import get_signals


async def monitor_prices():

    while True:
        db = SessionLocal()

        try:
            signals = get_signals(db)

            for s in signals:
                print(f"[{s['symbol']}] Checking price against demand/supply zones...")

        except Exception as e:
            print(f"Error occurred while checking signals: {e}")

        finally:
            db.close()

        print("--- Price check complete. Sleeping 60 seconds ---")

        await asyncio.sleep(60)
