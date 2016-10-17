#!/usr/local/bin/python3

import csv

from bokeh.plotting import output_file, figure, show, hplot
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
m_c = []



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
        return 255
    x = int(x)
    return max(0, min(x, 255))


def rgb2hex(rgb):
    r = clamp(rgb[0])
    g = clamp(rgb[1])
    b = clamp(rgb[2])
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def time_as_int(time):
    h,m,s = str.split(time, sep=':')
    val = ((int(h) % 6) * 60) + int(m) + (int(s)/60)
    return val


# read in file
with open(DATA, encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)#skip headings
    for line in reader:
        if line[1] != 'NA':
            x.append(time_as_int(line[0]))
            l.append(line[1])
            y.append(int(line[2]))
            w_c.append(rgb2hex((line[3], line[4], line[5])))
            w_n.append(line[6])
            s_c.append(rgb2hex((line[7], line[8], line[9])))
            s_n.append(line[10])

            m_c.append(rgb2hex((128, 128, 128))) # middle grey

# locations = set(l)
# print(locations)
# for location in locations:
#     index = [i for i, x in enumerate(l) if x == location]
#     print(l.index(location))

radii = [1 for x in range(len(w_c))]

source = ColumnDataSource({'x': [], 'y': [], 'width': [], 'height': []})

jscode="""
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        source.trigger('change');
    """

x_range = (min(x) - 10, max(x) + 10)
y_range = (min(y) - 10, max(y) + 10)

x_label = 'Time'
y_label = 'Luminosity (Lux)'


p1 = figure(title='Sky Colours', x_range=x_range, y_range=y_range,
            tools='box_zoom,wheel_zoom,pan,reset', plot_width=400, plot_height=800)
p1.scatter(x, y, radius=radii, fill_color=s_c, fill_alpha=0.6, line_color=None)

p1.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p1.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
p1.xaxis.axis_label = x_label
p1.yaxis.axis_label = y_label

p2 = figure(title='Chicago Sunrise Colours', x_range=x_range, y_range=y_range,
            tools='', plot_width=400, plot_height=800)
p2.scatter(x, y, radius=radii, fill_color=m_c, fill_alpha=0.6, line_color=None)
rect = Rect(x='x', y='y', width='width', height='height', fill_alpha=0.1,
            line_color='black', fill_color='black')
p2.add_glyph(source, rect)
p2.xaxis.axis_label = x_label
p2.yaxis.axis_label = y_label


p3 = figure(title='Water Colours', x_range=p1.x_range, y_range=p1.y_range,
            tools='box_zoom,wheel_zoom,pan,reset', plot_width=400, plot_height=800)
p3.scatter(x, y, radius=radii, fill_color=w_c, fill_alpha=0.6, line_color=None)

p3.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p3.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
p3.xaxis.axis_label = x_label
p3.yaxis.axis_label = y_label

layout = hplot(gridplot([[p1, p2, p3]]))
show(layout)

