"""Tests de filtros para inspecciones a nivel de repositorio"""
from datetime import datetime, timedelta
from app.repositories.inspecciones import inspeccion_repository
from app.models import Planta, Naviera, Usuario, Inspeccion


def crear_datos_basicos(db):
    # Plantas
    p1 = Planta(codigo="P1", nombre="Planta 1")
    p2 = Planta(codigo="P2", nombre="Planta 2")
    db.add_all([p1, p2])
    db.commit()
    db.refresh(p1); db.refresh(p2)

    # Navieras
    n1 = Naviera(codigo="N1", nombre="Naviera 1")
    n2 = Naviera(codigo="N2", nombre="Naviera 2")
    db.add_all([n1, n2])
    db.commit()
    db.refresh(n1); db.refresh(n2)

    # Inspectores
    u1 = Usuario(nombre="Inspector 1", correo="i1@example.com", rol="inspector")
    u2 = Usuario(nombre="Inspector 2", correo="i2@example.com", rol="inspector")
    db.add_all([u1, u2])
    db.commit()
    db.refresh(u1); db.refresh(u2)

    # Inspecciones con fechas distintas
    ahora = datetime.now()
    i1 = Inspeccion(
        codigo="INS_A",
        numero_contenedor="CONT-001",
        id_planta=p1.id_planta,
        id_navieras=n1.id_navieras,
        id_inspector=u1.id_usuario,
        estado='pending',
        inspeccionado_en=ahora - timedelta(days=2)
    )
    i2 = Inspeccion(
        codigo="INS_B",
        numero_contenedor="CONT-002",
        id_planta=p1.id_planta,
        id_navieras=n2.id_navieras,
        id_inspector=u2.id_usuario,
        estado='approved',
        inspeccionado_en=ahora - timedelta(days=1)
    )
    i3 = Inspeccion(
        codigo="INS_C",
        numero_contenedor="CONT-003",
        id_planta=p2.id_planta,
        id_navieras=n1.id_navieras,
        id_inspector=u2.id_usuario,
        estado='rejected',
        inspeccionado_en=ahora
    )

    db.add_all([i1, i2, i3])
    db.commit()

    return {
        'plantas': (p1, p2),
        'navieras': (n1, n2),
        'usuarios': (u1, u2),
        'inspecciones': (i1, i2, i3),
    }


def test_filtrar_por_planta(db_session):
    data = crear_datos_basicos(db_session)
    p1, _ = data['plantas']

    items, total = inspeccion_repository.get_all(db_session, id_planta=p1.id_planta)
    assert total == 2
    assert all(i.id_planta == p1.id_planta for i in items)


def test_filtrar_por_naviera(db_session):
    data = crear_datos_basicos(db_session)
    n1, _ = data['navieras']

    items, total = inspeccion_repository.get_all(db_session, id_navieras=n1.id_navieras)
    assert total == 2
    assert all(i.id_navieras == n1.id_navieras for i in items)


def test_filtrar_por_inspector(db_session):
    data = crear_datos_basicos(db_session)
    u1, _ = data['usuarios']

    items, total = inspeccion_repository.get_all(db_session, id_inspector=u1.id_usuario)
    assert total == 1
    assert all(i.id_inspector == u1.id_usuario for i in items)


def test_filtrar_por_fecha(db_session):
    data = crear_datos_basicos(db_session)
    i1, i2, i3 = data['inspecciones']

    # Desde ayer -> debe traer i2 e i3
    desde = (i2.inspeccionado_en).isoformat()
    items, total = inspeccion_repository.get_all(db_session, fecha_desde=datetime.fromisoformat(desde))
    assert total == 2

    # Hasta ayer -> debe traer i1 e i2 (si i2 fue exactamente ayer)
    hasta = (i2.inspeccionado_en).isoformat()
    items, total = inspeccion_repository.get_all(db_session, fecha_hasta=datetime.fromisoformat(hasta))
    assert total >= 2
