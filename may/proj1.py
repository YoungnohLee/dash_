import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# 가상의 데이터 생성
np.random.seed(0)
data = {
    'X': np.arange(1, 101),
    'Y1': np.random.normal(0, 1, 100),
    'Y2': np.random.normal(1, 1, 100),
    'Y3': np.random.normal(2, 1, 100),
    'Y4': np.random.normal(3, 1, 100),
    'Y5': np.random.normal(4, 1, 100)
}
df = pd.DataFrame(data)

# Dash 앱 생성
app = dash.Dash(__name__)

# 레이아웃 생성
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Choose a Dataset:'),
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Y1', 'value': 'Y1'},
                    {'label': 'Y2', 'value': 'Y2'},
                    {'label': 'Y3', 'value': 'Y3'},
                    {'label': 'Y4', 'value': 'Y4'},
                    {'label': 'Y5', 'value': 'Y5'}
                ],
                value='Y1'
            ),
        ], className='six columns'),
        html.Div(id='left-plots', className='six columns'),
    ], className='row'),
    html.Div([
        html.Div(id='right-plots', className='six columns'),
    ], className='row'),
])

# 콜백 함수 생성
@app.callback(
    [dash.dependencies.Output('left-plots', 'children'),
     dash.dependencies.Output('right-plots', 'children')],
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_plots(selected_value):
    left_plots = []
    right_plots = []
    for plot_type in ['scatter', 'line']:
        if plot_type == 'scatter':
            plot_data = go.Scatter(x=df['X'], y=df[selected_value], mode='markers', name='Scatter Plot')
        elif plot_type == 'line':
            plot_data = go.Scatter(x=df['X'], y=df[selected_value], mode='lines', name='Line Plot')
        
        left_plots.append(
            dcc.Graph(
                id=f'{plot_type}-plot-left-{selected_value}',
                figure={'data': [plot_data], 'layout': go.Layout(title=f'{plot_type.capitalize()} Plot of {selected_value}')}
            )
        )
    
    for plot_type in ['bar', 'histogram', 'box']:
        if plot_type == 'bar':
            plot_data = go.Bar(x=df['X'], y=df[selected_value], name='Bar Plot')
        elif plot_type == 'histogram':
            plot_data = go.Histogram(x=df[selected_value], name='Histogram')
        elif plot_type == 'box':
            plot_data = go.Box(y=df[selected_value], name='Box Plot')

        right_plots.append(
            dcc.Graph(
                id=f'{plot_type}-plot-right-{selected_value}',
                figure={'data': [plot_data], 'layout': go.Layout(title=f'{plot_type.capitalize()} Plot of {selected_value}')}
            )
        )
        
    return left_plots, right_plots

# 앱 실행
if __name__ == '__main__':
    app.run_server(debug=True)
