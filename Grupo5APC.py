import dash
from dash import dcc
from dash import html
#caso não funcione, comente as duas linhas superiores e descomente as duas linhas inferiores.
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go
import pandas

#Aqui Pegamos Os Dados de Cada Dupla (ler e colocar os dados em uma forma mais trabalhável(dict))

def DadosAugustoECatlen():
    def SepararPorAno(
            lista_arquivo):  # Lista_arquivos recebe tudo que está em lista_homens (passagem por parâmetro)
        lista_com_os_anos = []
        lista_mortes_por_ano = []

        for coluna in lista_arquivo:
            for linha in coluna:  # "For" serve para percorrer todas as linhas da lista_arquivo
                ano = int(linha.split(";")[
                              2])  # Variavel ano recebe o conteudo presente na posição [2]
                if ano not in lista_com_os_anos:  # Verifica se o ano já esta na lista_com_os_anos
                    lista_com_os_anos.append(
                        ano)  # Coloca o ano na lista_com_os_anos
                    lista_mortes_por_ano.append(
                        0)  # Coloca o valor zero na lista_mortes_por_ano

        for coluna in lista_arquivo:
            for linha in coluna:
                ano = int(linha.split(";")[
                              2])  # Variavel ano recebe o conteudo presente na posição [2]
                mortes = (int(linha.split(';')[
                                  3]))  # Variavel mortes recebe o conteudo presente na posição [3]
                lista_mortes_por_ano[lista_com_os_anos.index(
                    ano)] += mortes  # Soma todas as mortes que o ocorreram em um determinado ano e armazena esse valor na lista_mortes_por_ano

        return lista_mortes_por_ano, lista_com_os_anos  # retorna as listas para a localização onde a função foi chamada
        #   EXEMPLO:
        #           lista_homicidios_homens_por_ano = lista_mortes_por_ano
        #           lista_anos_homens = lista_com_os_anos

    arquivo_homens = pandas.read_csv(
        "homicidios-de-homens-por-armas-de-fogo-uf.csv")  # ler a tabela do excel (540 x 1)
    arquivo_mulheres = pandas.read_csv(
        "homicidios-de-mulheres-por-armas-de-fogo-uf.csv")  # ler a tabela do excel (540 x 1)

    lista_homens = arquivo_homens.values  # tranformar tabela do excel em uma lista
    lista_mulheres = arquivo_mulheres.values  # tranformar tabela do excel em uma lista

    lista_homicidios_homens_por_ano, lista_anos_homens = SepararPorAno(
        lista_homens)  # chama a função SepararPorAno
    lista_homicidios_mulheres_por_ano, lista_anos_mulheres = SepararPorAno(
        lista_mulheres)  # chama a função SepararPorAno

    dicionario = {
        "Homens":{"ano":lista_anos_homens,"homicidios":lista_homicidios_homens_por_ano},
        "Mulheres":{"ano":lista_anos_mulheres,"homicidios":lista_homicidios_mulheres_por_ano}
    }
    return dicionario

