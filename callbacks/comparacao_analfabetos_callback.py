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

def clean_column_values(df, column_name):
    """Função para limpar espaços extras e normalizar os valores de uma coluna"""
    df[column_name] = df[column_name].str.strip().str.lower()
    return df

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
            # Filtrar e limpar os dados de 2024
            df_rj_2024_filtered = filter_by_rj(df_rj_2024)
            df_rj_2024_filtered = clean_column_values(df_rj_2024_filtered, 'DS_GRAU_ESCOLARIDADE')
            df_rj_2024_filtered = clean_column_values(df_rj_2024_filtered, 'DS_FAIXA_ETARIA')
            df_rj_2024_filtered = clean_column_values(df_rj_2024_filtered, 'NM_MUNICIPIO')

            # Filtrar os analfabetos de 2024 do RJ com faixa etária desejada
            analfabetos_2024 = df_rj_2024_filtered[
                (df_rj_2024_filtered['DS_GRAU_ESCOLARIDADE'].str.contains('analfabeto', na=False)) &
                (df_rj_2024_filtered['DS_FAIXA_ETARIA'].isin(['16 anos', '17 anos', '18 anos', '19 anos', '20 anos']))
            ]

            # Agrupar por município e zona, contando os registros em 2024
            analfabetos_2024_grouped = analfabetos_2024.groupby(['NM_MUNICIPIO', 'NR_ZONA']).size().reset_index(name='count_2024')

            # Filtrar e limpar os dados de 2022
            df_rj_2022_filtered = filter_by_rj(df_rj_2022)
            df_rj_2022_filtered = clean_column_values(df_rj_2022_filtered, 'DS_GRAU_ESCOLARIDADE')
            df_rj_2022_filtered = clean_column_values(df_rj_2022_filtered, 'DS_FAIXA_ETARIA')
            df_rj_2022_filtered = clean_column_values(df_rj_2022_filtered, 'NM_MUNICIPIO')

            # Filtrar os analfabetos de 2022 do RJ com faixa etária desejada
            analfabetos_2022 = df_rj_2022_filtered[
                (df_rj_2022_filtered['DS_GRAU_ESCOLARIDADE'].str.contains('analfabeto', na=False)) &
                (df_rj_2022_filtered['DS_FAIXA_ETARIA'].isin(['16 anos', '17 anos', '18 anos', '19 anos', '20 anos']))
            ]

            # Agrupar por município e zona, contando os registros em 2022
            analfabetos_2022_grouped = analfabetos_2022.groupby(['NM_MUNICIPIO', 'NR_ZONA']).size().reset_index(name='count_2022')

            # Unir os dois DataFrames para comparação
            comparacao = pd.merge(analfabetos_2022_grouped, analfabetos_2024_grouped, on=['NM_MUNICIPIO', 'NR_ZONA'], how='outer').fillna(0)

            # Encontrar os registros que deixaram de ser analfabetos em 2024
            comparacao['changed_to_literate'] = comparacao.apply(
                lambda row: 1 if row['count_2022'] > 0 and row['count_2024'] == 0 else 0,
                axis=1
            )

            # Calcular o número de analfabetos que mudaram para alfabetizados
            total_changed_to_literate = comparacao['changed_to_literate'].sum()

            # Calcular o total de analfabetos em 2022
            total_2022 = comparacao['count_2022'].sum()

            # Calcular a variação percentual de analfabetos que mudaram para alfabetizados
            variacao_percentual_total = ((total_changed_to_literate) / total_2022 * 100) if total_2022 > 0 else 0

            # Calcular a diferença total
            total_alfabetizados = total_2022 - total_changed_to_literate

            # Texto de saída com a subtração e a quantidade de alfabetizados
            texto_variacao = (
                f"A variação percentual de analfabetos que mudaram para alfabetizados foi de {variacao_percentual_total:.2f}%.\n"
                f"Total de analfabetos que agora são alfabetizados: {total_changed_to_literate}.\n"
                f"Subtração entre os números: {total_2022} - {total_changed_to_literate} = {total_alfabetizados}."
            )

            # Criar um DataFrame para o gráfico
            comparacao_df = pd.DataFrame({
                'Ano': ['2022', '2024'],
                'Total Analfabetos': [total_2022, total_alfabetizados]
            })

            # Gráfico de barras
            fig = px.bar(
                comparacao_df,
                x='Ano',
                y='Total Analfabetos',
                title="Comparação de Analfabetos com 20 Anos ou Menos no RJ por Município e Zona (2022 vs 2024)",
                labels={'Total Analfabetos': 'Número de Analfabetos'},
                barmode='group'
            )

            return fig, texto_variacao

        except Exception as e:
            print(f"Erro no callback 'comparacao_analfabetos': {e}")
            return {}, 'Erro ao calcular a variação percentual.'
