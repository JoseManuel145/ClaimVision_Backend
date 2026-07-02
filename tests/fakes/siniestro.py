"""Fakes compartidos del módulo Siniestro (usados por cliente, ajustador, taller, aseguradora)."""
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional, Tuple

from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel


class FakeSiniestroRepo:
    def __init__(self):
        self.items: dict[str, SiniestroModel] = {}

    def save(self, siniestro: SiniestroModel) -> SiniestroModel:
        self.items[siniestro.id] = siniestro
        return siniestro

    def get_by_id(self, id: str) -> Optional[SiniestroModel]:
        return self.items.get(id)

    def update(self, siniestro: SiniestroModel) -> SiniestroModel:
        self.items[siniestro.id] = siniestro
        return siniestro

    def list_by_aseguradora(self, aseguradora_id, offset=0, limit=20, estatus=None,
                            ajustador_id=None, taller_id=None, q=None) -> Tuple[List[SiniestroModel], int]:
        rows = [s for s in self.items.values() if s.aseguradora_id == aseguradora_id and s.deleted_at is None]
        if estatus is not None:
            rows = [s for s in rows if s.estatus == estatus]
        if ajustador_id is not None:
            rows = [s for s in rows if s.ajustador_id == ajustador_id]
        if taller_id is not None:
            rows = [s for s in rows if s.taller_id == taller_id]
        if q:
            ql = q.lower()
            rows = [s for s in rows if ql in (s.vehiculo_placas or "").lower()
                    or ql in (s.vehiculo_marca or "").lower() or ql in (s.vehiculo_modelo or "").lower()]
        total = len(rows)
        return rows[offset: offset + limit], total

    def list_by_cliente(self, cliente_id, offset=0, limit=20, estatus=None) -> Tuple[List[SiniestroModel], int]:
        rows = [s for s in self.items.values() if s.cliente_id == cliente_id and s.deleted_at is None]
        if estatus is not None:
            rows = [s for s in rows if s.estatus == estatus]
        total = len(rows)
        return rows[offset: offset + limit], total

    def list_by_ajustador(self, ajustador_id, offset=0, limit=20, estatus=None) -> Tuple[List[SiniestroModel], int]:
        rows = [s for s in self.items.values() if s.ajustador_id == ajustador_id and s.deleted_at is None]
        if estatus is not None:
            rows = [s for s in rows if s.estatus == estatus]
        total = len(rows)
        return rows[offset: offset + limit], total

    def list_by_taller(self, taller_id, offset=0, limit=20, estatus=None) -> Tuple[List[SiniestroModel], int]:
        rows = [s for s in self.items.values() if s.taller_id == taller_id and s.deleted_at is None]
        if estatus is not None:
            rows = [s for s in rows if s.estatus == estatus]
        total = len(rows)
        return rows[offset: offset + limit], total

    def update_estatus(self, siniestro_id: str, estatus: str) -> SiniestroModel:
        self.items[siniestro_id].estatus = estatus
        return self.items[siniestro_id]


class FakeImagenRepo:
    def __init__(self):
        self.items: List[ImagenSiniestroModel] = []

    def save(self, imagen: ImagenSiniestroModel) -> ImagenSiniestroModel:
        self.items.append(imagen)
        return imagen

    def get_by_siniestro_id(self, siniestro_id: str) -> List[ImagenSiniestroModel]:
        return [i for i in self.items if i.siniestro_id == siniestro_id and i.deleted_at is None]


