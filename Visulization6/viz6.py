#!/usr/local/bin/python3

import pandas as pd

from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    Slider,
    CheckboxGroup,
    Column,
    Row,
    CustomJS
)
from bokeh.palettes import Viridis256 as palette
from bokeh.plotting import figure

from bokeh.sampledata.us_counties import data as counties

# https://catalog.data.gov/dataset/violent-crimes-by-county-2006-to-2013-00616
DATA = 'Violent_Crimes_by_County__2006_to_2013.csv'

palette.reverse()

counties = {
    code: county for code, county in counties.items() if county["state"] == "md"
}


crime_df = pd.read_csv(DATA, index_col=0, parse_dates=True)

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]
county_names = [county['name'] for county in counties.values()]
percentChange = crime_df.pc20062013.values[:-1]
t2006 = crime_df.t2006.values[:-1]
t2007 = crime_df.t2007.values[:-1]
t2008 = crime_df.t2008.values[:-1]
t2009 = crime_df.t2009.values[:-1]
t2010 = crime_df.t2010.values[:-1]
t2011 = crime_df.t2011.values[:-1]
t2012 = crime_df.t2012.values[:-1]
t2013 = crime_df.t2013.values[:-1]


nxys = sorted(zip(county_names, county_xs, county_ys))
county_names, county_xs, county_ys = zip(*nxys)


color_mapper = LogColorMapper(palette=palette)
source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    percentChange=percentChange,
    t2006=t2006,
    t2007=t2007,
    t2008=t2008,
    t2009=t2009,
    t2010=t2010,
    t2011=t2011,
    t2012=t2012,
    t2013=t2013,
    data=t2013
))

TOOLS = "box_zoom,wheel_zoom,hover,save,reset"

p = figure(
    title="Maryland Violent Crim 2006 to 2013", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    width=1600, height=900
)
p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'data', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Percent Change 2006 2013", "@percentChange"),
    ("Current Year Total", "@data"),
    # ("2006 total", "@t2006"),
    # ("2007 total", "@t2007"),
    # ("2008 total", "@t2008"),
    # ("2009 total", "@t2009"),
    # ("2010 total", "@t2010"),
    # ("2011 total", "@t2011"),
    # ("2012 total", "@t2012"),
    # ("2013 total", "@t2013"),
]

code="""
        var data = source.get('data');
        var year = cb_obj.get('value');
        var replace = data['t'+year];
        for (i = 0; i < replace.length; i++) {{
            {var}[i] = replace[i] ;
            data['{var}'][i] = replace[i];
        }}
        source.trigger('change');
    """

slidercb = CustomJS(args=dict(source=source), code=code.format(var='data'))

slider = Slider(start=2006, end=2013, value=2013, step=1, title="year", callback=slidercb)

# checkbox = checkbox_group = CheckboxGroup(labels=["Percent Change"], active=[0])

show(Column(p, slider))
# show(Column(p, Row(checkbox, slider)))
