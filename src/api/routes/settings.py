from fastapi import APIRouter, Depends
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class SettingsUpdate(BaseModel):
    assets: Optional[List[str]] = None
    interval: Optional[str] = None
    llm_model: Optional[str] = None
    trading_mode: Optional[str] = None
    max_position_size: Optional[float] = None
    auto_trade_enabled: Optional[bool] = None
    auto_trade_threshold: Optional[float] = None

@router.get("/")
async def get_settings(bot_service: BotService = Depends(get_bot_service)):
    return await bot_service.get_current_config()

@router.put("/")
async def update_settings(
    settings: SettingsUpdate,
    bot_service: BotService = Depends(get_bot_service)
):
    update_data = settings.dict(exclude_unset=True)
    success = await bot_service.update_config(update_data)
    return {"success": success}
