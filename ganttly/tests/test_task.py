from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from ganttly import Task


@pytest.fixture
def dt_times():
    start = datetime(2020, 7, 2)
    end = datetime(2020, 10, 3)
    return start, end


@pytest.fixture
def np_times():
    start = np.datetime64("2020-07-02")
    end = np.datetime64("2020-10-03")
    return start, end


@pytest.fixture
def pd_times():
    start = pd.Timestamp("2020/07/02")
    end = pd.Timestamp("2020/10/03")
    return start, end


@pytest.mark.parametrize("time", ["dt_times", "np_times", "pd_times"])
def test_init_task(time, request):
    start, end = request.getfixturevalue(time)
    task1 = Task("charmander", start, end)

    assert type(task1.start) == pd.Timestamp
    assert type(task1.end) == pd.Timestamp

    assert task1.start == pd.Timestamp("2020-07-02")
    assert task1.end == pd.Timestamp("2020-10-03")
    assert task1.name == "charmander"
