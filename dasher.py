import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX], title="Stock Analysis Dashboard")

# Function to shorten text with ellipsis
def shorten_text(text, max_len=40):
    return text if len(text) <= max_len else text[:max_len-3] + " ..."

# Database connection (replace with your actual path)
conn = sqlite3.connect('C:/Users/anubh/Programs/Sunyata OU Internship Assignment/stock_data.db')
df = pd.read_sql_query("SELECT * FROM stock_data", conn)

# Mapping of metrics to human-readable labels
human_labels = {
    'close_price': 'Closing Price',
    'daily_return': 'Daily Return',
    'moving_avg': 'Moving Average',
    'rsi': 'Relative Strength Index (RSI)',
    'macd': 'Moving Average Convergence Divergence (MACD)',
    'upper_band': 'Upper Bollinger Band',
    'lower_band': 'Lower Bollinger Band',
}

# Mapping of tickers to company names (replace with your actual mapping)
ticker_to_name = {
    'AAPL': 'Apple Inc. (AAPL)',
    'GOOGL': 'Alphabet Inc. (GOOGL)',
    'MSFT': 'Microsoft Corporation (MSFT)',
    # Add more as needed
}

# Calculate correlation matrix for heatmap
correlation_matrix = df.pivot(index='date', columns='ticker', values='close_price').corr()

# Create heatmap using Plotly
heatmap_fig = px.imshow(correlation_matrix,
                        labels=dict(x="Ticker", y="Ticker", color="Correlation"),
                        x=correlation_matrix.columns,
                        y=correlation_matrix.index,
                        zmin=-1,
                        zmax=1)

# Main layout
app.layout = dbc.Container([
    html.Div([
        html.H1("Stock Analysis Dashboard", style={"fontSize": "36px", "fontFamily": "Open Sans, sans-serif"})
    ], style={"margin-bottom": "20px", "margin-top": "20px", "textAlign": "center"}),  # Centering title vertically and horizontally
    
    html.Hr(),  # Horizontal Rule
    
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            dbc.Row([
                dbc.Col(width={"size": 2}),  # Adjusted empty column for centering
                dbc.Col([
                    dcc.Dropdown(
                        id='stock-dropdown',
                        options=[{'label': shorten_text(ticker_to_name.get(i, i)), 'value': i} for i in df['ticker'].unique()],
                        value=df['ticker'].iloc[0],
                        style={"fontFamily": "Open Sans, sans-serif", "borderRadius": "12px"}  # Rounded corners
                    ),
                ], width={"size": 4}),  # Adjusted column size
                dbc.Col([
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[{'label': shorten_text(human_labels[i]), 'value': i} for i in human_labels.keys()],
                        value='close_price',
                        style={"fontFamily": "Open Sans, sans-serif", "borderRadius": "12px"}  # Rounded corners
                    ),
                ], width={"size": 4}),  # Adjusted column size
                dbc.Col(width={"size": 2})  # Adjusted empty column for centering
            ], style={"margin-bottom": "30px"}),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='line-plot')
                ])
            ], style={"margin-bottom": "30px"}),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3('Stock Correlation Heatmap'),
                        dcc.Graph(id='heatmap_revised', figure=heatmap_fig)
                    ])
                ], width={"size": 6}),
                
                dbc.Col([
                    html.Div([
                        html.H3('How to Interpret this Heatmap'),
                        html.Div(style={"height": "20px"}), # Vertical space
                        html.P('Correlation determines how similar the trends of entities are. The heatmap is plotted with the Daily Closing Prices of the Stocks as the trend.'),
                        html.P('Correlation values range from -1 to 1.'),
                        html.P('1 represents a Perfect positive correlation'),
                        html.P('0 represents No correlation'),
                        html.P('-1 represents Perfect negative correlation'),
                        html.P('Example 1: If Stock A and Stock B have a correlation of 0.9, they move in a very similar direction.'),
                        html.P('Example 2: If Stock A and Stock B have a correlation of -0.9, they move in very opposite directions')
                    ])
                ], width={"size": 6}),
            ])
        ]
    )
], fluid=True)

# Callback to update line plot
@app.callback(
    Output('line-plot', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_graph(selected_stock, selected_metric):
    filtered_df = df[df['ticker'] == selected_stock]
    fig = px.line(
        filtered_df,
        x='date',
        y=selected_metric,
        title=f'{ticker_to_name.get(selected_stock, selected_stock)}\'s {human_labels[selected_metric]} Over Time',
        labels={'date': 'Date', selected_metric: human_labels[selected_metric]},
        hover_data={'date': True, selected_metric: ':.2f'}
    )
    fig.update_layout(
        autosize=True,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(
            family="Open Sans, sans-serif",
            size=14,
            color="#2c3e50"
        ),
        title=dict(
            x=0.5,
            font=dict(
                color='black',
                size=24
            )
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)