from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/")
def placeholder() -> None:
    """Placeholder only; this capability is not implemented in Phase 0."""
    raise HTTPException(status_code=501, detail="Not implemented: Phase 0 placeholder")
