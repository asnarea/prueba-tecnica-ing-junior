from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_item_service
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate, PaginatedItems
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=PaginatedItems)
def list_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    service: ItemService = Depends(get_item_service),
):
    items, total = service.list_items(page=page, limit=limit)
    return PaginatedItems(
        items=[ItemResponse.model_validate(i) for i in items],
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, service: ItemService = Depends(get_item_service)):
    item = service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(
        title=payload.title,
        priority=payload.priority,
        description=payload.description,
    )


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item_status(
    item_id: str,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
):
    item = service.update_status(item_id, payload.status)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item
