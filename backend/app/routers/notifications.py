from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..utils.auth import get_current_active_user
from ..models import Usuario
from ..services.notification_manager import notification_manager

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get("/", response_model=List[dict])
def list_notifications(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    """Listar notificaciones para el usuario autenticado (incluye por rol)."""
    roles = [current_user.rol]
    items = notification_manager.list_for_user(user_id=current_user.id_usuario, roles=roles)
    return items


@router.post("/{notif_id}/read")
def mark_read(notif_id: str, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    """Marcar notificación como leída."""
    ok = notification_manager.mark_read(notif_id, user_id=current_user.id_usuario)
    if not ok:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"ok": True}