def DadosLarissaELeticia():
    data1 = pandas.read_csv("vitimas.csv", sep=";")  # ---------- lê a base de dados e armazena na variável
    data1_array = data1.values  # ---------- lê e armazena cada linha da base de dados como uma lista
    data2 = pandas.read_csv("regioesbrasileiras.csv", sep=";")
    data2_array = data2.values

    dicionarioEstadoRegiao = {}

    for linha in data2_array:
        dicionarioEstadoRegiao[linha[1]] = linha[0]

    # Estado -> anos , ocorrencias
    # Regiao -> estado

    dicionarioEstados = {}

    for linha in data1_array:

        anoAtual = linha[2]
        ufAtual = linha[0]
        crime = linha[1]
        sexo = linha[4]

        if sexo == "Não informado" or sexo == "Sem informação":
            sexo = "Sexo NI"

        if crime == "Lesão corporal seguida de morte":
            crime = "Lesão. Cp. Sg. Morte"
        elif crime == "Roubo seguido de morte (latrocínio)":
            crime = "Latrocínio"

        if anoAtual != 2021:
            if dicionarioEstadoRegiao[ufAtual] not in dicionarioEstados:
                dicionarioEstados[dicionarioEstadoRegiao[ufAtual]] = {crime: {anoAtual: {sexo: linha[5]}}}
            else:
                if crime not in dicionarioEstados[dicionarioEstadoRegiao[ufAtual]]:
                    dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime] = {anoAtual: {sexo: linha[5]}}
                else:
                    if anoAtual not in dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime]:
                        dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime][anoAtual] = {sexo: linha[5]}
                    else:
                        if sexo not in dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime][anoAtual]:
                            dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime][anoAtual][sexo] = linha[5]
                        else:
                            dicionarioEstados[dicionarioEstadoRegiao[ufAtual]][crime][anoAtual][sexo] += linha[5]

    return dicionarioEstados

def DadosOtavioECaio():
    # Para facilitar na hora de fazer o grafico fazemos uma funcao que ira retornar listas com os tipos de crimes, tipos de cimes por ano e ocorrencias por tipo de crimepor ano
    def SepararEmAnosETipos(lista_arquivo):
        lista_tipos_de_crimes = []
        lista_anos = []

        # primeiro vamos abrir listas com o que queremos e vamos abrir listas contendo os tipos de crimes e os anos que estao no arquivo
        for linha in lista_arquivo:
            ano = int(linha[2])
            tipoCrime = linha[1]

            # esse if é pra excluirmos o crime Furto de veiculo e nao ficarmos repetindo os Tipos
            if tipoCrime not in lista_tipos_de_crimes and tipoCrime != "Furto de veículo" and ano != 2021:
                lista_tipos_de_crimes.append(tipoCrime)

            # esse é pra nao repetir o ano
            if ano not in lista_anos and ano != 2021:
                lista_anos.append(ano)

        # vamos reverter a lista dos anos pois ela estava em ordem crescente(decorrencia do arquivo)
        lista_anos.reverse()

        # até entao tinhamos listas com termos, agora vamos fazer uma lista de listas para colocar todos os crimes em uma só variavel
        lista_ano_por_tipo_de_crime = []  # essa conterá os anos.
        lista_ocorrencias_por_tipo_de_crime = []  # essa conterá as ocorrências.

        for tipoCrime in lista_tipos_de_crimes:
            lista_ano_por_tipo_de_crime.append(
                lista_anos)  # aqui estamos adicionando todos os anos em que ocorreram esse crime
            lista_ocorrencias_vazia = []

            # vamos preencher essa lista vazia com zeros para podermos adicionar as ocorrências logo logo.
            for ano in lista_anos:
                lista_ocorrencias_vazia.append(0)

            # agora adicionamos ela na lista de ocorrencias por tipo de crime.
            lista_ocorrencias_por_tipo_de_crime.append(lista_ocorrencias_vazia)

        # Agora ja temos as listas separadas dessa forma:
        #                                todos os anos que ocorreram o 1 crime         todos os anos que ocorreram o 2 crime     ...
        # lista_ano_por_tipo_de_crime = [[2015, 2016, 2017, 2018, 2019, 2020], [2015, 2016, 2017, 2018, 2019, 2020],[...]]
        #  lista ocorrencias_por_tipo_de_crime = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[...]]
        #                            ocorrencias por ano pro 1 crime      ocorr. por ano pro 2 crime       ...

        # Agora vamos preencher a lista com as ocorrencias.
        for linha in lista_arquivo:
            tipoCrime = linha[1]
            ano = int(linha[2])
            ocorrencias = int(linha[4])

            # usamos a proxima linha para não contarmos o furto de veículo na nossa lista.
            if (tipoCrime != "Furto de veículo") and ano != 2021:
                # aqui estamos adicionando na lista de ocorrencia relacionada ao crime que estamos analisando e no ano em que estamos analisando.
                lista_ocorrencias_por_tipo_de_crime[lista_tipos_de_crimes.index(tipoCrime)][
                    lista_anos.index(ano)] += ocorrencias
        # dessa forma, a lista com as ocorrencias terminaria mais ou menos assim:
        #
        #                                       (nota-se que a cada lista é relacionada a um crime diferente)
        # lista_ocorrencias_por_tipo_de_crime = {[[43574, 46770, 50502, 53221, 53765, 47533], [49627, 51645, 53380, 46321, 37835, 40599], [723, 782, 997, 906, 851, 730, 176],[...]}

        return lista_tipos_de_crimes, lista_ano_por_tipo_de_crime, lista_ocorrencias_por_tipo_de_crime

    # ate agr fizemos uma funcao que retorna 3 listas quando dado uma base de dados do tipo lista de listas
    # agr vamos aplicar a funcao e fazer o grafico com os dados trabalhados

    arquivo = pandas.read_excel("indicadoressegurancapublicauf.xlsx")

    # aqui transforma o arquivo em uma lista de listas, onde cada linha é uma lista
    lista_arquivo = arquivo.values

    # Ultilizando dos dados da data base fazemos 3 listas com a funcao criada
    lista_tipos_de_crime, lista_anos_por_tipo_de_crime, lista_ocorrencias_por_tipo_de_crime = SepararEmAnosETipos(
        lista_arquivo)

    dicionario_tipos = {}
    index = 0
    for tipo in lista_tipos_de_crime:
        dicionario_tipos[tipo] = {"ano":lista_anos_por_tipo_de_crime[index],"ocorrencias":lista_ocorrencias_por_tipo_de_crime[index]}
        index += 1

    return dicionario_tipos

