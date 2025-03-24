import asyncio
import flet as ft
from flet_impl.ui_elements import (
    create_text_fields,
    create_buttons,
    create_labels,
    create_data_row,
    create_news_column,
    create_layout,
    type_text
)
from flet_impl.api_functions import fetch_exchange, fetch_weather, fetch_news

async def main(page: ft.Page):
    page.title = "API Client"

    # Создаём элементы интерфейса
    city_field, currency_field = create_text_fields()
    get_data_button, admin_button = create_buttons(page)
    exchange_label, weather_label = create_labels()
    data_row = create_data_row(exchange_label, weather_label)
    news_column = create_news_column()

    # Контейнер для новостей
    news_container = ft.Container(
        content=news_column,
        alignment=ft.Alignment(0, 0)
    )

    async def get_data(e):
        city = city_field.value
        currency = currency_field.value

        # Параллельное выполнение запросов к API
        exchange_task = fetch_exchange(currency)
        weather_task = fetch_weather(city)
        news_task = fetch_news(city)
        exchange_response, weather_response, news_response = await asyncio.gather(
            exchange_task, weather_task, news_task
        )

        if exchange_response.status_code == 200:
            exchange_text = f"Exchange Rate ({currency}): {exchange_response.json().get('exchange_rate', 'N/A')}"
        else:
            exchange_text = "Failed to fetch exchange rate."
        await type_text(exchange_text, exchange_label, page)

        if weather_response.status_code == 200:
            weather_data = weather_response.json().get('weather', {})
            weather_text = f"Weather in {city}: {weather_data.get('temperature', 'N/A')}°C"
        else:
            weather_text = "Failed to fetch weather."
        await type_text(weather_text, weather_label, page)

        news_column.controls.clear()
        if news_response.status_code == 200:
            titles_list = news_response.json().get('news', [])
            for title in titles_list:
                label = ft.Text("")
                news_column.controls.append(label)
                page.update()
                await type_text(title, label, page)
        else:
            label = ft.Text("Failed to fetch news.")
            news_column.controls.append(label)
            page.update()

        page.update()

    get_data_button.on_click = get_data
    buttons_row = ft.Row(
        [get_data_button, admin_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    layout = create_layout(city_field, currency_field, buttons_row, data_row, news_container)
    for control in layout:
        page.add(control)

ft.app(target=main, view=ft.WEB_BROWSER)
