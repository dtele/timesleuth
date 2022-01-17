import matplotlib.pyplot as plt
import seaborn as sns
from numpy import array as np_arr
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from matplotlib.ticker import FuncFormatter,MultipleLocator
from sql_commands import Reader
from icons import Icon

db_obj=Reader(r'haskelldudes-main/src/dbname.sqlite')
df=db_obj.read_rows('2021-12-17')

df['sort_key']=[i.split('\\')[-1][:-4].capitalize() for i in df['exe_path']]
df=df.sort_values(by='sort_key',inplace=False)

path_icon={}
for i in df['exe_path'].unique():
    try:    
        path_icon[i]=Icon(i)
    except Exception as e:
        print(e,f"\n{i} is not a valid path.")
        pass
    
colors=sns.color_palette([i.dominant_color for i in path_icon.values()])

def offset_image(coord, img_obj, ax1_local):
    img=np_arr(img_obj.img_pil)
    im=OffsetImage(img)
    im.image.axes=ax1_local
    ab=AnnotationBbox(im, (0, coord),  xybox=(-30,0), frameon=False,
                        xycoords='data',  boxcoords="offset points", pad=0)
    ax1_local.add_artist(ab)

def label_to_hours(label, pos):
    return f'{int(label // 60)}h{int(label % 60)}m'


plt.figure(figsize=(10,5))

sns.set_theme(style='ticks',context='paper',font='arial')

ax1=sns.stripplot(data=df,y='exe_path',x='instance_time',hue='sort_key',palette=colors,linewidth=1.2,size=6.9)
ax1.set(xlabel='',ylabel='',xticklabels=[],yticklabels=[])
ax1.legend(loc='best', bbox_to_anchor=(1,0.5, 0.5, 0.5),frameon=True,title='Tasks')

ax2=sns.barplot(y='exe_path',x='runtime',data=df,dodge=False,palette=colors,saturation=0.69)
ax2.set(xlabel='Runtime',ylabel='',yticklabels=[])
#ax2.set_yticklabels([i for i in df['sort_key'].unique()], va='center', rotation=90)

ax2.xaxis.set_major_formatter(FuncFormatter(label_to_hours))
ax2.xaxis.set_major_locator(MultipleLocator(min(60, 15 * (df['runtime'].max() // 15))))

for i,j in enumerate(path_icon.values()):
    try: 
        offset_image(i,j,ax1)
    except Exception as e:
        print(e)

plt.subplots_adjust(left=0.079,right=0.683,top=0.964)

plt.show()
