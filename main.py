import logging
import uvicorn
from fastapi import FastAPI
from products import router as tours_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Туристическое агентство API",
    description="API для поиска туров",
    version="1.0.0",
)

app.include_router(tours_router)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в туристическое агентство!",
        "docs": "Перейдите на /docs для просмотра документации"
    }

def main():
    logger.info('Сервер запускается...')
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

if __name__ == "__main__":
    main()