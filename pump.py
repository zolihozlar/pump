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

    return {'flow': str(flow), 'pump_pressure': str(pump_pressure) }
