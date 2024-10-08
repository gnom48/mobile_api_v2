from fastapi import APIRouter, HTTPException, Header
from .models import UserKpiLevels
from api.app.repository import Repository
from .jwt import verify_jwt_token


router_statistics = APIRouter(prefix="/user/statistics", tags=["Статистика"])

    
@router_statistics.get("/get", status_code=200)
async def user_statistics_get(period: str, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await verify_jwt_token(token_authorization)
    res = await Repository.get_statistics_by_period(user.id, period)
    return res


@router_statistics.get("/get_kpi", status_code=200)
async def user_statistics_get_with_kpi(token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await verify_jwt_token(token_authorization)
    last_month_kpi = await Repository.get_statistics_with_kpi(user.id)
    current_month_kpi = await Repository.get_current_kpi(user)
    if current_month_kpi is None:
        return { "last_month_kpi": last_month_kpi, "current_month_kpi": None, "level": None, "summary_deals_rent": None, "summary_deals_sale": None }
    return { 
        "last_month_kpi": last_month_kpi, 
        "current_month_kpi": current_month_kpi["kpi"],
        "level": current_month_kpi["level"], 
        "summary_deals_rent": current_month_kpi["deals_rent"], 
        "summary_deals_sale": current_month_kpi["deals_sale"] 
    }


@router_statistics.put("/update", status_code=200)
async def user_statistics_update(statistic: str, addvalue: int, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await verify_jwt_token(token_authorization)
    res = await Repository.update_statistics(user.id, statistic, addvalue)
    return res


@router_statistics.put("/move_kpi_level", status_code=200)
async def user_statistics_kpi_move(level: UserKpiLevels, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await verify_jwt_token(token_authorization)
    res = await Repository.update_kpi_level(user.id, level)
    if res == None:
        raise HTTPException(status_code=401, detail="move level error")
    return res