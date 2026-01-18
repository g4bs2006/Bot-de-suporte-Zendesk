from fastapi import FastAPI
from app.api import webhook

app = FastAPI(title="Bot Suporte IA + Zendesk")

# Incluindo as rotas
app.include_router(webhook.router)

@app.get("/")
def health_check():
    return {"status": "online", "service": "Bot Suporte IA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
