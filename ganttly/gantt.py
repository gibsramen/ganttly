from typing import List
import warnings

import matplotlib.dates as mdates
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import seaborn as sns

from .task import Task


class Gantt:
    def __init__(self, format_: str = None):
        """Collection of tasks.

        :param format_: Formatting for dates, defaults to '%Y/%m/%d'
        :type format: str
        """
        self.format = format_ if format_ else "%Y/%m/%d"
        self.tasks = []

    def add_task(self, task: Task):
        """Add a single Task.

        :param task: Task to add to Gantt
        :type task: ganttly.task.Task
        """
        if not isinstance(task, Task):
            raise ValueError("task must be of type Task.")
        self.tasks.append(task)

    def add_tasks(self, tasks: List[Task]):
        """Add multiple Tasks.

        :param tasks: Tasks to add to Gantt
        :type task: List[ganttly.task.Task]
        """
        if not all([isinstance(x, Task) for x in tasks]):
            raise ValueError("All entries in tasks must be of type Task.")
        self.tasks += tasks

    def plot(
        self,
        frequency: str = None,
        interval: float = None,
        locator: mdates.RRuleLocator = None,
        facecolor: str = None,
        color_tag: str = None,
        palette: dict = None
    ) -> "GanttPlot":
        """Plot the Gantt chart.

        :param frequency: Grid frequency, one of 'day', 'week', 'month', or
            'year'
        :type param: str

        :param interval: Grid interval of frequency
        :type interval: float

        :param locator: Custom Locator to use for Gantt grid (optional)
        :type locator: matplotlib.dates.RRuleLocator

        :param facecolor: Color of Gantt bars (applied to all). This argument,
            if provided, will override 'color_tag' and 'palette'.
        :type facecolor: str

        :param color_tag: Tag to use for coloring
        :type color_tag: str

        :param palette: Dictionary of colors to use for each tag
        :type palette: Dict[str, str]
        """
        if locator is not None:
            if frequency is not None or interval is not None:
                warnings.warn(
                    "Locator provided - ignoring frequency and "
                    "interval arguments."
                )
        else:
            if frequency == "day":
                locator = mdates.DayLocator(interval=interval)
            elif frequency == "week":
                locator = mdates.DayLocator(interval=7*interval)
            elif frequency == "month":
                locator = mdates.MonthLocator(interval=interval)
            elif frequency == "year":
                locator == mdates.YearLocator(base=interval)
            else:
                raise ValueError(
                    "freqency must be one of 'day', 'week', 'month', or 'year'"
                )
        return GanttPlot(
            self,
            locator=locator,
            facecolor=facecolor,
            color_tag=color_tag,
            palette=palette
        )


class GanttPlot:
    def __init__(
        self, gantt: Gantt,
        locator: mdates.RRuleLocator,
        facecolor: str = None,
        color_tag: str = None,
        palette: dict = None
    ):
        """Visualization of Gantt chart.

        :param locator: Custom Locator to use for Gantt grid (optional)
        :type locator: matplotlib.dates.RRuleLocator

        :param facecolor: Color of Gantt bars (applied to all). This argument,
            if provided, will override 'color_tag' and 'palette'.
        :type facecolor: str

        :param color_tag: Tag to use for coloring
        :type color_tag: str

        :param palette: Dictionary of colors to use for each tag value
        :type palette: Dict[str, str]
        """
        self.gantt = gantt
        self.tasks = self.gantt.tasks
        self.num_tasks = len(self.tasks)
        self.locator = locator
        self.facecolor = facecolor
        self.color_tag = color_tag
        self.palette = palette

        self.fig, self.ax = plt.subplots(1, 1)

        if self.facecolor is None:
            if self.palette is None:
                self._get_palette()

            if self.palette:
                self._get_legend()

        for i, task in enumerate(self.tasks):
            self.ax.broken_barh(
                [(task.start, task.end - task.start)],
                (i, 1),
                linewidth=1,
                edgecolor="black",
                facecolor=(
                    facecolor or self.palette.get(task.tags.get(color_tag))
                )
            )

        self.ax.tick_params("x", labelsize="small")
        self.ax.tick_params("y", width=0, which="both")
        self.ax.grid(axis="both", which="major")
        self.ax.set_axisbelow(True)
        self.ax.xaxis.set_major_locator(self.locator)

        self.ax.set_yticks(range(self.num_tasks + 1))
        self.ax.set_yticklabels([])

        task_label_pos = [0.5 + i for i in range(self.num_tasks)]
        task_names = [task.name for task in self.tasks]
        self.ax.yaxis.set_minor_locator(FixedLocator(task_label_pos))
        self.ax.yaxis.set_ticklabels(task_names, minor=True)

    def _get_palette(self):
        if self.color_tag is None:  # Both color_tag and palette are None
            self.color_tag = ""
            self.palette = dict()
        else:
            if self.palette is None:
                uniq_vals = {task.tags[self.color_tag] for task in self.tasks}
                self.palette = dict(
                    zip(uniq_vals, sns.color_palette("muted", len(uniq_vals)))
                )

    def _get_legend(self):
        patches = []
        for tag, color in self.palette.items():
            _patch = Patch(
                edgecolor="black",
                facecolor=color,
                label=tag
            )
            patches.append(_patch)
        self.ax.legend(
            handles=patches,
            framealpha=0,
            ncol=len(self.tasks),
            loc="lower center",
            bbox_to_anchor=[0.5, 1],
            title=self.color_tag
        )
