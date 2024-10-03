from dash import Input, Output
import plotly.express as px
from data_loader import load_data

# Carregar os dados
df_rj_2024 = load_data('dados/perfil_eleitorado_2024.csv')

def filter_by_rj(df):
    """Filtra dados apenas do Rio de Janeiro."""
    return df[df['SG_UF'] == 'RJ']

def clean_column_values(df, col_name):
    """Normaliza os valores de uma coluna removendo espaços e convertendo para maiúsculas."""
    return df[col_name].str.strip().str.upper()

def get_analfabetos_por_municipio(df, search_value=None):
    """Conta a quantidade de analfabetos por município e filtra pelo valor de pesquisa, se fornecido."""
    analfabetos_municipios = filter_by_rj(df)[df['DS_GRAU_ESCOLARIDADE'] == 'ANALFABETO']
    
    # Contar a quantidade de analfabetos por município
    analfabetos_por_municipio = analfabetos_municipios['NM_MUNICIPIO'].value_counts().reset_index()
    analfabetos_por_municipio.columns = ['Municipio', 'Quantidade']

    # Filtrar pela pesquisa, se houver valor na barra de pesquisa
    if search_value:
        analfabetos_por_municipio = analfabetos_por_municipio[
            analfabetos_por_municipio['Municipio'].str.contains(search_value.upper(), na=False)
        ]
    
    return analfabetos_por_municipio

def create_pie_chart(data):
    """Cria um gráfico de pizza a partir dos dados fornecidos."""
    return px.pie(
        data,
        names='Municipio',
        values='Quantidade',
        title="Distribuição de Analfabetos por Município no RJ (2024)",
        color_discrete_sequence=px.colors.sequential.Viridis
    )

def register_municipio_analfabetos_callback(app):
    @app.callback(
        Output('municipio-analfabetos-grafico', 'figure'),
        Output('municipio-list', 'children'),  # Output para lista de municípios
        Input('municipio-dropdown', 'value'),  # O valor selecionado do dropdown
        Input('municipio-search', 'value')     # O valor da barra de pesquisa
    )
    def update_municipio_analfabetos_grafico(selected_municipio, search_value):
        try:
            # Normalizar os dados
            df_rj_2024['DS_GRAU_ESCOLARIDADE'] = clean_column_values(df_rj_2024, 'DS_GRAU_ESCOLARIDADE')
            
            # Obter analfabetos por município
            analfabetos_por_municipio = get_analfabetos_por_municipio(df_rj_2024, search_value)

            # Criar gráfico de pizza
            fig = create_pie_chart(analfabetos_por_municipio)

            # Criar lista de municípios com suas quantidades
            lista_municipios = [
                f"{municipio}: {quantidade} analfabetos"
                for municipio, quantidade in zip(analfabetos_por_municipio['Municipio'], analfabetos_por_municipio['Quantidade'])
            ]

            return fig, lista_municipios

        except Exception as e:
            print(f"Erro no callback 'municipio_analfabetos': {e}")
            return {}, 'Erro ao calcular a quantidade de analfabetos por município.'
