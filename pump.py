import pandas as pd
import numpy as np
import seaborn as sns
import json

def sys_curve(flow, sys_k_factor, sys_static_head):
    return flow ** 2 / float(sys_k_factor) ** 2 + float(sys_static_head)

def main_pump(data):
    df_sys = pd.DataFrame(data=np.arange(0, 10001), columns=['flow'])

    df_sys['sys_k_factor'] = data['sys_k_factor']
    df_sys['sys_static_head'] = data['sys_static_head']

    df_sys['sys_pressure'] = 0.0
    df_sys['sys_pressure'] = df_sys.apply(lambda x: sys_curve(x['flow'], x['sys_k_factor'], x['sys_static_head']), axis=1)    
    del df_sys['sys_k_factor']
    del df_sys['sys_static_head']

    pump_data = []
    for key in data:
        if 'pump_' in key:
            pump_data.append([float(key.replace('pump_', '')), float(data[key])])

    df_pump = pd.DataFrame(data=pump_data, columns=['flow', 'pump_head'])

    df = df_sys.merge(df_pump, how='left', on='flow')
    df = df.interpolate(method ='linear', limit_direction ='forward') 
    df['pump_pressure'] = 0.098 * df['pump_head']

    df['delta'] = df['sys_pressure'] - df['pump_pressure']

    result = df[(df['delta'] == min(abs(df['delta']))) | (df['delta'] == -min(abs(df['delta'])))]

    flow = result['flow'].values[0]
    pump_pressure = result['pump_pressure'].values[0]

    # sns.lineplot(data=df, x="flow", y="sys_pressure")
    # sns.lineplot(data=df, x="flow", y="pump_pressure")


    import plotly
    import plotly.graph_objects as go

    # Create traces
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=df['flow'], y=df['sys_pressure'],
    #                     mode='lines',
    #                     name='lines'))
    # fig.add_trace(go.Scatter(x=df['flow'], y=df['pump_pressure'],
    #                     mode='lines',
    #                     name='lines'))

    html_chart = plotly.offline.plot({
        "data": [go.Scatter(x=df['flow'], y=df['sys_pressure'],
                        mode='lines',
                        name='Sys Pressure'), 
                go.Scatter(x=df['flow'], y=df['pump_pressure'],
                        mode='lines',
                        name='Pump Pressure')
                ],
        "layout": go.Layout(legend=dict(
                  orientation = "h",
                  yanchor="bottom",
                  y=-0.3,
                  xanchor="left",
                  x=0))
        
    }, include_plotlyjs=False, output_type='div')

    return {'flow': str(flow), 'pump_pressure': str(pump_pressure), 'html_chart': str(html_chart)}
