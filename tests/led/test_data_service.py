from pathlib import Path
from tempfile import TemporaryDirectory

from led.data_service import DataService


def test_data_service_basic_workflow() -> None:
    with TemporaryDirectory() as data_dir:
        data_file = Path(data_dir) / "data.txt"

        ds = DataService(data_file=str(data_file), logger=lambda _: None)

        example_data = {"name": "ettore", "age": 52}

        ds.save_data(example_data)

        with open(data_file) as dbfile:
            assert dbfile.read() == str(example_data).replace("'", '"')

        retrieved_data = ds.get_data()

        assert retrieved_data == example_data
        assert type(retrieved_data["name"]) is str
        assert type(retrieved_data["age"]) is int


def test_data_service_data_types_are_respected() -> None:
    with TemporaryDirectory() as data_dir:
        data_file = Path(data_dir) / "data.txt"

        ds = DataService(data_file=str(data_file), logger=lambda _: None)

        example_data = {
            "name": "ettore",
            "age": 52,
            "favourite_number": 3.1415,
        }

        ds.save_data(example_data)
        retrieved_data = ds.get_data()

        assert retrieved_data == example_data

        assert type(retrieved_data["name"]) is str
        assert type(retrieved_data["age"]) is int
        assert type(retrieved_data["favourite_number"]) is float


def test_cast_data_to_model() -> None:
    example_target_data = {
        "name": "ettore",
        "age": 52,
        "favourite_number": 3.1415,
    }
    actual_input_data = {
        "name": "ettore",
        "age": "52",
        "favourite_number": "3.1415",
    }
    model = {
        "age": int,
        "favourite_number": float,
    }
    assert (
        DataService.cast_data_to_model(data=actual_input_data, model=model)
        == example_target_data
    )
