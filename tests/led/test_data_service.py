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

        assert ds.get_data() == example_data