def DadosCarolEQuirino():
    # aqui colocamos as listas para os valores e os periodos dos graficos
    per = []
    val = []
    per1 = []
    val1 = []

    # Aqui estamos abrindo o arquivo de base de dados de homicidios de pessoas negras
    with open("homicidios-negros.csv") as f:
        f.readline()
        # Aqui abrimos as linhas, passamos um laço para prucurar as colunas 2 e 3
        linhas = f.readlines()
        for linha in linhas:
            linha = linha.replace('\n', '')  # é inserido um espaçamento dentro da string
            linha = linha.split(';')  # Atribuir os valores da lista a variáveis diferentes
            per.append(int(linha[2]))
            val.append(int(linha[3]))

    # aqui estamos abrindo o arquivo de base de dados de homicidios de pessoas não negras
    with open("homicidios-nao-negros.csv") as f:
        f.readline()
        # Aqui abrimos as linhas, passamos um laço para prucurar as colunas 2 e 3
        linhas = f.readlines()
        for linha in linhas:
            linha = linha.replace('\n', '')  # é inserido um espaçamento dentro da string
            linha = linha.split(';')  # Atribuir os valores da lista a variáveis diferentes
            per1.append(int(linha[2]))
            val1.append(int(linha[3]))

    dicionario = {
        "Negros": {"ano": per, "homicidios": val},
        "Não Negros": {"ano": per1, "homicidios": val1}
    }
    return dicionario

#Aqui Temos Os Gráficos de Cada Um:

def AugustoECatlen(dicionario): # Objetivo: mostra os homicídios por arma de fogo por sexo nos anos de 2000 a 2019.

    grafico = go.Figure()

    for sexo in dicionario:
        grafico.add_scatter(x=dicionario[sexo]["ano"], y=dicionario[sexo]["homicidios"], name=sexo, mode="lines")

    grafico.update_layout(title="Homicídios por Arma de Fogo x Ano",xaxis_title="Ano",yaxis_title="Homicídios",legend_title="Sexo",hovermode="x unified")

    return grafico

