"""Modelos SQLAlchemy para el sistema de inspecciones"""
from datetime import datetime
from sqlalchemy import (
    BigInteger, String, Text, DECIMAL, DateTime, Enum, 
    ForeignKey, Index, Integer, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from ..core.database import Base


class Usuario(Base):
    """Tabla usuarios"""
    __tablename__ = "usuarios"
    
    id_usuario: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(191), nullable=False, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rol: Mapped[str] = mapped_column(
        Enum('inspector', 'supervisor', 'admin', name='usuario_rol_enum'),
        nullable=False,
        default='inspector'
    )
    estado: Mapped[str] = mapped_column(
        Enum('active', 'inactive', name='usuario_estado_enum'),
        nullable=False,
        default='active'
    )
    ultimo_acceso: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    
    # Relaciones
    inspecciones: Mapped[List["Inspeccion"]] = relationship("Inspeccion", back_populates="inspector")
    preferencias: Mapped[Optional["PreferenciaUsuario"]] = relationship(
        "PreferenciaUsuario", back_populates="usuario", uselist=False
    )
    bitacoras: Mapped[List["BitacoraAuditoria"]] = relationship("BitacoraAuditoria", back_populates="usuario")


class Planta(Base):
    """Tabla plantas"""
    __tablename__ = "plantas"
    
    id_planta: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(191), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    
    # Relaciones
    inspecciones: Mapped[List["Inspeccion"]] = relationship("Inspeccion", back_populates="planta")


class Naviera(Base):
    """Tabla navieras"""
    __tablename__ = "navieras"
    
    id_navieras: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    
    # Relaciones
    inspecciones: Mapped[List["Inspeccion"]] = relationship("Inspeccion", back_populates="naviera")


class Inspeccion(Base):
    """Tabla inspecciones"""
    __tablename__ = "inspecciones"
    
    id_inspeccion: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    numero_contenedor: Mapped[str] = mapped_column(String(30), nullable=False)
    id_planta: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("plantas.id_planta", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    id_navieras: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("navieras.id_navieras", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    temperatura_c: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    firma_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    id_inspector: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("usuarios.id_usuario", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    estado: Mapped[str] = mapped_column(
        Enum('pending', 'approved', 'rejected', name='inspeccion_estado_enum'),
        nullable=False,
        default='pending'
    )
    inspeccionado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    
    # Relaciones
    planta: Mapped["Planta"] = relationship("Planta", back_populates="inspecciones")
    naviera: Mapped["Naviera"] = relationship("Naviera", back_populates="inspecciones")
    inspector: Mapped["Usuario"] = relationship("Usuario", back_populates="inspecciones")
    fotos: Mapped[List["FotoInspeccion"]] = relationship(
        "FotoInspeccion", back_populates="inspeccion", cascade="all, delete-orphan"
    )


# Índices compuestos
Index('ix_inspecciones_planta_estado_fecha', 
      Inspeccion.id_planta, Inspeccion.estado, Inspeccion.inspeccionado_en)


class FotoInspeccion(Base):
    """Tabla fotos_inspeccion"""
    __tablename__ = "fotos_inspeccion"
    
    id_foto: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id_inspeccion: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("inspecciones.id_inspeccion", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    foto_path: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(50), nullable=False, default='image/jpeg')
    hash_hex: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tomada_en: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    # Relaciones
    inspeccion: Mapped["Inspeccion"] = relationship("Inspeccion", back_populates="fotos")


class BitacoraAuditoria(Base):
    """Tabla bitacora_auditoria"""
    __tablename__ = "bitacora_auditoria"
    
    id_evento: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id_usuario: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id_usuario", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    accion: Mapped[str] = mapped_column(String(120), nullable=False)
    detalles: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    # Relaciones
    usuario: Mapped[Optional["Usuario"]] = relationship("Usuario", back_populates="bitacoras")


Index('ix_bitacora_usuario_fecha', BitacoraAuditoria.id_usuario, BitacoraAuditoria.creado_en)


class PreferenciaUsuario(Base):
    """Tabla preferencias_usuario"""
    __tablename__ = "preferencias_usuario"
    
    id_usuario: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id_usuario", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    auto_sync: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notificaciones: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    geolocalizacion: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    
    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="preferencias")
