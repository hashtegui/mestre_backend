from fastapi import APIRouter, HTTPException

from src.config.database.connection import SessionDB
from src.domain.shared.tenant.schemas import TenantIn, TenantOut

from . import service

router = APIRouter()


@router.post("/", response_model=TenantOut)
async def create_tenant(tenant_in: TenantIn, session: SessionDB):
    tenant = await service.create_tenant(tenant_in, session)

    return tenant


@router.get("/")
async def get_tenants(session: SessionDB):
    tenants = await service.get_all_tenants(session)

    return tenants


@router.post("/{tenant_id}/create_schema")
async def create_schema(tenant_id: int, session: SessionDB):
    tenant = await service.get_tenant_by_id(tenant_id, session)
    if tenant is None:
        raise HTTPException(404, 'Tenant not found')
    await service.create_schema(tenant.schema_name)