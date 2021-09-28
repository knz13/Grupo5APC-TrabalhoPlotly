import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go
import pandas
import plotly.subplots


def AugustoECatlen():
    def SepararPorAno(lista_arquivo):
        lista_com_os_anos = []
        lista_mortes_por_ano = []

        for coluna in lista_arquivo:
            for linha in coluna:
                ano = int(linha.split(";")[2])
                if ano not in lista_com_os_anos:
                    lista_com_os_anos.append(ano)
                    lista_mortes_por_ano.append(0)

        for coluna in lista_arquivo:
            for linha in coluna:
                ano = int(linha.split(";")[2])
                mortes = (int(linha.split(';')[3]))
                lista_mortes_por_ano[lista_com_os_anos.index(ano)] += mortes

        return lista_mortes_por_ano, lista_com_os_anos

    arquivo_homens = pandas.read_csv("homicidios-de-homens-por-armas-de-fogo-uf.csv")
    arquivo_mulheres = pandas.read_csv("homicidios-de-mulheres-por-armas-de-fogo-uf.csv")

    lista_homens = arquivo_homens.values
    lista_mulheres = arquivo_mulheres.values

    lista_homicidios_homens_por_ano, lista_anos_homens = SepararPorAno(lista_homens)
    lista_homicidios_mulheres_por_ano, lista_anos_mulheres = SepararPorAno(lista_mulheres)

    grafico = go.Figure()

    grafico.add_scatter(x=lista_anos_homens, y=lista_homicidios_homens_por_ano, name="Homens", mode="lines")

    grafico.add_scatter(x=lista_anos_mulheres, y=lista_homicidios_mulheres_por_ano, name="Mulheres", mode="lines")

    grafico.update_layout(title="Homicídios por Arma de Fogo x Ano", xaxis_title="Ano", yaxis_title="Homicídios",
                          legend_title="Sexo", hovermode="x unified")

    return grafico