def OtavioECaio(dicionarioCrimes,crimesEscolhidos=[]): # Objetivo: mostra as mudanças no número de ocorrencias de crimes no anos 2015-2020.

    # Para construir o grafico vamos criar um grafico em branco e ir adicionando linha por linha em relacao aos crimes utilizando um for para passar em cada crime na lista tipoCrime

    grafico = go.Figure()

    index = 0
    for tipoCrime in dicionarioCrimes:
        if len(crimesEscolhidos) != 0:
            if tipoCrime in crimesEscolhidos:
                grafico.add_scatter(x=dicionarioCrimes[tipoCrime]["ano"], y=dicionarioCrimes[tipoCrime]["ocorrencias"],
                                        mode="markers+lines", name=tipoCrime)
            index += 1
        else:
            grafico.add_scatter(x=dicionarioCrimes[tipoCrime]["ano"], y=dicionarioCrimes[tipoCrime]["ocorrencias"],
                                mode="markers+lines", name=tipoCrime)
            index += 1


    # aqui fazemos o layout do gráfico.
    grafico.update_layout(title="Tipos de Crime x Ano no Brasil 2015 x 2020", xaxis_title="Ano", yaxis_title="Ocorrências",
                          legend_title="Tipo", hovermode="x unified")

    return grafico

def LarissaELeticia(dicionarioEstados,regioesEscolhidas = []):


    crime = []
    ano = []
    regiao = []
    genero = []
    vitimas = []

    for reg in dicionarioEstados:
        if len(regioesEscolhidas) != 0:
            if reg in regioesEscolhidas:
                for tipo_de_crime in dicionarioEstados[reg]:
                    for ano_atual in dicionarioEstados[reg][tipo_de_crime]:
                        for sexo in dicionarioEstados[reg][tipo_de_crime][ano_atual]:
                            crime.append(tipo_de_crime)
                            ano.append(ano_atual)
                            regiao.append(reg)
                            genero.append(sexo)
                            vitimas.append(dicionarioEstados[reg][tipo_de_crime][ano_atual][sexo])
        else:
            for tipo_de_crime in dicionarioEstados[reg]:
                for ano_atual in dicionarioEstados[reg][tipo_de_crime]:
                    for sexo in dicionarioEstados[reg][tipo_de_crime][ano_atual]:
                        crime.append(tipo_de_crime)
                        ano.append(ano_atual)
                        regiao.append(reg)
                        genero.append(sexo)
                        vitimas.append(dicionarioEstados[reg][tipo_de_crime][ano_atual][sexo])



    dados = dict(crime=crime, ano=ano,regiao=regiao, genero=genero, vitimas=vitimas)


    fig = px.sunburst(dados, path=['crime','regiao','ano','genero'], values='vitimas')

    return fig

def CarolEQuirino(dicionario):

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dicionario["Negros"]["ano"], y=dicionario["Negros"]["homicidios"], name='Homicidios de negros',
                         marker=dict(color='black')))  # aqui especificamos a cor e o tipo de grafico

    fig.add_trace(go.Bar(x=dicionario["Não Negros"]["ano"], y=dicionario["Não Negros"]["homicidios"], name='Homicidios não negros',
                         marker=dict(color='darkgrey')))  # aqui especificamos a cor e o tipo de grafico
    fig.update_yaxes(title='Qtde Mortes', visible=True)  # aqui renomeamos o eixo Y
    fig.update_xaxes(title='Ano', visible=True)  # aqui renomeamos o eixo X

    fig.update_layout(barmode='group',
                      xaxis_tickangle=-45,title="Homicídios de Negros x Não Negros")  # Aqui usamos o cod para juntar os dois graficos e criar uma comparação


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
        if linha[2] != 2021:  # linha[2] = ano
            crime.append(linha[1])  # linha[1] = crime
            ocorrencias.append(linha[4])  # linha[4] = ocorrencia

    # criando uma lista com a região
    regiao = []
    for c in range(0, len(data2)):  # percorrendo o data2
        for d in range(0, len(data1)):  # percorrendo o data1
            if data1[d][2] != 2021:  # o d corresponde a coluna, data1[d][2] = ano
                if data2[c][1] == data1[d][0]:  # comparando o nome do estado no data2 com o nome do estado no data1
                    regiao.append(
                        data2[c][0])  # adiciona na lista 'regiao' o nome da região correspondente àquele estado


    # grafico

    df = dict(regioes=regiao, crimes=crime, ocorrencias=ocorrencias)  # informações que estarão no gráfico


    # as ocorrencias são os valores tanto das regiões, quanto dos crimes
    # o path é utilizado para atribuir os valores (as ocorrencias) para 'regioes' e 'crimes'

    fig = px.sunburst(df, path=['regioes', 'crimes'], values='ocorrencias')

    fig.update_layout(
        height=500,  # tamanho do gráfico em px
        title={"text": "Crimes no Brasil entre 2015 e 2020"}  # título
    )

    return fig

