#!/usr/local/bin/python3

import pandas as pd

from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    Circle
)
from bokeh.palettes import Purples8 as palette
from bokeh.plotting import figure

from bokeh.sampledata.us_counties import data as counties


DATA = 'voterreg.csv'

palette.reverse()

counties = {
    code: county for code, county in counties.items() if county["state"] == "mt"
}


voter_df = pd.read_csv(DATA, index_col=0, parse_dates=True)

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]
county_names = [county['name'] for county in counties.values()]

nxys = sorted(zip(county_names, county_xs, county_ys))
county_names, county_xs, county_ys = zip(*nxys)

county_rates = voter_df.percent.values
county_pops = voter_df.population.values
county_voters = voter_df.voters.values
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
    pop=county_pops,
    voters=county_voters
))

cities = ColumnDataSource(
    data=dict(
        lat=[46.8787],
        lon=[ 113.9966],
    )
)

TOOLS = "box_zoom,wheel_zoom,hover,save,reset"

p = figure(
    title="Montana Voter Registration as of 2016/10/31", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    width=1600, height=900
)
p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

# circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
# p.add_glyph(cities, circle)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Voter Registration Rate", "@rate"),
    ("Voters", "@voters"),
    ("Population", "@pop"),
]

show(p)
