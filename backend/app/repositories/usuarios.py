"""Repositorio para usuarios"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Usuario, PreferenciaUsuario
from ..schemas import UsuarioCreate, UsuarioUpdate
from ..utils.security import hash_password


class UsuarioRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def get_all(self, db: Session, include_inactive: bool = False) -> List[Usuario]:
        """Obtener todos los usuarios"""
        query = db.query(Usuario)
        if not include_inactive:
            query = query.filter(Usuario.estado == 'active')
        return query.order_by(Usuario.nombre).all()
    
    def get_by_id(self, db: Session, id_usuario: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    def get_by_correo(self, db: Session, correo: str) -> Optional[Usuario]:
        """Obtener usuario por correo"""
        return db.query(Usuario).filter(Usuario.correo == correo).first()
    
    def create(self, db: Session, usuario_data: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        data_dict = usuario_data.model_dump(exclude={'password'})
        
        # Hash de contraseña si se proporciona
        if usuario_data.password:
            data_dict['password_hash'] = hash_password(usuario_data.password)
        
        usuario = Usuario(**data_dict)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        # Crear preferencias por defecto
        preferencia = PreferenciaUsuario(id_usuario=usuario.id_usuario)
        db.add(preferencia)
        db.commit()
        
        return usuario
    
    def update(self, db: Session, usuario: Usuario, usuario_data: UsuarioUpdate) -> Usuario:
        """Actualizar usuario existente"""
        update_data = usuario_data.model_dump(exclude_unset=True, exclude={'password'})
        
        # Hash de contraseña si se proporciona
        if usuario_data.password:
            update_data['password_hash'] = hash_password(usuario_data.password)
        
        for key, value in update_data.items():
            setattr(usuario, key, value)
        
        db.commit()
        db.refresh(usuario)
        return usuario
    
    def update_estado(self, db: Session, usuario: Usuario, estado: str) -> Usuario:
        """Actualizar solo el estado del usuario"""
        usuario.estado = estado
        db.commit()
        db.refresh(usuario)
        return usuario
    
    def delete(self, db: Session, usuario: Usuario) -> None:
        """Eliminar usuario"""
        db.delete(usuario)
        db.commit()


usuario_repository = UsuarioRepository()
