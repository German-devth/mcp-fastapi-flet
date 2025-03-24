import asyncio
import flet as ft

def create_text_fields() -> tuple[ft.TextField, ft.TextField]:
    """
    Создаёт два текстовых поля: для ввода города и кода валюты
    Returns:
         Кортеж из двух TextField
    """
    city_field = ft.TextField(label="Enter city", autofocus=True, width=300)
    currency_field = ft.TextField(label="Enter currency code", value="USD", width=300)
    return city_field, currency_field

def create_buttons(page: ft.Page) -> tuple[ft.ElevatedButton, ft.ElevatedButton]:
    """
    Создаёт две кнопки: для получения данных и для перехода в админку FastAPI
    Args:
         page: Объект страницы Flet, чтобы назначить обработчик перехода
    Returns:
         Кортеж с кнопками (Get Data, Admin FastAPI)
    """
    def open_link(e):
        page.launch_url("http://127.0.0.1:8000/docs")
    admin_button = ft.ElevatedButton("Admin FastAPI", on_click=open_link)
    get_data_button = ft.ElevatedButton("Get Data")
    return get_data_button, admin_button

def create_labels() -> tuple[ft.Text, ft.Text]:
    """
    Создаёт два текстовых элемента для вывода обменного курса и погоды
    Returns:
         Кортеж из двух пустых Text
    """
    exchange_label = ft.Text("")
    weather_label = ft.Text("")
    return exchange_label, weather_label

def create_data_row(exchange_label: ft.Text, weather_label: ft.Text) -> ft.Row:
    """
    Собирает строку, содержащую обменный курс и данные о погоде
    Returns:
         Объект Row с заданными элементами
    """
    return ft.Row([exchange_label, weather_label],
                  alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

def create_news_column() -> ft.Column:
    """
    Создаёт колонку для вывода новостных заголовков
    Returns:
         Объект Column с автоматической прокруткой
    """
    return ft.Column(scroll=ft.ScrollMode.AUTO,
                     height=600,
                     horizontal_alignment=ft.CrossAxisAlignment.CENTER)

def create_layout(city_field: ft.TextField,
                  currency_field: ft.TextField,
                  buttons_row: ft.Row,
                  data_row: ft.Row,
                  news_container: ft.Container) -> list[ft.Control]:
    """
    Собирает общий макет страницы из основных компонентов
    Returns:
         Список компонентов (контейнеры), которые будут добавлены на страницу
    """
    container = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    container.controls = [
        city_field,
        currency_field,
        buttons_row,
        data_row,
    ]
    return [container, news_container]

async def type_text(target_text: str, label: ft.Text, page: ft.Page) -> None:
    """
    Последовательно отображает текст по символам в заданном элементе
    Args:
         target_text: Текст для показа
         label: Элемент, в котором отображается текст (уже добавлен на страницу)
         page: Объект страницы для обновления интерфейса
    Returns:
         None
    """
    label.value = ""
    label.update()

    for char in target_text:
        label.value += char
        label.update()
        await asyncio.sleep(0.01)
