from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import calendar

app = Dash(__name__)
server - app.server

# Assume you have a "long-form" data frame
# See https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("UT-020-PROJETOS.xlsx")

# Renomeie as colunas para facilitar a leitura
df = df.rename(columns={'Status': 'Status', 'Quantidade': 'Quantidade', 'Setor': 'Setor', 'Equipe': 'Equipe', 'Data de Inicio': 'DataInicio'})

# Criando o gráfico de barras inicial
fig_bar = px.bar(df, x="Status", y="Quantidade", color="Setor", barmode="group")

# Criando o gráfico de pizza inicial (ajustado para mostrar a distribuição por Equipe)
fig_pie = px.pie(df, names='Equipe', values='Quantidade', title='Distribuição por Equipe')

# Função para gerar a figura padrão de Quantidade
def create_default_quantidade_figure():
    return px.line(df, x="DataInicio", y="Quantidade", color="Setor", title='Tendência Semanal de Ordens de Serviço')

# Função para obter as opções do dropdown
def get_dropdown_options(column_name):
    options = list(df[column_name].unique())
    options.append(f"Lista por {column_name}")
    return options

opcoes_setor = get_dropdown_options('Setor')
opcoes_equipe = get_dropdown_options('Equipe')
opcoes_anual = get_dropdown_options('Setor')

# Cria um DataFrame de referência com os meses do ano
meses_referencia = pd.DataFrame(index=range(1, 13), columns=['Mes'])
meses_referencia['Mes'] = meses_referencia.index.map(lambda x: calendar.month_abbr[x])

app.layout = html.Div([
    # html, css
    html.H1('Ordem de Serviço - UT - 020 Projetos', style={'color': 'orange', 'fontSize': 40} ),

    html.H2('Gráfico por Setores '),  # Gráfico Barras
    dcc.Dropdown(options=opcoes_anual, value='Lista por Setor', id='lista_Setor_bar'),
    dcc.Graph(id='grafico_por_setor_bar', figure=fig_bar),

    html.H2('Gráfico por Equipe '),  # Gráfico pizza
    dcc.Dropdown(options=opcoes_equipe, value='Lista por Equipe', id='lista_Equipe_pie'),
    dcc.Graph(id='grafico_por_equipe_pie', figure=fig_pie),

    html.H2('Gráfico por Quantidade Anual '),  # Novo bloco para Meses do ano
    dcc.Dropdown(options=opcoes_anual, value='Lista por Setor', id='lista_Setor'),
    dcc.Graph(id='grafico_por_setor', figure=create_default_quantidade_figure())
])

@app.callback(
    Output('grafico_por_setor_bar', 'figure'),
    Input('lista_Setor_bar', 'value')
)
def update_output_bar(value):
    if value == 'Lista por Setor':
        fig = px.bar(df, x="Status", y="Quantidade", color="Setor", barmode="group")
    else:
        tabela_filtrada = df.loc[df['Setor'] == value, :]
        fig = px.bar(tabela_filtrada, x="Status", y="Quantidade", color="Setor", barmode="group")
    return fig

@app.callback(
    Output('grafico_por_equipe_pie', 'figure'),
    Input('lista_Equipe_pie', 'value')
)
def update_output_pie(value):
    if value == 'Lista por Equipe':
        fig = px.pie(df, names='Equipe', values='Quantidade', title='Distribuição por Equipe')
    else:
        tabela_filtrada = df.loc[df['Equipe'] == value, :]
        fig = px.pie(tabela_filtrada, names='Equipe', values='Quantidade', title=f'Distribuição por Equipe - {value}')
    return fig

@app.callback(
    Output('grafico_por_setor', 'figure'),
    Input('lista_Setor', 'value')
)
def update_output_quantidade(value):
    if value == 'Lista por Setor':
        fig = create_default_quantidade_figure()
    else:
        tabela_filtrada = df.loc[df['Setor'] == value, :]

        # Atualiza o eixo x para mostrar os meses do ano
        fig = px.line(tabela_filtrada, x="DataInicio", y="Quantidade", color="Setor", title=f'Tendência Semanal de Ordens de Serviço - {value}')
        fig.update_layout(xaxis=dict(type='category', categoryorder='array', categoryarray=meses_referencia['Mes']))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
