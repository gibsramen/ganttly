import pandas as pd

from ganttly import Gantt, Task


def test_gantt():
    task1 = Task(
        "task1",
        pd.Timestamp("2020/01/01"),
        pd.Timestamp("2020/02/01")
    )

    task2 = Task(
        "task2",
        pd.Timestamp("2020/02/15"),
        pd.Timestamp("2020/03/25")
    )

    g = Gantt()
    g.add_tasks([task1, task2])

    t1 = g.tasks[0]
    t2 = g.tasks[1]

    assert t1.name == "task1"
    assert t2.name == "task2"
    assert t1.start == pd.Timestamp("2020/01/01")
    assert t1.end == pd.Timestamp("2020/02/01")
    assert t2.start == pd.Timestamp("2020/02/15")
    assert t2.end == pd.Timestamp("2020/03/25")

    g.plot(frequency="month", interval=1)
