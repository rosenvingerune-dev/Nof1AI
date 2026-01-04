from fastapi import APIRouter, Depends
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService

router = APIRouter()

@router.get("/data")
def get_market_data(bot_service: BotService = Depends(get_bot_service)):
    state = bot_service.get_state()
    if hasattr(state, 'market_data'):
        return state.market_data
    return {}

@router.post("/refresh")
async def refresh_market_data(bot_service: BotService = Depends(get_bot_service)):
    success = await bot_service.refresh_market_data()
    return {"success": success}
