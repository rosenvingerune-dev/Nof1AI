from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from src.api.dependencies import get_bot_service
from src.gui.services.bot_service import BotService

router = APIRouter()

class ProposalActionRequest(BaseModel):
    reason: Optional[str] = None

@router.get("/")
def get_pending_proposals(bot_service: BotService = Depends(get_bot_service)):
    """Get all pending trade proposals"""
    proposals = bot_service.get_pending_proposals()
    return proposals

@router.post("/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: str,
    bot_service: BotService = Depends(get_bot_service)
):
    """Approve a trade proposal"""
    success = await bot_service.approve_proposal(proposal_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to approve proposal or bot not running")
    return {"status": "approved", "id": proposal_id}

@router.post("/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    request: ProposalActionRequest = Body(default=ProposalActionRequest()),
    bot_service: BotService = Depends(get_bot_service)
):
    """Reject a trade proposal"""
    reason = request.reason or "User rejected via API"
    success = await bot_service.reject_proposal(proposal_id, reason=reason)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to reject proposal or bot not running")
    return {"status": "rejected", "id": proposal_id}
