import asyncio
import re
from typing import Any

from microdot.microdot import Microdot, Request  # type: ignore[attr-defined]

from led.base import (
    WEB_PAGE_INDEX_IP,
    WEB_PAGE_INDEX_LED,
    WEB_PAGE_INDEX_WIFI,
    WEB_PAGES,
    WEB_PAGES_PATH,
    BaseDataService,
    BaseWebServer,
)

HTTP_OK = 200

METHOD_GET: str = "GET"
METHOD_POST: str = "POST"


def get_page_file_by_id(page_id: str) -> str:
    return f"{WEB_PAGES_PATH}/{WEB_PAGES.get(page_id)}"


def get_raw_page_content(page_id: str) -> str:
    with open(get_page_file_by_id(page_id), encoding="utf-8") as page:
        return page.read()


def get_page_content(page_id: str) -> tuple[str, int, dict[str, str]]:
    with open(get_page_file_by_id(page_id), encoding="utf-8") as page:
        html_content = page.read()
        return html_content, HTTP_OK, {"Content-Type": "text/html"}


def build_page_response(rendered_html_content: str) -> tuple[str, int, dict[str, str]]:
    return rendered_html_content, HTTP_OK, {"Content-Type": "text/html"}


def get_data_from_request(request: Request) -> dict[str, Any]:
    return {key: request.form.get(key, None) for key in request.form}


def replace_tag(raw_page: str, field: str, value: Any) -> str:  # noqa: ANN401
    return re.sub(rf"{{%\s*{field.lower()}\s*%}}", str(value), raw_page)


def render_page_using_data(raw_page: str, raw_data: dict) -> str:
    rendered = raw_page
    for field, value in raw_data.items():
        rendered = replace_tag(raw_page=rendered, field=field, value=value)
    return rendered


def merge_dictionaries(
    dict_alfa: dict[Any, Any], dict_beta: dict[Any, Any]
) -> dict[Any, Any]:
    merged: dict[Any, Any] = {}
    for dictionary in [dict_alfa, dict_beta]:
        merged.update(dictionary)

    return merged


async def process_page_repl(
    data_service: BaseDataService,
    page_id: str,
    invariant_rendering_data: dict[str, Any],
    request: Request,
) -> tuple[str, int, dict[str, str]]:
    raw_page_content: str = get_raw_page_content(page_id=page_id)

    if request.method == METHOD_POST:
        request_data: dict[str, Any] = get_data_from_request(request=request)
        rendering_data = merge_dictionaries(invariant_rendering_data, request_data)
        data_service.save_data(data=request_data)

    saved_data = data_service.get_data()
    rendering_data = merge_dictionaries(invariant_rendering_data, saved_data)
    rendered_page = render_page_using_data(
        raw_page=raw_page_content,
        raw_data=rendering_data,
    )

    return build_page_response(rendered_html_content=rendered_page)


class WebServer(BaseWebServer):

    def __init__(
        self,
        led_data_service: BaseDataService,
        wifi_data_service: BaseDataService,
        network_data_service: BaseDataService,
    ) -> None:
        self.app = Microdot()
        self.led_data_service = led_data_service
        self.wifi_data_service = wifi_data_service
        self.network_data_service = network_data_service

        @self.app.route("/led", methods=[METHOD_GET, METHOD_POST])
        async def led_page(
            request: Request,
        ) -> tuple[str, int, dict[str, str]]:
            return await process_page_repl(
                data_service=self.led_data_service,
                page_id=WEB_PAGE_INDEX_LED,
                invariant_rendering_data={"action": WEB_PAGE_INDEX_LED},
                request=request,
            )

        @self.app.route("/wifi", methods=[METHOD_GET, METHOD_POST])
        async def wifi_page(
            request: Request,
        ) -> tuple[str, int, dict[str, str]]:
            return await process_page_repl(
                data_service=self.wifi_data_service,
                page_id=WEB_PAGE_INDEX_WIFI,
                invariant_rendering_data={"action": WEB_PAGE_INDEX_WIFI},
                request=request,
            )

        @self.app.route("/ip", methods=[METHOD_GET])
        async def ip_page(
            request: Request,
        ) -> tuple[str, int, dict[str, str]]:
            return await process_page_repl(
                data_service=self.network_data_service,
                page_id=WEB_PAGE_INDEX_IP,
                invariant_rendering_data={},
                request=request,
            )

    async def startup(self) -> None:
        server = asyncio.create_task(self.app.start_server())
        await server
