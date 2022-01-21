from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.ticker import FuncFormatter, MultipleLocator
from numpy import array as np_arr
from seaborn import stripplot, barplot, color_palette, set_theme

from icons import Icon
from sql_commands import Reader


class GraphGenerator:
    def __init__(self, icons, instances, names, legend, num_bars, ax):
        self.icons = icons
        self.instances = instances
        self.names = names
        self.legend = legend
        self.ax = ax

        self.colors = 'mako'
        self.xcoord = -37 if icons and self.names else -27
        self.path_icon = {}
        self.strip_ax = ''

        self.db_obj = Reader(r'dbname.sqlite')
        self.df = self.db_obj.read_rows('2022-01-01')
        self.df['title'] = [i.split('\\')[-1][:-4] for i in self.df['exe_path']]
        self.df.sort_values(by='runtime', inplace=True, ascending=False)

        self.num_bars = min(num_bars, len(self.df['exe_path'].unique()))

        if self.icons:
            self.add_icons()

        self.df = self.df[self.df.runtime.isin(sorted(self.df.runtime.unique(), reverse=True)[:self.num_bars])]

        set_theme(style='ticks', context='paper', font='arial')

        if self.instances:
            self.add_instances()

        self.bar_ax = barplot(y='exe_path', x='runtime', data=self.df, dodge=False, palette=self.colors, saturation=0.69, hue='title', ax=self.ax)
        self.bar_ax.set(xlabel='', ylabel='', yticklabels=[])
        self.bar_ax.xaxis.set_major_formatter(FuncFormatter(self.label_to_hours))
        self.bar_ax.xaxis.set_major_locator(MultipleLocator(min(60, max(1, 15 * (self.df['runtime'].max() // 15)))))

        if self.legend:
            self.bar_ax.legend(loc='best', bbox_to_anchor=(1, 0.5, 0.5, 0.5), frameon=True, title='Tasks')
        else:
            self.bar_ax.legend(labels=[])

        if self.names:
            self.bar_ax.set_yticklabels([i for i in self.df['title'].unique()], va='center', rotation=90)

        try:
            for i, j in enumerate(self.path_icon.values()):
                self.offset_image(i, j, self.bar_ax, self.xcoord)
        except Exception as e:
            print(e)

    def add_icons(self):
        fail_lst = []
        for i in self.df['exe_path'].unique():
            try:
                self.path_icon[i] = Icon(i)
                assert self.path_icon[i].img_pil
            except Exception as e:
                fail_lst.append(i)
                print(e, f"\n{i} is not a valid path.")
                pass

        self.df.drop(self.df[self.df.exe_path.isin(fail_lst)].index, inplace=True)
        self.path_icon = {i: j for i, j in list(self.path_icon.items())[:self.num_bars]}
        self.colors = color_palette([i.dominant_color for i in self.path_icon.values()])

    def add_instances(self):
        self.strip_ax = stripplot(data=self.df, y='exe_path', x='instance_time', palette=self.colors, linewidth=1.2, size=6.9, ax=self.ax)
        self.strip_ax.set(xlabel='', ylabel='', xticklabels=[], yticklabels=[])

    def offset_image(self, coord, img_obj, ax1_local, xcoord):
        img = np_arr(img_obj.img_pil)
        im = OffsetImage(img)
        im.image.axes = ax1_local
        ab = AnnotationBbox(im, (0, coord), xybox=(xcoord, 0), frameon=False,
                            xycoords='data', boxcoords="offset points", pad=0)
        ax1_local.add_artist(ab)

    @staticmethod
    def label_to_hours(label, pos):
        return f'{int(label // 60)}h{int(label % 60)}m'