def OtavioECaio():
    def SepararEmAnosETipos(lista_arquivo):
        lista_tipos_de_crimes = []
        lista_anos = []

        # primeiro vamos passar pelo arquivo inteiro e pegar os tipos de crimes e os anos registrados.
        for linha in lista_arquivo:
            ano = int(linha[2])
            tipoCrime = linha[1]

            # caso o tipo de crime ainda não esteja na lista ou ele seja furto de veículo,não vamos adicionar
            if tipoCrime not in lista_tipos_de_crimes and tipoCrime != "Furto de veículo":
                lista_tipos_de_crimes.append(tipoCrime)

            # caso o ano não esteja na lista dos anos, nós adicionaremos a ela.
            if ano not in lista_anos:
                lista_anos.append(ano)

        # vamos reverter a lista dos anos pois ela estava em ordem decrescente.
        lista_anos.reverse()

        # agora vamos criar duas listas em que colocaremos uma lista para cada tipo de crime
        lista_ano_por_tipo_de_crime = []  # essa conterá os anos.
        lista_ocorrencias_por_tipo_de_crime = []  # essa conterá as ocorrências.

        for tipoCrime in lista_tipos_de_crimes:
            lista_ano_por_tipo_de_crime.append(lista_anos)  # aqui estamos adicionando todos os anos em que ocorreram esse crime.
            lista_ocorrencias_vazia = []

            # vamos preencher essa lista vazia com zeros para podermos adicionar as ocorrências logo logo.
            for i in lista_anos:
                lista_ocorrencias_vazia.append(0)

            # agora adicionamos ela na lista de ocorrencias por tipo de crime.
            lista_ocorrencias_por_tipo_de_crime.append(lista_ocorrencias_vazia)

        #Agora ja temos as listas separadas dessa forma:
        # lista_ano_por_tipo_de_crime = [[2015, 2016, 2017, 2018, 2019, 2020, 2021], [2015, 2016, 2017, 2018, 2019, 2020, 2021],[...]]
        # lista ocorrencias_por_tipo_de_crime = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[...]]

        #Agora vamos preencher a lista com as ocorrencias.
        for linha in lista_arquivo:
            tipoCrime = linha[1]
            ano = int(linha[2])
            ocorrencias = int(linha[4])

            #usamos a proxima linha para não contarmos o furto de veículo na nossa lista.
            if (tipoCrime != "Furto de veículo"):

                #aqui estamos adicionando na lista de ocorrencia relacionada ao crime que estamos analisando e no ano em que estamos analisando.
                lista_ocorrencias_por_tipo_de_crime[lista_tipos_de_crimes.index(tipoCrime)][lista_anos.index(ano)] += ocorrencias

        #dessa forma, a lista com as ocorrencias terminaria mais ou menos assim:
        #
        #                                       (nota-se que a cada lista é relacionada a um crime diferente)
        # lista_ocorrencias_por_tipo_de_crime = {[[43574, 46770, 50502, 53221, 53765, 47533, 16791], [49627, 51645, 53380, 46321, 37835, 40594, 13162], [723, 782, 997, 906, 851, 730, 176],[...]}


        return lista_tipos_de_crimes, lista_ano_por_tipo_de_crime, lista_ocorrencias_por_tipo_de_crime

    #aqui começa o codigo.

    arquivo = pandas.read_excel("indicadoressegurancapublicauf.xlsx")

    lista_arquivo = arquivo.values

    lista_tipos_de_crime, lista_anos_por_tipo_de_crime, lista_ocorrencias_por_tipo_de_crime = SepararEmAnosETipos(
        lista_arquivo)

    #vamos iniciar o gráfico após a separação do arquivo em suas listas que nos interessam.

    grafico = go.Figure()

    index = 0
    for tipoCrime in lista_tipos_de_crime:
        #adicionamos um scatter com o mode="markers+lines" para cada crime.

        grafico.add_scatter(x=lista_anos_por_tipo_de_crime[index], y=lista_ocorrencias_por_tipo_de_crime[index],
                            mode="markers+lines", name=tipoCrime)
        index += 1

    #aqui fazemos o layout do gráfico.
    grafico.update_layout(title="Tipos de Crime x Ano no Brasil", xaxis_title="Ano", yaxis_title="Ocorrências",
                          legend_title="Tipo", hovermode="x unified")

    return grafico

def LarissaELeticia():
    data1 = pandas.read_csv("vitimas.csv", sep=";")
    data1_array = data1.values
    data2 = pandas.read_csv("regioesbrasileiras.csv", sep=";")
    data2_array = data2.values

    uf = []
    crime = []
    ano = []
    genero = []
    vitimas = []
    regiaos = []
    ufreg = []
    # separando cada coluna em listas
    for linha in data1_array:
        # para não pegar o ano de 2020
        if linha[2] != 2021:
            uf.append(linha[0])
            crime.append(linha[1])
            ano.append(linha[2])
            genero.append(linha[4])
            vitimas.append(linha[5])
    # saparando os estados e regiões
    for linha in data2_array:
        # para não pegar o ano de 2020
        regiaos.append(linha[0])
        ufreg.append(linha[1])

    # definindo as regioes dos estados da base de dados com os crimes
    regiao = []
    for j in uf:
        count = 0
        for k in ufreg:
            if j == k:
                regiao.append(regiaos[count])
            count += 1

    # mudando para nomes mais menores
    ano = list(map(str, ano))
    crime = ["Ls. Cp. sg. Morte" if value == "Lesão corporal seguida de morte" else value for value in crime]
    crime = ["Latrocínio" if value == "Roubo seguido de morte (latrocínio)" else value for value in crime]
    genero = ["Sexo NI" if value == "Não informado" or value == "Sem Informação" else value for value in genero]

    # dicionario do banco de dados a ser usado, cada um representa uma lista
    dados = dict(crime=crime, ano=ano, regiao=regiao, uf=uf, genero=genero, vitimas=vitimas)
    # grafico, o path mostra a ordem hierárquica do gráfico, a primeiro é o nível um
    fig = px.sunburst(dados, path=['crime', 'regiao', 'ano', 'genero'], values='vitimas',
                      color='ano',
                      color_discrete_sequence=["rgb(217, 233, 241)", "rgb(247, 182, 152)", "rgb(127, 8, 35)",
                                               "rgb(251, 209, 186)", "rgb(126, 184, 215)", "rgb(5, 48, 97)",
                                               "rgb(217, 233, 241)"]
                      )
    return fig

