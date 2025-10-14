"""Tests para endpoints de plantas"""
import pytest


def test_listar_plantas_vacio(client):
    """Test listar plantas cuando no hay datos"""
    response = client.get("/api/plantas")
    assert response.status_code == 200
    assert response.json() == []


def test_crear_planta(client):
    """Test crear nueva planta"""
    planta_data = {
        "codigo": "norte",
        "nombre": "Planta Norte",
        "ubicacion": "Sector Norte"
    }
    response = client.post("/api/plantas", json=planta_data)
    assert response.status_code == 201
    data = response.json()
    assert data["codigo"] == "norte"
    assert data["nombre"] == "Planta Norte"
    assert "id_planta" in data


def test_crear_planta_codigo_duplicado(client):
    """Test crear planta con código duplicado"""
    planta_data = {
        "codigo": "norte",
        "nombre": "Planta Norte",
        "ubicacion": "Sector Norte"
    }
    # Primera creación
    client.post("/api/plantas", json=planta_data)
    
    # Segunda creación con mismo código
    response = client.post("/api/plantas", json=planta_data)
    assert response.status_code == 400


def test_actualizar_planta(client):
    """Test actualizar planta"""
    # Crear planta
    planta_data = {
        "codigo": "sur",
        "nombre": "Planta Sur",
        "ubicacion": "Sector Sur"
    }
    response = client.post("/api/plantas", json=planta_data)
    id_planta = response.json()["id_planta"]
    
    # Actualizar
    update_data = {"nombre": "Planta Sur Actualizada"}
    response = client.put(f"/api/plantas/{id_planta}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Planta Sur Actualizada"


def test_eliminar_planta(client):
    """Test eliminar planta"""
    # Crear planta
    planta_data = {
        "codigo": "este",
        "nombre": "Planta Este",
        "ubicacion": "Sector Este"
    }
    response = client.post("/api/plantas", json=planta_data)
    id_planta = response.json()["id_planta"]
    
    # Eliminar
    response = client.delete(f"/api/plantas/{id_planta}")
    assert response.status_code == 200
    
    # Verificar que no existe
    response = client.get("/api/plantas")
    assert len(response.json()) == 0
