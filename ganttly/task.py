from typing import Union
from datetime import datetime

import numpy as np
import pandas as pd

Timepoint = Union[datetime, np.datetime64, pd.Timestamp, str]


class Task:
    def __init__(
        self,
        name: str,
        start: Timepoint,
        end: Timepoint,
        tag: str = None
    ):
        self.name = name
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.tag = tag

        if self.start > self.end:
            raise ValueError("Start must come before end.")

    def __str__(self) -> str:
        tag_str = self.tag if self.tag else ""
        return f"Task ({self.name}) [{tag_str}]: {self.start} - {self.end}"

    def __repr__(self) -> str:
        return self.__str__()
