import asyncio, os
# pyrefly: ignore [missing-import]
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def clear_db():
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = client.contractgraph
    print("Dropping old collections to force a re-seed with accurate risk history...")
    await db.projects.drop()
    await db.contract_baselines.drop()
    await db.monthly_reports.drop()
    await db.risk_history.drop()
    print("Database cleared. The next backend startup will re-seed everything with correct deviation calculations.")

if __name__ == "__main__":
    asyncio.run(clear_db())
