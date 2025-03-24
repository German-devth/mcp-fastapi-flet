from typing import List
from pydantic import BaseModel

class NewsResponse(BaseModel):
    news: List[str]

class ExchangeResponse(BaseModel):
    exchange_rate: str

class WeatherData(BaseModel):
    city: str
    temperature: float
    description: str

class WeatherResponse(BaseModel):
    weather: WeatherData

class FullDataResponse(BaseModel):
    city: str
    exchange_rate: str
    news: List[str]
    weather: WeatherData
