from datetime import datetime
import pandas as pd
import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot,layout
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure, save, output_file, show
from bokeh.transform import transform
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.core.properties import value
from bokeh.palettes import Category20
# from bokeh.plotting import figure, output_file, show

df_temp = pd.read_csv('BitBucketDashboardInput.csv')

def Render_dashboard():
    # df_temp = pd.read_csv('BitBucketDashboardInput.csv')

    df1 =df_temp.groupby(['author']).size().reset_index().rename(index=str,columns={0:'commits'}).sort_values(by=['commits'], ascending=False).head(10)

    p1 = figure(x_range=list(df1['author']), plot_width=1200, plot_height=400, title="Top Committers of the Month",
               toolbar_location=None, tools="")

    p1.vbar(x=list(df1['author']), top=df1['commits'], width=0.9, color='#2171b5')

    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0
    p1.axis.major_label_text_font_size = "10pt"

    print(df_temp.columns)
    df2 =df_temp.groupby(['author','month-date']).size().reset_index().rename(index=str,columns={0:'commits'})
    source = ColumnDataSource(df2)
    colors = list(reversed(['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef']))
    mapper = LinearColorMapper(palette=colors, low=df2.commits.min(), high=df2.commits.max())

    p2 = figure(plot_width=1200, plot_height=400, title="Author Commits by Day",
               x_range=sorted(list(df2['month-date'].unique())), y_range=sorted(list(df2['author'].unique())),
               toolbar_location=None, tools="", x_axis_location="above")

    p2.rect(x="month-date", y="author", width=1, height=1, source=source, line_color=None, fill_color=transform('commits', mapper))

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d"))

    p2.add_layout(color_bar, 'right')

    p2.axis.axis_line_color = None
    p2.axis.major_tick_line_color = None
    p2.axis.major_label_text_font_size = "10pt"
    p2.axis.major_label_standoff = 0
    p2.xaxis.major_label_orientation = 1.0

    l = layout([[p1],[p2]], sizing_mode='stretch_both')

    html = file_html(l , CDN, "dashboard.html")

    Html_file= open("templates/dashboard.html","w")
    Html_file.write(html)
    Html_file.close()


def Repo_commits_by_date():
    df=df_temp.groupby(['repo','year_month_date'],as_index = False)['project'].count().pivot('year_month_date','repo').fillna(0)
    df.columns = df.columns.droplevel()
    df.index=pd.to_datetime(df.index, format='%Y-%m-%d', errors='ignore')
    colors=Category20[len(df.columns)]
    # output_file("templates/Repo_commits_by_date.html")

    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", title="Repo Commits by Date")

    for i in range(len(df.columns)):
        p.line(df.index, df[df.columns[i]], color=colors[i], alpha=0.5,legend=df.columns[i], line_width=4)
        p.circle(df.index, df[df.columns[i]], color=colors[i],legend=df.columns[i], size=8)

    html = file_html(p , CDN, "Repo_commits_by_date.html")

    Html_file= open("templates/Repo_commits_by_date.html","w")
    Html_file.write(html)
    Html_file.close()



def Author_commits_by_repo():
    df=df_temp.groupby(['repo','author'],as_index = False)['project'].count().pivot('author','repo').fillna(0)
    dict_commits={}
    for i in df.index:
        dict_commits[i]=df.loc[i].values.tolist()

    # output_file("templates/Author_commits_by_repo.html")

    # author_list = test2.columns.droplevel().values.tolist()
    author_list = df.index.tolist()
    repo_list = df.columns.droplevel().values.tolist()
    colors=Category20[len(author_list)]
    # colors = ["#c9d9d3", "#718dbf", "#e84d60"]

    data = dict_commits
    dict_commits['repo_list']=repo_list

    p = figure(x_range=repo_list, plot_height=500, plot_width=1000, title="Author contribution by Repo",
           toolbar_location=None, tools="")

    p.vbar_stack(author_list, x='repo_list', width=0.9,  source=data,color=colors,
                 legend=[value(x) for x in author_list])

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "center_left"
    p.legend.orientation = "vertical"

    html = file_html(p , CDN, "Author_commits_by_repo.html")

    Html_file= open("templates/Author_commits_by_repo.html","w")
    Html_file.write(html)
    Html_file.close()

    # show(p)
