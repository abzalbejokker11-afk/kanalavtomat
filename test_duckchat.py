from duck_chat import DuckChat
import asyncio

async def test():
    dc = DuckChat()
    r = await dc.ask("Sportda doping nazorati haqida 3 ta muhim fakt ayt. O'zbek tilida.")
    print(f"Javob ({len(r)} belgi):")
    print(r)

asyncio.run(test())
