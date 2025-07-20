from unittest.mock import MagicMock

from led.web_server import (
    get_data_from_request,
    merge_dictionaries,
    render_page_using_data,
    replace_tag,
)
from microdot.microdot import MultiDict  # type: ignore[attr-defined]


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
