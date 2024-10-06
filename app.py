from dash import Dash, dcc, html
from callbacks.distribuicao_analfabetos_callback import register_distribuicao_analfabetos_callback
from callbacks.analfabetos_below_20_callback import register_analfabetos_below_20_callback
from callbacks.comparacao_analfabetos_callback import register_comparacao_analfabetos_callback
from data_loader import load_data

# Carregar os dados
df_rj_2024 = load_data('dados/perfil_eleitorado_2024.csv')

# Inicializando o aplicativo Dash
app = Dash(__name__, suppress_callback_exceptions=True)

# Estilos para as abas
tab_style = {
    'padding': '10px',
    'backgroundColor': '#f0f0f0',
    'color': 'black',
    'fontWeight': 'bold',
    'border': '1px solid #d6d6d6'
}

tab_selected_style = {
    'padding': '10px',
    'backgroundColor': '#d6d6d6',
    'color': 'black',
    'fontWeight': 'bold',
    'border': '1px solid #d6d6d6'
}

# Layout da aplicação
app.layout = html.Div([
    html.H1("Eleitorado do Estado do Rio de Janeiro", style={'text-align': 'center', 'margin-bottom': '20px'}),
    dcc.Tabs(id='tabs', value='tab-distribuicao-analfabetos', children=[
        
        # Tab para a distribuição de analfabetos
        dcc.Tab(label='Distribuição de Analfabetos', value='tab-distribuicao-analfabetos', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
                html.H2("Distribuição de Analfabetos no Rio de Janeiro", style={'text-align': 'center', 'margin-bottom': '20px'}),
                html.Div([
                    dcc.Input(
                        id='municipio-search', 
                        type='text', 
                        placeholder='Pesquisar município...', 
                        style={'padding': '10px', 'width': '70%', 'box-sizing': 'border-box', 'border': '1px solid #ccc', 'border-radius': '4px'}
                    ),
                    html.Button('Pesquisar', id='search-button', n_clicks=0, style={'padding': '10px 20px', 'margin-left': '10px', 'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'border-radius': '4px', 'cursor': 'pointer'}),
                ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),
                html.Div(id='municipio-list', style={'max-width': '800px', 'margin': '0 auto'}),
            ])
        ]),
        
        # Tab para analfabetos jovens
        dcc.Tab(label='Analfabetos Jovens', value='tab-analfabetos-below-20', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
                dcc.Graph(id='analfabetos-below-20-grafico'),
                html.Div(id='variacao-percentual-below-20-text', style={'margin-top': '20px', 'font-size': '20px'})
            ])
        ]),

        # Tab para comparação 2022 vs 2024
        dcc.Tab(label='Comparação 2022 vs 2024', value='tab-comparacao-analfabetos', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
                dcc.Graph(id='comparacao-analfabetos-grafico'),
                html.Div(id='variacao-percentual-text', style={'margin-top': '20px', 'font-size': '20px'})
            ])
        ]),
        
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "#f9f9f9"
    })
])

# Registrando os callbacks
register_distribuicao_analfabetos_callback(app)
register_analfabetos_below_20_callback(app)
register_comparacao_analfabetos_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