class FakePeritajeRepo:
    def __init__(self):
        self.by_siniestro: dict[str, PeritajeAjustadorModel] = {}
        self.by_id: dict[str, PeritajeAjustadorModel] = {}

    def guardar_peritaje(self, peritaje: PeritajeAjustadorModel) -> PeritajeAjustadorModel:
        existing = self.by_siniestro.get(peritaje.siniestro_id)
        if existing:
            peritaje.id = existing.id
            peritaje.version = existing.version + 1
        if peritaje.created_at is None:
            peritaje.created_at = datetime.utcnow()
        peritaje.updated_at = datetime.utcnow()
        for d in peritaje.danos:
            d.peritaje_ajustador_id = peritaje.id
            if d.created_at is None:
                d.created_at = datetime.utcnow()
            if d.updated_at is None:
                d.updated_at = datetime.utcnow()
        self.by_siniestro[peritaje.siniestro_id] = peritaje
        self.by_id[peritaje.id] = peritaje
        return peritaje

    def obtener_peritaje_por_siniestro(self, siniestro_id: str):
        return self.by_siniestro.get(siniestro_id)

    def obtener_por_id(self, peritaje_id: str):
        return self.by_id.get(peritaje_id)

    def get_by_siniestro(self, siniestro_id: str):
        return self.by_siniestro.get(siniestro_id)


class FakeCotizacionRepo:
    def __init__(self):
        self.by_siniestro: dict[str, CotizacionTallerModel] = {}
        self.by_id: dict[str, CotizacionTallerModel] = {}

    def save(self, cotizacion: CotizacionTallerModel) -> CotizacionTallerModel:
        existing = self.by_siniestro.get(cotizacion.siniestro_id)
        if existing:
            cotizacion.id = existing.id
            cotizacion.version = existing.version + 1
        self.by_siniestro[cotizacion.siniestro_id] = cotizacion
        self.by_id[cotizacion.id] = cotizacion
        return cotizacion

    def get_by_siniestro(self, siniestro_id: str):
        return self.by_siniestro.get(siniestro_id)

    def get_by_id(self, id: str):
        return self.by_id.get(id)

    def update_estatus(self, id: str, estatus: str) -> CotizacionTallerModel:
        self.by_id[id].estatus = estatus
        return self.by_id[id]


class FakeAjustadorChecker:
    def __init__(self, validos: set[str]):
        self.validos = validos

    def existe_y_activo(self, ajustador_id: str) -> bool:
        return ajustador_id in self.validos


class FakeTallerChecker:
    def __init__(self, validos: set[str]):
        self.validos = validos

    def existe(self, taller_id: str) -> bool:
        return taller_id in self.validos


def make_cotizacion(cid="cot-1", siniestro_id="sin-t", taller_id="taller-1", estatus="Pendiente_Aprobacion") -> CotizacionTallerModel:
    now = datetime.utcnow()
    return CotizacionTallerModel(
        id=cid, siniestro_id=siniestro_id, taller_id=taller_id,
        monto_mano_obra=1000.0, monto_refacciones=2000.0, monto_total=3000.0,
        desglose_pdf_url="https://x/cot.pdf", estatus=estatus,
        observaciones_tecnicas=None, version=1, created_at=now, updated_at=now,
    )


def make_peritaje(siniestro_id="sin-t", ajustador_id="aj-profile-1") -> PeritajeAjustadorModel:
    now = datetime.utcnow()
    return PeritajeAjustadorModel(
        id="per-x", siniestro_id=siniestro_id, ajustador_id=ajustador_id,
        costo_definitivo_ajustador=12000.0, firma_digital_ajustador="firma",
        observaciones_campo=None, danos=[], version=1, created_at=now, updated_at=now,
    )


def make_siniestro(sid="sin-1", ajustador_id="aj-profile-1", estatus="Asignado_A_Ajustador", taller_id=None) -> SiniestroModel:
    now = datetime.utcnow()
    return SiniestroModel(
        id=sid, aseguradora_id="aseg-1", cliente_id="perfil-1",
        ajustador_id=ajustador_id, taller_id=taller_id, estatus=estatus,
        vehiculo_marca="Toyota", vehiculo_modelo="Corolla", vehiculo_anio=2020,
        vehiculo_placas="ABC-123", vehiculo_vin=None,
        latitud_siniestro=19.0, longitud_siniestro=-99.0,
        narracion_texto=None, narracion_audio_url=None,
        indicaciones_dano_interno=False, fecha_siniestro=now,
        version=1, created_at=now, updated_at=now,
    )
