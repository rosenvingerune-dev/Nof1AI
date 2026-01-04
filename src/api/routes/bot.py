from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService

router = APIRouter()

class StartBotRequest(BaseModel):
    assets: Optional[List[str]] = None
    interval: Optional[str] = None

@router.get("/status")
def get_bot_status(bot_service: BotService = Depends(get_bot_service)):
    state = bot_service.get_state()
    return state

@router.post("/start")
async def start_bot(
    request: StartBotRequest,
    bot_service: BotService = Depends(get_bot_service)
):
    try:
        await bot_service.start(assets=request.assets, interval=request.interval)
        return {"status": "started", "message": "Bot started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_bot(bot_service: BotService = Depends(get_bot_service)):
    try:
        await bot_service.stop()
        return {"status": "stopped", "message": "Bot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
