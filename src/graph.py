import matplotlib.pyplot as plt
from seaborn import stripplot,barplot,color_palette,set_theme
from numpy import array as np_arr
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from matplotlib.ticker import FuncFormatter,MultipleLocator
from sql_commands import Reader
from icons import Icon


#reading from df
db_obj=Reader(r'haskelldudes-main/src/dbname.sqlite')
df=db_obj.read_rows('2021-12-17')


#sorting df based on runtime
df['title']=[i.split('\\')[-1][:-4].capitalize() for i in df['exe_path']]
df.sort_values(by='runtime',inplace=True,ascending=False)


#gui variables
icons=0
inst_plt=1
name=1
leg=0


#gui dependent variables not in func
colors='mako'
xcoord=-37 if icons and name else -27
path_icon={}
strip_ax=''


def add_icons():
    global path_icon, df, colors
    fail_lst=[]
    for i in df['exe_path'].unique():
        try:    
            path_icon[i]=Icon(i)
            assert path_icon[i].img_pil
        except Exception as e:
            fail_lst.append(i)
            print(e,f"\n{i} is not a valid path.")
            pass

    df.drop(df[df.exe_path.isin(fail_lst)].index,inplace=True)
    path_icon={i:j for i,j in list(path_icon.items())[:num]}
    colors=color_palette([i.dominant_color for i in path_icon.values()])


def add_instances():
    global strip_ax
    strip_ax=stripplot(data=df,y='exe_path',x='instance_time',palette=colors,linewidth=1.2,size=6.9)
    strip_ax.set(xlabel='',ylabel='',xticklabels=[],yticklabels=[])


def offset_image(coord, img_obj, ax1_local, xcoord):
    img=np_arr(img_obj.img_pil)
    im=OffsetImage(img)
    im.image.axes=ax1_local
    ab=AnnotationBbox(im, (0, coord),  xybox=(xcoord,0), frameon=False,
                        xycoords='data',  boxcoords="offset points", pad=0)
    ax1_local.add_artist(ab)


def label_to_hours(label, pos):
    return f'{int(label // 60)}h{int(label % 60)}m'


num=int(input("No. of bars to show: "))
if num>len(df['exe_path'].unique()): num=len(df['exe_path'].unique())

if icons: add_icons()

df=df[df.runtime.isin(sorted(df.runtime.unique(),reverse=True)[:num])]


plt.figure(figsize=(10,5))

set_theme(style='ticks',context='paper',font='arial')

if inst_plt: add_instances()

bar_ax=barplot(y='exe_path',x='runtime',data=df,dodge=False,palette=colors,saturation=0.69,hue='title')
bar_ax.set(xlabel='Runtime',ylabel='',yticklabels=[])
bar_ax.xaxis.set_major_formatter(FuncFormatter(label_to_hours))
bar_ax.xaxis.set_major_locator(MultipleLocator(min(60, max(1, 15 * (df['runtime'].max() // 15)))))

if leg:
    bar_ax.legend(loc='best', bbox_to_anchor=(1,0.5, 0.5, 0.5),frameon=True,title='Tasks')
else:    
    bar_ax.legend(labels=[])

if name: bar_ax.set_yticklabels([i for i in df['title'].unique()], va='center', rotation=90)

try:
    for i,j in enumerate(path_icon.values()):
        offset_image(i,j,bar_ax,xcoord)
except Exception as e:
        print(e)

plt.subplots_adjust(left=0.079,right=0.683,top=0.964)

plt.show()
