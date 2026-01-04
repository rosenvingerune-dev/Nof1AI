from fastapi import APIRouter, Depends, Query
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService

router = APIRouter()

@router.get("/")
def get_trades(
    limit: int = 50, 
    offset: int = 0, 
    asset: str = None, 
    action: str = None,
    bot_service: BotService = Depends(get_bot_service)
):
    trades = bot_service.get_trade_history(limit=limit, offset=offset, asset=asset, action=action)
    return trades
