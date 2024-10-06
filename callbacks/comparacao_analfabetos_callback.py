from dash import Input, Output
import plotly.express as px
import pandas as pd
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
        Input('tabs', 'value')  # Acionará quando a aba mudar
    )
    def update_comparacao_analfabetos_grafico(selected_tab):
        # Verificar se a aba ativa é a de comparação dos analfabetos
        if selected_tab != 'tab-comparacao-analfabetos':
            return {}, ''

        try:
            # Filtrar e normalizar os dados de 2024
            df_rj_2024_filtered = filter_by_rj(df_rj_2024)

            # Filtrar os analfabetos de 2024 do RJ com faixa etária desejada
            analfabetos_2024 = df_rj_2024_filtered[
                (df_rj_2024_filtered['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO', case=False, na=False)) &
                (df_rj_2024_filtered['DS_FAIXA_ETARIA'].isin(['16 anos', '17 anos', '18 anos', '19 anos', '20 anos']))
            ]
            total_2024 = analfabetos_2024.shape[0]
            print('Total de analfabetos com 20 anos ou menos em 2024:', total_2024)

            # Filtrar e normalizar os dados de 2022
            df_rj_2022_filtered = filter_by_rj(df_rj_2022)

            # Filtrar os analfabetos de 2022 do RJ com faixa etária desejada
            analfabetos_2022 = df_rj_2022_filtered[
                (df_rj_2022_filtered['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO', case=False, na=False)) &
                (df_rj_2022_filtered['DS_FAIXA_ETARIA'].isin(['16 anos', '17 anos', '18 anos', '19 anos', '20 anos']))
            ]
            total_2022 = analfabetos_2022.shape[0]
            print('Total de analfabetos com 20 anos ou menos em 2022:', total_2022)

            # Criar um DataFrame para o gráfico
            comparacao_df = pd.DataFrame({
                'Ano': ['2022', '2024'],
                'Total Analfabetos': [total_2022, total_2024]
            })

            # Gráfico de barras
            fig = px.bar(
                comparacao_df,
                x='Ano',
                y='Total Analfabetos',
                title="Comparação de Analfabetos com 20 Anos ou Menos no RJ (2022 vs 2024)",
                labels={'Total Analfabetos': 'Número de Analfabetos'},
                barmode='group'
            )

            # Calcular a variação percentual total
            variacao_percentual_total = ((total_2024 - total_2022) / total_2022 * 100) if total_2022 > 0 else 0
            texto_variacao = f"A variação percentual total foi de {variacao_percentual_total:.2f}%."

            return fig, texto_variacao

        except Exception as e:
            print(f"Erro no callback 'comparacao_analfabetos': {e}")
            return {}, 'Erro ao calcular a variação percentual.'
