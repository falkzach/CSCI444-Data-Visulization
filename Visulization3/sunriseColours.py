#!/usr/local/bin/python3

import csv
import datetime

from bokeh.plotting import output_file, figure, show
from bokeh.models import ColumnDataSource, CustomJS, Rect
from bokeh.layouts import gridplot

DATA="data.csv"
output_file('chicago_sunrise_colours.html')

x = [] # time as int
l = [] # location
y = [] #luminosity as int
w_c = []
w_n = []
s_c = []
s_n = []

x_l = {}
y_l = {}
c_l = {
    'Argyle ':  '#FF0000',
    'Berwyn':   '#FFFF00',
    'Wilson':   '#008000',
    'Thorndale':    '#800080',
    'Bryn Mawr':    '#0000FF'
}

# read data
# 0 time
# 1 location
# 2 illuminance_lux
# 3 water_R
# 4 water_G
# 5 water_B
# 6 water_name
# 7 sky_R
# 8 sky_G
# 9 sky_B
# 10 sky_name
#


def clamp(x):
    if x == 'NA':
        return 0
    return max(0, min(int(x), 255))


def rgb2hex(rgb):
    r = clamp(rgb[0])
    g = clamp(rgb[1])
    b = clamp(rgb[2])
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def time_as_time(time):
    d = datetime.datetime.strptime('2016/10/03 ' + time, '%Y/%m/%d %I:%M:%S')
    return d


def indexes_at(data, key):
    return [i for i, x in enumerate(data) if x == key]


def sublist(data, indexes):
    return [data[index] for index in indexes]


# read in file
with open(DATA, encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)#skip headings
    for line in reader:
        if line[1] != 'NA':
            x.append(time_as_time(line[0]))
            l.append(line[1])
            y.append(int(line[2]))
            w_c.append(rgb2hex((line[3], line[4], line[5])))
            w_n.append(line[6])
            s_c.append(rgb2hex((line[7], line[8], line[9])))
            s_n.append(line[10])


locations = set(l)
for location in locations:
    index = indexes_at(l, location)
    x_l[location] = sublist(x, index)
    y_l[location] = sublist(y, index)

source = ColumnDataSource({'x': [], 'y': [], 'width': [], 'height': []})

jscode="""
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        source.trigger('change');
    """

x_label = 'Time'
y_label = 'Luminosity (Lux)'
size = 10


p1 = figure(title='Sky Colours', x_axis_type='datetime',
            tools='box_zoom,wheel_zoom,pan,reset,hover', plot_width=500, plot_height=800, background_fill_color='black')
p1.scatter(x, y, size=size, fill_color=s_c, fill_alpha=0.6, line_color=None)

p1.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p1.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
p1.xaxis.axis_label = x_label
p1.yaxis.axis_label = y_label


p2 = figure(title='Chicago Sunrise Colours along the Red Line', x_axis_type='datetime',
            tools='', plot_width=500, plot_height=800, background_fill_color='black',)
for location in locations:
    p2.scatter(x_l[location], y_l[location], size=size,
               fill_color=c_l[location], fill_alpha=0.6,
               line_color=None, legend=location)
rect = Rect(x='x', y='y', width='width', height='height', fill_alpha=0.1,
            line_color='orange', fill_color='white')
p2.add_glyph(source, rect)
p2.xaxis.axis_label = x_label
p2.yaxis.axis_label = y_label
p2.legend.location = 'top_left'


p3 = figure(title='Water Colours', x_range=p1.x_range, y_range=p1.y_range, x_axis_type='datetime',
            tools='box_zoom,wheel_zoom,pan,reset,hover', plot_width=500, plot_height=800, background_fill_color='black')
p3.scatter(x, y, size=size, fill_color=w_c, fill_alpha=0.6, line_color=None)

p3.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p3.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
p3.xaxis.axis_label = x_label
p3.yaxis.axis_label = y_label


layout = gridplot([[p1, p2, p3]])
show(layout)

