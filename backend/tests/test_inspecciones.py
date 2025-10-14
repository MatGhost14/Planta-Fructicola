"""Tests para endpoints de inspecciones"""
import pytest
from datetime import datetime


@pytest.fixture
def planta_test(client):
    """Fixture para crear planta de prueba"""
    response = client.post("/api/plantas", json={
        "codigo": "test",
        "nombre": "Planta Test",
        "ubicacion": "Test"
    })
    return response.json()


@pytest.fixture
def naviera_test(client):
    """Fixture para crear naviera de prueba"""
    response = client.post("/api/navieras", json={
        "codigo": "test",
        "nombre": "Naviera Test"
    })
    return response.json()


@pytest.fixture
def usuario_test(client):
    """Fixture para crear usuario de prueba"""
    response = client.post("/api/usuarios", json={
        "nombre": "Inspector Test",
        "correo": "test@example.com",
        "rol": "inspector"
    })
    return response.json()


def test_crear_inspeccion(client, planta_test, naviera_test, usuario_test):
    """Test crear nueva inspección"""
    inspeccion_data = {
        "numero_contenedor": "TEST-1234567",
        "id_planta": planta_test["id_planta"],
        "id_navieras": naviera_test["id_navieras"],
        "id_inspector": usuario_test["id_usuario"],
        "temperatura_c": -18.5,
        "observaciones": "Inspección de prueba"
    }
    
    response = client.post("/api/inspecciones", json=inspeccion_data)
    assert response.status_code == 201
    data = response.json()
    assert "id_inspeccion" in data
    assert "codigo" in data
    assert data["codigo"].startswith("INS_")


def test_listar_inspecciones(client, planta_test, naviera_test, usuario_test):
    """Test listar inspecciones con paginación"""
    # Crear inspección
    inspeccion_data = {
        "numero_contenedor": "TEST-1234567",
        "id_planta": planta_test["id_planta"],
        "id_navieras": naviera_test["id_navieras"],
        "id_inspector": usuario_test["id_usuario"],
        "temperatura_c": -18.5
    }
    client.post("/api/inspecciones", json=inspeccion_data)
    
    # Listar
    response = client.get("/api/inspecciones")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] == 1


def test_obtener_inspeccion_detalle(client, planta_test, naviera_test, usuario_test):
    """Test obtener detalle de inspección"""
    # Crear inspección
    inspeccion_data = {
        "numero_contenedor": "TEST-1234567",
        "id_planta": planta_test["id_planta"],
        "id_navieras": naviera_test["id_navieras"],
        "id_inspector": usuario_test["id_usuario"],
        "temperatura_c": -18.5
    }
    response = client.post("/api/inspecciones", json=inspeccion_data)
    id_inspeccion = response.json()["id_inspeccion"]
    
    # Obtener detalle
    response = client.get(f"/api/inspecciones/{id_inspeccion}")
    assert response.status_code == 200
    data = response.json()
    assert data["numero_contenedor"] == "TEST-1234567"
    assert "planta" in data
    assert "naviera" in data
    assert "inspector" in data


def test_actualizar_inspeccion(client, planta_test, naviera_test, usuario_test):
    """Test actualizar inspección"""
    # Crear inspección
    inspeccion_data = {
        "numero_contenedor": "TEST-1234567",
        "id_planta": planta_test["id_planta"],
        "id_navieras": naviera_test["id_navieras"],
        "id_inspector": usuario_test["id_usuario"],
        "temperatura_c": -18.5
    }
    response = client.post("/api/inspecciones", json=inspeccion_data)
    id_inspeccion = response.json()["id_inspeccion"]
    
    # Actualizar
    update_data = {
        "temperatura_c": -19.0,
        "estado": "approved"
    }
    response = client.put(f"/api/inspecciones/{id_inspeccion}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["temperatura_c"] == -19.0
    assert data["estado"] == "approved"
