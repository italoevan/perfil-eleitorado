from dash import Dash, dcc, html
from callbacks.municipio_analfabetos_callback import register_municipio_analfabetos_callback
from callbacks.analfabetos_below_20_callback import register_analfabetos_below_20_callback
from callbacks.comparacao_analfabetos_callback import register_comparacao_analfabetos_callback
from data_loader import load_data

# Carregar os dados
df_rj_2024 = load_data('dados/perfil_eleitorado_2024.csv')

# Inicializando o aplicativo Dash
app = Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Eleitorado do Estado do Rio de Janeiro"),
    dcc.Tabs([
        dcc.Tab(label='Distribuição de Analfabetos', children=[
            dcc.Input(id='municipio-search', type='text', placeholder='Pesquisar município...', debounce=True),  # Barra de pesquisa
            dcc.Dropdown(
                id='municipio-dropdown',
                options=[
                    {'label': municipio, 'value': municipio}
                    for municipio in df_rj_2024['NM_MUNICIPIO'].unique()  # Criação de opções do dropdown
                ],
                placeholder='Selecione um município',
                multi=True  # Permitir seleção múltipla
            ),
            dcc.Graph(id='municipio-analfabetos-grafico'),
            html.Div(id='variacao-percentual-municipio-analfabetos-text', style={'margin-top': '20px', 'font-size': '20px'})
        ]),
        
        dcc.Tab(label='Analfabetos de 20 anos ou menos', children=[
            dcc.Graph(id='analfabetos-below-20-grafico'),
            html.Div(id='variacao-percentual-below-20-text', style={'margin-top': '20px', 'font-size': '20px'})  
        ]),

        dcc.Tab(label='Comparação Analfabetos 2022 vs 2024', children=[
            dcc.Graph(id='comparacao-analfabetos-grafico'),
            html.Div(id='variacao-percentual-text', style={'margin-top': '20px', 'font-size': '20px'})
        ]),
        
    ])
])

# Registrando os callbacks
register_municipio_analfabetos_callback(app)
register_analfabetos_below_20_callback(app)
register_comparacao_analfabetos_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
