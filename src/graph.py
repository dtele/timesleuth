from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.ticker import FuncFormatter, MultipleLocator
from numpy import array as np_arr
from seaborn import stripplot, barplot, color_palette, set_theme

from icons import Icon
from sql_commands import Reader


class GraphGenerator:
    """
    A class to handle generation of the graph.
    """

    def __init__(self, icons: bool, instances: bool, legend: bool, names: bool, num_bars: int, date_start: str, date_end: str, path: str, ax):
        """
        :param icons: specifies whether icons to be on graph
        :param instances: specifies whether instances to be plotted
        :param legend: specifies whether legend to be present on graph
        :param names: specifies whether process names to be on graph
        :param num_bars: number of processes to be plotted
        :param date_start: lower range of timeframe read from
        :param date_end: upper range of timeframe read from
        :param path: absolute path of database 
        :param ax: matplotlib Axes object to draw plot onto
        """
        self.icons = icons
        self.instances = instances
        self.legend = legend
        self.names = names
        self.ax = ax

        self.colors = 'flare'
        self.xcoord = -37 if icons and self.names else -27
        self.path_icon = {}
        self.strip_ax = ''

        """
        Reads the DataFrame object from the database based on a date range.
        Adds DataFrame column with process name and sorting by runtime.
        """
        self.db_obj = Reader(path)
        self.df = self.db_obj.read_rows(date_start, date_end)
        self.df['title'] = [i.split('\\')[-1][:-4] for i in self.df['exe_path']]
        self.df.sort_values(by='runtime', ascending=False, inplace=True)

        self.num_bars = min(num_bars, len(self.df['exe_path'].unique()))

        """
        Creates icon objects if needed.
        Splitting DataFrame based on number of bars.
        Sets the graph theme.
        Adds plots of process instances.
        """
        if self.icons:
            self.icon_create()

        self.df = self.df[self.df.runtime.isin(sorted(self.df.runtime.unique(), reverse=True)[:self.num_bars])]

        set_theme(context='paper', style='ticks', font='arial')

        if self.instances:
            self.add_instances()

        """
        Creates the barplot along with graph tick styles.
        Adds legend or names if specified.
        Sets xticklabels and yticklabels colors.
        Adds icons to graph, fails if not specified
        """
        self.bar_ax = barplot(data=self.df, x='runtime', y='exe_path', hue='title', palette=self.colors, saturation=0.8,
                              dodge=False, ax=self.ax)
        self.bar_ax.set(xlabel='', ylabel='', yticklabels=[])
        self.bar_ax.xaxis.set_major_formatter(FuncFormatter(self.label_to_hours))
        self.bar_ax.xaxis.set_major_locator(MultipleLocator(min(60, max(1, 15 * (self.df['runtime'].max() // 15)))))

        if self.legend:
            self.bar_ax.legend(loc='lower right', frameon=True, title='')
        else:
            self.bar_ax.legend([], [], frameon=False)

        if self.names:
            self.bar_ax.set_yticklabels([i for i in self.df['title'].unique()], va='center', rotation=90)

        for label in [*self.bar_ax.get_yticklabels(), *self.bar_ax.get_xticklabels()]:
            label.set_color('#C9C9C9')

        try:
            for i, j in enumerate(self.path_icon.values()):
                self.offset_image(i, j, self.bar_ax, self.xcoord)
        except Exception as e:
            print(e)

    def icon_create(self) -> None:
        """
        Creates path and icon object dict along with color palette based on most dominant color.
        Also rearranges DataFrame based on failed icon extraction.
        """
        fail_lst = []
        for path in self.df['exe_path'].unique():
            try:
                self.path_icon[path] = Icon(path)
                assert self.path_icon[path].img_pil
            except Exception as e:
                fail_lst.append(path)
                print(e, f"\n{path} is not a valid path.")
                pass

        self.df.drop(self.df[self.df.exe_path.isin(fail_lst)].index, inplace=True)
        self.path_icon = {i: j for i, j in list(self.path_icon.items())[:self.num_bars]}
        self.colors = color_palette([i.dominant_color for i in self.path_icon.values()])

    def add_instances(self) -> None:
        """
        Adds plots of all instances of the process in the DataFrame to the graph.
        """
        self.strip_ax = stripplot(data=self.df, x='instance_time', y='exe_path', palette=self.colors, size=6.9,
                                  linewidth=1.2, ax=self.ax)
        self.strip_ax.set(xlabel='', xticklabels=[], ylabel='', yticklabels=[])

    def offset_image(self, coord, icon, ax_local, xcoord) -> None:
        """
        Adds pil object container of icons extracted to the graph.

        :param coord: y-axis position for image
        :param icon: icon object to be added to graph
        :param ax_local: matplotlib Axes to add icons on
        :param xcoord: x-axis spacing of icons from y-axis
        """
        img_arr = np_arr(icon.img_pil)
        img_con = OffsetImage(img_arr)
        img_con.image.axes = ax_local
        con_pos = AnnotationBbox(img_con, (0, coord), xybox=(xcoord, 0), xycoords='data',
                                 boxcoords="offset points", frameon=False, pad=0)
        ax_local.add_artist(con_pos)

    @staticmethod
    def label_to_hours(label, pos) -> str:
        """
        Formats the runtime to hhmm format for graph xticklabels.

        :param label: runtime value of process
        """
        return f'{int(label // 60)}h{int(label % 60)}m'
