import asyncio
import json
from datetime import timedelta

from fastapi import Form, APIRouter, Depends, HTTPException
from pydantic import ValidationError

from api.decorators import redis_cache
from api.depends import get_mcp_client, get_redis
from api.schemas import NewsResponse, ExchangeResponse, \
    WeatherResponse, FullDataResponse, WeatherData
from mcp_impl.client import MCPClient

router = APIRouter()

@router.post("/news", response_model=NewsResponse)
async def get_news(
    city = Form(..., description="Название города"),
    client = Depends(get_mcp_client)
) -> NewsResponse:
    try:
        response = await client.session.read_resource(f"news://{city}")
        news_info = json.loads(response.contents[0].text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500,
                            detail="Ошибка декодирования данных новостей")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Не удалось получить новости")
    return NewsResponse(news=news_info)

@router.post("/exchange", response_model=ExchangeResponse)
@redis_cache(timedelta(hours=1))
async def get_exchange(
    currency: str = Form(default="USD",
                         description="Код валюты (по умолчанию USD)"),
    client: MCPClient = Depends(get_mcp_client),
    redis = Depends(get_redis)
) -> ExchangeResponse:
    try:
        response = await client.session.read_resource(f"exchange://{currency}")
        exchange_info = response.contents[0].text
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Не удалось получить данные курса обмена")
    if not exchange_info:
        raise HTTPException(status_code=500,
                            detail="Пустой ответ от сервиса")
    return ExchangeResponse(exchange_rate=exchange_info)

@router.post("/weather", response_model=WeatherResponse)
@redis_cache(timedelta(hours=1))
async def get_weather(
    city = Form(..., description="Название города"),
    client = Depends(get_mcp_client),
    redis = Depends(get_redis)
) -> WeatherResponse:
    try:
        response = await client.session.read_resource(f"weather://{city}")
        weather_info = response.contents[0].text
        weather_data = json.loads(weather_info)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Не удалось получить данные погоды")
    try:
        validated_weather = WeatherData(**weather_data)
    except ValidationError as e:
        raise HTTPException(status_code=500,
                            detail="Неверный формат данных погоды")
    return WeatherResponse(weather=validated_weather)

@router.post("/full_data", response_model=FullDataResponse)
async def full_data(
    city = Form(..., description="Название города"),
    client: MCPClient = Depends(get_mcp_client),
    redis = Depends(get_redis)
) -> FullDataResponse:
    try:
        exchange_task = asyncio.create_task(
            get_exchange(currency="USD", client=client, redis=redis)
        )
        news_task = asyncio.create_task(
            get_news(city=city, client=client)
        )
        weather_task = asyncio.create_task(get_weather(
            city=city, client=client, redis=redis)
        )
        exchange_response, news_response, weather_response = await asyncio.gather(
            exchange_task, news_task, weather_task
        )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Не удалось получить набор данных")
    return FullDataResponse(
        city=city,
        exchange_rate=exchange_response["exchange_rate"],
        news=news_response.dict()["news"],
        weather=weather_response["weather"]
    )

