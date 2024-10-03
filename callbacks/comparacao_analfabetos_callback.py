from dash import Input, Output
import plotly.express as px
from data_loader import load_data

# Carregar os dados
df_rj_2024 = load_data('dados/perfil_eleitorado_2024.csv')
df_rj_2022 = load_data('dados/perfil_eleitorado_2022.csv')

def filter_by_rj(df):
    """Função auxiliar para filtrar dados do Rio de Janeiro"""
    return df[df['SG_UF'] == 'RJ']

def register_comparacao_analfabetos_callback(app):
    @app.callback(
        Output('comparacao-analfabetos-grafico', 'figure'),
        Output('variacao-percentual-text', 'children'),
        Input('comparacao-analfabetos-grafico', 'id')
    )
    def update_comparacao_analfabetos_grafico(_):
        try:
            # Filtrar os analfabetos de 2024 do RJ
            analfabetos_2024 = filter_by_rj(df_rj_2024)[df_rj_2024['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO')]
            analfabetos_2024_grouped = analfabetos_2024.groupby('NM_MUNICIPIO').size().reset_index(name='count_2024')

            # Filtrar os analfabetos de 2022 do RJ
            analfabetos_2022 = filter_by_rj(df_rj_2022)[df_rj_2022['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO')]
            analfabetos_2022_grouped = analfabetos_2022.groupby('NM_MUNICIPIO').size().reset_index(name='count_2022')

            # Unir os dois dataframes para comparação
            comparacao = analfabetos_2024_grouped.merge(analfabetos_2022_grouped, on='NM_MUNICIPIO', how='outer').fillna(0)

            # Calcular a variação percentual (evitando divisão por zero)
            comparacao['percent_change'] = comparacao.apply(
                lambda row: ((row['count_2024'] - row['count_2022']) / row['count_2022'] * 100) if row['count_2022'] > 0 else 0, axis=1
            )

            # Gráfico de barras
            fig = px.bar(comparacao, x='NM_MUNICIPIO', y=['count_2022', 'count_2024'],
                         title="Comparação de Analfabetos por Localidade no RJ (2022 vs 2024)",
                         labels={'value': 'Número de Analfabetos', 'NM_MUNICIPIO': 'Município'},
                         barmode='group')

            # Variação percentual total
            total_2022 = comparacao['count_2022'].sum()
            total_2024 = comparacao['count_2024'].sum()
            variacao_percentual_total = ((total_2024 - total_2022) / total_2022 * 100) if total_2022 > 0 else 0
            texto_variacao = f"A variação percentual total foi de {variacao_percentual_total:.2f}%."

            return fig, texto_variacao

            print(f"Erro no callback 'comparacao_analfabetos': {e}")
            return {}, 'Erro ao calcular a variação percentual.'


        except Exception as e:
            print(f"Erro no callback 'comparacao_analfabetos': {e}")
            return {}, 'Erro ao calcular a variação percentual.'
