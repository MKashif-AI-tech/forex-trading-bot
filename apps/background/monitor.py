import asyncio
from apps.data import signals_db
async def monitor_prices():
    

    while True:

        for s in signals_db:

            try:
                print(f"[{s['symbol']}] Checking price against demand/supply zones...")

            except Exception as e:
                print(f"Error occurred while checking {s['symbol']}: {e}")

        print("--- Price check complete. Sleeping 60 seconds ---")

        await asyncio.sleep(60)