def CarolEQuirino():
    per = []
    val = []
    per1 = []
    val1 = []

    with open("./homicidios-negros.csv") as f:
        f.readline()

        linhas = f.readlines()
        for linha in linhas:
            linha = linha.replace('\n', '')
            linha = linha.split(';')
            per.append(int(linha[2]))
            val.append(int(linha[3]))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=per, y=val, name='Homicidios de negros', marker=dict(color="darkgrey")))
    fig.update_yaxes(title='Qtde Mortes', visible=True)
    fig.update_xaxes(title='Ano', visible=True)

    with open("./homicidios-nao-negros.csv") as f:
        f.readline()

        linhas = f.readlines()
        for linha in linhas:
            linha = linha.replace('\n', '')
            linha = linha.split(';')
            per1.append(int(linha[2]))
            val1.append(int(linha[3]))

    fig.add_trace(go.Bar(x=per1, y=val1, name='Homicidios nao negros', marker=dict(color="darkgrey")))
    fig.update_yaxes(title='Qtde Mortes', visible=True)
    fig.update_xaxes(title='Ano', visible=True)

    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    return fig

def AnaEGuilherme():
    # criando os data frames
    df1 = pandas.read_excel("indicadoressegurancapublicauf.xlsx")
    df2 = pandas.read_csv("regioesbrasileiras.csv", sep=";")

    # transformando os data frames em listas
    data1 = df1.values.tolist()
    data2 = df2.values.tolist()

    crime = []
    ocorrencias = []

    # coloca os elementos anteriores a 2021 em listas por categoria
    for linha in data1:
        if linha[2] != 2021:
            crime.append(linha[1])
            ocorrencias.append(linha[4])

    # criando uma tabela com a região
    regiao = []
    for c in range(0, len(data2)):  # percorrendo o data2
        for d in range(0, len(data1)):  # percorrendo o data1
            if data1[d][2] != 2021:  # o d corresponde a coluna, data1[d][2] = ano
                if data2[c][1] == data1[d][0]:  # comparando o nome do estado no data2 com o nome do estado no data1
                    regiao.append(
                        data2[c][0])  # adiciona na lista 'regiao' o nome da região correspondente àquele estado

    # grafico

    df = pandas.DataFrame(
        dict(regioes=regiao, crimes=crime, ocorrencias=ocorrencias)  # informações que estarão no gráfico
    )

    # as ocorrencias são os valores tanto das regiões, quanto dos crimes
    # o path é utilizado para atribuir os valores (as ocorrencias) para 'regioes' e 'crimes'

    fig = px.sunburst(df, path=['regioes', 'crimes'], values='ocorrencias')

    fig.update_layout(
        height=500,  # tamanho do gráfico em px
        title={"text": "Crimes no Brasil entre 2015 e 2020"}  # título
    )

    return fig






#grafico = AnaEGuilherme()

#py.plot(grafico)

#app = dash.Dash(__name__)
#app.layout = html.Div(children=[
#    html.H1(children="Graficos Do Nosso Grupo"),
#    dcc.Dropdown(
#        options=[
#            {"label" : "Otavio e Caio","value":"OC"},
#            {"label" : "Augusto e Catlen","value":"AC"},
#            {"label" : "Larissa e Letícia","value":"LL"},
#            {"label" : "Carol e Quirino","value":"CQ"},
#            {"label" : "Ana e Guilherme","value":"AG"}
#        ]
#    )
#
#])
#
#app.run_server(debug=True)