from fastapi import APIRouter, Depends
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService

router = APIRouter()

@router.get("/")
def get_positions(bot_service: BotService = Depends(get_bot_service)):
    state = bot_service.get_state()
    return state.positions

@router.post("/{asset}/close")
async def close_position(asset: str, bot_service: BotService = Depends(get_bot_service)):
    success = await bot_service.close_position(asset)
    return {"success": success, "asset": asset}
