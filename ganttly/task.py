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
        **tags
    ):
        """Individual task to be plotted on a Gantt chart.

        :param name: Name of task
        :type name: str

        :param start: Start time of this task
        :type start: Timepoint

        :param end: End time of this task
        :type end: Timepoint

        :param tags: Tags to apply to task for styling (optional)
        """
        self.name = name
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.tags = tags

        if self.start > self.end:
            raise ValueError("Start must come before end.")

    def to_dict(self):
        ret_dict = {
            "name": self.name,
            "start": self.start,
            "end": self.end
        }
        ret_dict.update({tag: value for tag, value in self.tags.items()})
        return ret_dict

    def __str__(self) -> str:
        tag_str = " "
        if self.tags is not None:
            tag_list = [f"{k}: {v}" for k, v in self.tags.items()]
            tag_str = f" [{','.join(tag_list)}] "
        return f"Task ({self.name}){tag_str}: {self.start} - {self.end}"

    def __repr__(self) -> str:
        return self.__str__()
