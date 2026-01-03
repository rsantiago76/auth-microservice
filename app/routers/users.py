from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas
from ..deps import get_current_user, require_admin
from ..security import verify_password, hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
def me(current: models.User = Depends(get_current_user)):
    return schemas.UserOut(id=current.id, email=current.email, role=current.role, is_active=current.is_active)

@router.patch("/me", response_model=schemas.UserOut)
def update_me(payload: schemas.UpdateMeIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):
    if payload.email and payload.email != current.email:
        existing = db.query(models.User).filter(models.User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current.email = payload.email

    db.add(current)
    db.commit()
    db.refresh(current)
    return schemas.UserOut(id=current.id, email=current.email, role=current.role, is_active=current.is_active)

@router.post("/change-password")
def change_password(payload: schemas.ChangePasswordIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):
    if not verify_password(payload.current_password, current.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current.password_hash = hash_password(payload.new_password)
    db.add(current)
    db.commit()
    return {"status": "ok"}

admin = APIRouter(prefix="/admin", tags=["admin"])

@admin.get("/users")
def list_users(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    users = db.query(models.User).order_by(models.User.id.asc()).all()
    return [
        schemas.UserOut(id=u.id, email=u.email, role=u.role, is_active=u.is_active).model_dump()
        for u in users
    ]

@admin.patch("/users/{user_id}/role")
def set_role(user_id: int, payload: schemas.AdminSetRoleIn, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.role = payload.role
    db.add(u)
    db.commit()
    return {"status": "ok", "user_id": u.id, "role": u.role}

@admin.patch("/users/{user_id}/disable")
def disable_user(user_id: int, payload: schemas.AdminDisableIn, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.is_active = payload.is_active
    db.add(u)
    db.commit()
    return {"status": "ok", "user_id": u.id, "is_active": u.is_active}
