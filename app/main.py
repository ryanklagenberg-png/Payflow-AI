import logging

from fastapi import FastAPI

from app.api.invoices import router as invoices_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

app = FastAPI(
    title="PayFlow AI",
    description="AI-powered Accounts Payable automation for construction companies",
    version="0.1.0",
)

app.include_router(invoices_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
