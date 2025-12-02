from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from led.web_server import (
    WebServer,
    build_html_page_response,
    get_data_from_request,
    get_page_file_by_id,
    get_raw_page_content,
    merge_dictionaries,
    render_page_using_data,
    replace_tag,
)
from microdot.microdot import MultiDict  # type: ignore[attr-defined]

DATA_PAGE = Path(__file__).parent / "data" / "pages"
EXAMPLE_PAGE = DATA_PAGE / "example-page.html"


def test_get_page_by_id() -> None:
    assert (
        get_page_file_by_id(
            "beta", web_pages={"alfa": "alfa.html", "beta": "beta.html"}
        )
        == "./web/beta.html"
    )
    assert get_page_file_by_id("ip") == "./web/ip.html"


def test_get_raw_page_content() -> None:
    assert (
        get_raw_page_content(page_file=str(EXAMPLE_PAGE))
        == "<!DOCTYPE html><html><body>Example</body></html>"
    )


def test_build_html_page_response() -> None:
    assert build_html_page_response(
        rendered_html_content="<!DOCTYPE html><html><body>Example</body></html>"
    ) == (
        "<!DOCTYPE html><html><body>Example</body></html>",
        200,
        {"Content-Type": "text/html"},
    )


def test_replace_tag() -> None:
    assert (
        replace_tag("<p>{% my-field %}</p>", "My-FIeLD", "Hello, World!")
        == "<p>Hello, World!</p>"
    )


def test_merge_dictionaries() -> None:
    assert merge_dictionaries({}, {"number_of_flashes": ["3"]}) == {
        "number_of_flashes": ["3"]
    }


def test_get_data_from_request() -> None:
    request = MagicMock()
    request.form = MultiDict({"number_of_flashes": "3"})

    assert get_data_from_request(request=request) == {"number_of_flashes": "3"}


def test_render_page_using_data() -> None:
    raw_page = (
        "<input "
        'type="number" '
        'name="number_of_flashes" '
        'id="number_of_flashes" '
        'value="{%   number_of_flashes   %}">'
    )
    rendering_data = {"number_of_flashes": ["3"]}
    assert (
        render_page_using_data(raw_page=raw_page, raw_data=rendering_data)
        == '<input type="number" name="number_of_flashes" id="number_of_flashes" value="[\'3\']">'
    )


async def test_web_server_init() -> None:
    mock_app_class = MagicMock()
    mock_start_server = AsyncMock()
    mock_app_instance = MagicMock()
    mock_app_instance.start_server = mock_start_server
    mock_app_class.return_value = mock_app_instance

    web_server = WebServer(
        led_data_service=MagicMock(),
        wifi_data_service=MagicMock(),
        network_data_service=MagicMock(),
        app_class=mock_app_class,
    )

    await web_server.startup()

    mock_start_server_calls = list(mock_start_server.mock_calls)
    assert len(mock_start_server_calls) == 1