#Aqui Fazemos O Layout De Cada Um:

def LayoutOtavioECaio(dados):
    options = []
    for tipo in dados.keys():
        options.append({"label":tipo,"value":tipo})
    return dcc.Dropdown(id="dropdown_OC",
        options=options,multi=True,searchable=False,placeholder="Escolha Um Crime"
    )

def LayoutCarolEQuirino():
    return html.Div()

def LayoutLarissaELeticia(dados):

    options = []

    for reg in dados.keys():
        options.append({"label":reg,"value":reg})

    return dcc.Dropdown(id="dropdown_LL",
        options=options,placeholder="Escolha Uma Região",multi=True,searchable=False
    )

def LayoutAugustoECatlen():
    return html.Div()


duplas = {
    "CQ":dict(funcao_grafico=CarolEQuirino,dados=DadosCarolEQuirino(),layout=LayoutCarolEQuirino),
    "LL":dict(funcao_grafico=LarissaELeticia,dados=DadosLarissaELeticia(),layout=LayoutLarissaELeticia),
    "OC":dict(funcao_grafico=OtavioECaio,dados=DadosOtavioECaio(),layout=LayoutOtavioECaio),
    "AC":dict(funcao_grafico=AugustoECatlen,dados=DadosAugustoECatlen(),layout=LayoutAugustoECatlen)
}

app = dash.Dash(__name__)



app.layout = html.Div(children=[
    html.H1("Gráficos Do Nosso Grupo"),
    dcc.Dropdown(id="dropdown_escolha_grafico"
        ,options=[
            {"label":"Otavio E Caio","value":"OC"},
            {"label":"Larissa E Leticia","value":"LL"},
            {"label":"Carol E Quirino","value":"CQ"},
            {"label":"Augusto E Catlen","value":"AC"},
        ],value="OC",searchable=False
    ),
    html.Div(
        id="grafico_e_layout"
    )

])

@app.callback(
    Output(component_id="grafico_e_layout",component_property="children"),
    Input(component_id="dropdown_escolha_grafico",component_property="value")
)
def CriarGraficoComButoes(value):
    return [duplas[value]['layout'](duplas[value]['dados']),dcc.Graph(id="grafico_" + value,figure=duplas[value]['funcao_grafico'](duplas[value]['dados']))]

@app.callback(
    Output(component_id="grafico_LL",component_property="figure"),
    Input(component_id="dropdown_LL",component_property="value")
)
def DropdownLL(value):
    if value == None:
        return duplas["LL"]['funcao_grafico'](duplas["LL"]["dados"])
    else:
        return duplas["LL"]['funcao_grafico'](duplas["LL"]["dados"],value)

@app.callback(
    Output(component_id="grafico_OC",component_property="figure"),
    Input(component_id="dropdown_OC",component_property="value")
)
def DropdownOC(value):
    if value == None:
        return duplas["OC"]['funcao_grafico'](duplas["OC"]["dados"])
    else:
        return duplas["OC"]['funcao_grafico'](duplas["OC"]["dados"],value)


app.run_server(debug=True)





