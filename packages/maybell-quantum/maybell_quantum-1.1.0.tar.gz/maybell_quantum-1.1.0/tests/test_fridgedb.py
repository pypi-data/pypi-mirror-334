import datetime
import os

import pytest

from maybell_quantum.fridgedb import FridgeDB
from maybell_quantum.fridgedb import TimeRange
from maybell_quantum.helpers import plot
from maybell_quantum.helpers import pretty_print_result
from maybell_quantum.mock_data_generator import load_mock_data


@pytest.fixture()
def fdb():

    interval = 0.1
    n_cycles = 10
    bucket = "mock_datadb"
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    token = os.environ["INFLUXDB_TOKEN"]
    org = "Maybell Quantum"

    load_mock_data(
        interval=interval,
        n_cycles=n_cycles,
        bucket=bucket,
        url=url,
        token=token,
        org=org,
    )

    yield FridgeDB(url=url, org=org, token=token, bucket=bucket)


def test_instantiation(fdb: FridgeDB):
    assert fdb is not None
    since = datetime.timedelta(minutes=1)
    result = fdb.last(since)
    print(result)


def test_simple_fetch(fdb: FridgeDB):
    stop_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = stop_time - datetime.timedelta(minutes=1)
    trange = TimeRange(start_time, stop_time)

    result = fdb.fetch(trange, ["mxp"])
    pretty_print_result(result)


def test_multiple_mixed_device_fetch(fdb: FridgeDB):
    stop_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = stop_time - datetime.timedelta(days=1)
    trange = TimeRange(start_time, stop_time)

    result = fdb.fetch(trange, ["pm1", "pm2", "mxp", "prp"])
    pretty_print_result(result)


def test_plot_generation(fdb: FridgeDB):
    stop_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = stop_time - datetime.timedelta(minutes=1)
    trange = TimeRange(start_time, stop_time)

    result = fdb.fetch(trange, ["mxp"])
    pretty_print_result(result)

    filename = "mxp_test_plot.png"
    plot(["mxp"], "temperature", result, saveas=filename)

    assert os.path.exists(filename)
    os.unlink(filename)
