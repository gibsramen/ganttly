from typing import Union
from datetime import datetime

import numpy as np
import pandas as pd

Timepoint = Union[datetime, np.datetime64, pd.Timestamp, str]


class Task:
    def __init__(self, name: str, start: Timepoint, end: Timepoint):
        self.name = name
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)

        if self.start > self.end:
            raise ValueError("Start must come before end.")
