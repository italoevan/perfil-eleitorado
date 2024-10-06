from dash import Dash, dcc, html
from callbacks.distribuicao_analfabetos_callback import register_distribuicao_analfabetos_callback
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
    dcc.Tabs(id='tabs', value='tab-distribuicao-analfabetos', children=[
        
        # Tab para a distribuição de analfabetos
        dcc.Tab(label='Distribuição de Analfabetos', value='tab-distribuicao-analfabetos', children=[
            html.H2("Distribuição de Analfabetos no Rio de Janeiro"),
            dcc.Input(
                id='municipio-search', 
                type='text', 
                placeholder='Pesquisar município...', 
                style={'margin-bottom': '20px', 'padding': '10px', 'width': '100%'}
            ),
            html.Ul(id='municipio-list', style={'list-style-type': 'none', 'padding': '0', 'font-size': '18px'})
        ]),
        
        # Tab para analfabetos jovens
        dcc.Tab(label='Analfabetos Jovens', value='tab-analfabetos-below-20', children=[
            dcc.Graph(id='analfabetos-below-20-grafico'),
            html.Div(id='variacao-percentual-below-20-text', style={'margin-top': '20px', 'font-size': '20px'})  
        ]),

        # Tab para comparação 2022 vs 2024
        dcc.Tab(label='Comparação 2022 vs 2024', value='tab-comparacao-analfabetos', children=[
            dcc.Graph(id='comparacao-analfabetos-grafico'),
            html.Div(id='variacao-percentual-text', style={'margin-top': '20px', 'font-size': '20px'})
        ]),
        
    ])
])

# Registrando os callbacks
register_distribuicao_analfabetos_callback(app)
register_analfabetos_below_20_callback(app)
register_comparacao_analfabetos_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
