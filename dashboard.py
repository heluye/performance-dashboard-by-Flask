from datetime import datetime
import pandas as pd
import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot,layout
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure, save
# from bokeh.sampledata.unemployment1948 import data
from bokeh.transform import transform
from bokeh.resources import CDN
from bokeh.embed import file_html


def Render_dashboard():
	df_temp = pd.read_csv('BitBucketDashboardInput.csv')

	df1 =df_temp.groupby(['author']).size().reset_index().rename(index=str,columns={0:'commits'}).sort_values(by=['commits'], ascending=False).head(10)

	# output_file("top commiter.html")
	p1 = figure(x_range=list(df1['author']), plot_width=1200, plot_height=400, title="Top Committers of the Month",
	           toolbar_location=None, tools="")

	p1.vbar(x=list(df1['author']), top=df1['commits'], width=0.9, color='#2171b5')

	p1.xgrid.grid_line_color = None
	p1.y_range.start = 0
	# p1.xaxis.axis_label_text_font_size = "20pt"
	p1.axis.major_label_text_font_size = "10pt"
	# show(p)


	df2 =df_temp.groupby(['author','month-date']).size().reset_index().rename(index=str,columns={0:'commits'})
		#works
	# output_file("commits_steak2.html")
	source = ColumnDataSource(df2)
	# this is the colormap from the original NYTimes plot
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

	# output_file("test.html")
	# column(p1, p2)
	# save(p)

	# grid = gridplot([p1, p2])

	l = layout([[p1],[p2]], sizing_mode='stretch_both')

	html = file_html(l , CDN, "dashboard.html")

	Html_file= open("templates/dashboard.html","w")
	Html_file.write(html)
	Html_file.close()
