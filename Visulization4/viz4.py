#!/usr/local/bin/python3

import datetime
import math

import pandas as pd
import bleach

from bokeh.io import vform, hplot
from bokeh.plotting import output_file, figure, show
from bokeh.models import ColumnDataSource, CustomJS, RadioButtonGroup
from bokeh.layouts import gridplot, Row, Column, WidgetBox
from bokeh.models import HoverTool, BoxZoomTool, PanTool, ResetTool


DATA = "DonaldTrump_facebook_statuses.csv"

output_file('viz4.html')

trump_df = pd.read_csv(DATA, index_col=0, parse_dates=True)
rawdate = trump_df.status_published.values
datetime = [datetime.datetime.strptime(d, '%m/%d/%Y %H:%M:%S') for d in rawdate]
responses = trump_df.num_reactions.values
likes = trump_df.num_likes.values
loves = trump_df.num_loves.values
wows = trump_df.num_wows.values
hahas = trump_df.num_hahas.values
sads = trump_df.num_sads.values
angrys = trump_df.num_angrys.values
comments = trump_df.num_comments.values
shares = trump_df.num_shares.values
status_message = [bleach.clean(x) for x in trump_df.status_message.values]
link = [bleach.linkify(x) for x in trump_df.status_link.values]
for i in range(len(responses)):
    derp = max(likes[i], loves[i], wows[i], hahas[i], sads[i], angrys[i])
    if derp != likes[i]:
        print('color me bro')
        print(i)

ys = {'likes': likes, 'loves': loves, 'wows': wows, 'hahas': hahas, 'sads': sads, 'angrys': angrys}
colour = {'likes': '#5C92FF', 'loves': '#F25268', 'wows': '#42423F', 'hahas': '#FED871', 'sads': '#83A9F0', 'angrys': '#ff0000'}


source = ColumnDataSource(
    data=dict(
        x=datetime,
        y=responses,
        likes=likes,
        loves=loves,
        wows=wows,
        hahas=hahas,
        sads=sads,
        angrys=angrys,
        comments=comments,
        shares=shares,
        date=rawdate,
        link=link,
        # comment=comment
        status=status_message
    )
)

hover = HoverTool(
    tooltips="""
        <div>
            <div><span style="font-size: 17px; font-weight: bold;">Datetime: @date</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Likes: @likes</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Loves: @loves</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Wows: @wows</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">HaHas: @hahas</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Sads: @sads</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Angrys: @angrys</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Comments: @comments</span></div>
            <div><span style="font-size: 17px; font-weight: bold;">Shares: @shares</span></div>
            <div style="width: 400px"><span style="font-size: 17px; font-weight: bold;" style="word-wrap: break-word;">Post: @status</span></div>
        </div>
    """
    # <div><span style="font-size: 8px; font-weight: bold;">Link: @link</span></div>
)

change = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['likes']
ger('change');
    """)



tools = [BoxZoomTool(), hover, PanTool(), 'reset']  # 'box_zoom,wheel_zoom,pan,reset,hover'
p = figure(title="Reactions to Trump's Facebook posts through 2016/10/17",
           x_axis_type='datetime', tools=tools, width=2000, height=1000)

p.scatter('x', 'y', source=source, size=20)
p.xaxis.axis_label = 'Datetime'
p.yaxis.axis_label = 'Total Reactions'

select_by_interaction = RadioButtonGroup(
    labels=["Total Responses", "Likes", "Loves", "Wows", "HaHas", "Sads", "Angrys", "Total Comments", "Total shares"],
    active=0,
    callback=change
)

show(
    Column(
        p,
        Row(
            WidgetBox(select_by_interaction),
        )
    )
)
