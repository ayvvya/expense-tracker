from fastapi import FastAPI

app = FastAPI(title="Expense Tracker")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
