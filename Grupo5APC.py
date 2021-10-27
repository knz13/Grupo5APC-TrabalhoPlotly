import copy
import dash
from dash import html
from dash import dcc
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas
import math


def DadosAugustoECatlen():
    def SepararPorAno(lista_arquivo):  # Lista_arquivos recebe tudo que está em lista_homens (passagem por parâmetro)
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
                ano = int(linha.split(";")[2])  # Variavel ano recebe o conteudo presente na posição [2]
                mortes = (int(linha.split(';')[3]))  # Variavel mortes recebe o conteudo presente na posição [3]
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

    return dict(data1_array=data1_array,data2_array=data2_array)


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


def DadosAnaEGuilherme():
    # criando os data frames
    df1 = pandas.read_excel("indicadoressegurancapublicauf.xlsx")
    df2 = pandas.read_csv("regioesbrasileiras.csv", sep=";")

    # transformando os data frames em listas
    data1 = df1.values.tolist()
    data2 = df2.values.tolist()

    return dict(data1=data1,data2=data2)

duplas = {
    "CQ":{"dados":DadosCarolEQuirino()},
    "LL":{"dados":DadosLarissaELeticia()},
    "OC":{"dados":DadosOtavioECaio()},
    "AC":{"dados":DadosAugustoECatlen()},
    "AG":{"dados":DadosAnaEGuilherme()}
}

#Aqui Temos Os Gráficos de Cada Um:


def AugustoECatlen(tipoEscolhido="V"): # Objetivo: mostra os homicídios por arma de fogo por sexo nos anos de 2000 a 2019.

    dicionario = copy.deepcopy(duplas["AC"]["dados"]) #fazer uma copia profunda para não modificar o dicionario principal
    grafico = go.Figure()

    #Se a pessoa escolher o modo porcentagem com base no ano anterior:
    if tipoEscolhido == "P":
        #para cada sexo no dicionario:
        for sexo in dicionario:

            #definimos um homicídio base com o primeiro ano
            homicidio_base = dicionario[sexo]["homicidios"][0]
            
            #colocamos um 0 no inicio, já que não temos anos anteriores
            homicidios_para_colocar_no_fim = [0]

            #para cada valor, vamos adicionar a diferença entre o homicídio do ano anterior e do ano atual.
            for valor in dicionario[sexo]["homicidios"][1:]:
                homicidios_para_colocar_no_fim.append((valor*100/homicidio_base)-100) #adicionamos a diferença entre eles e subtraimos 100 para vermos a diferença 
                homicidio_base = valor #atualizamos o ano anterior (ou ano base)


            #adicionamos os valores atualizados no dicionário
            dicionario[sexo]["homicidios"] = homicidios_para_colocar_no_fim


            #atualizamos o titulo.
            grafico.update_layout(title="Em relação ao ano anterior", xaxis_title="Ano",
                                  yaxis_title="Homicídios %",
                                  legend_title="Sexo", hovermode="x unified", plot_bgcolor="#161A28",
                                  paper_bgcolor="rgba(0,0,0,0)")
    else:
        #atualizamos o titulo
        grafico.update_layout(xaxis_title="Ano", yaxis_title="Homicídios",
                              legend_title="Sexo", hovermode="x unified", plot_bgcolor="#161A28",
                              paper_bgcolor="rgba(0,0,0,0)")


    #para cada sexo, adicionamos uma linha no gráfico.
    for sexo in dicionario:
        grafico.add_scatter(x=dicionario[sexo]["ano"], y=dicionario[sexo]["homicidios"], name=sexo, mode="lines")




    return grafico


def OtavioECaio(crimesEscolhidos=None, desejaLog=None, anoEscolhido=None): # Objetivo: mostra as mudanças no número de ocorrencias de crimes no anos 2015-2020.

    #fazemos uma cópia profunda dos dados no dicionario de duplas para não modificarmos o dicionario.
    dicionario_inicial = copy.deepcopy(duplas["OC"]["dados"])
    

    y_axis_title="Ocorrências"
    if desejaLog != None and desejaLog != []:
        y_axis_title = "Ocorrências (log n)"
        dicionario = {} 
        

        for tipo_crime in dicionario_inicial:
            #dicionario[tipo_crime] = {"ano":[],"ocorrencias":[]}
            dicionario[tipo_crime]["ano"] = dicionario_inicial[tipo_crime]["ano"]
            dicionario[tipo_crime]["ocorrencias"] = list(map(lambda a : math.log(a,10),dicionario_inicial[tipo_crime]["ocorrencias"]))

        #lambda define uma função na hora, sem precisar escrever um def (util para funções pequenas de uso único)
        #no caso esse lambda pega para cada item (variável a) e retorna o log na base 10 dele.


    else:
        #caso a pessoa não escolha o log, somente colocamos o dicionario_inicial
        dicionario = dicionario_inicial



    #caso a pessoa escolha um ou mais anos.
    if anoEscolhido != None and anoEscolhido != []:
        #para cada tipo de crime no dicionario.
        for tipo_crime in dicionario:
            #criamos duas listas vazias para preenchermos com os dados
            lista_ano = []
            lista_ocorrencia = []


            for ano in dicionario[tipo_crime]["ano"]:
                #caso o ano esteja na lista dos anos escolhidos, adicionamos na lista_ano
                if ano in anoEscolhido:
                    lista_ano.append(ano)


            index = 0
            for ocorrencia in dicionario[tipo_crime]["ocorrencias"]:
                #caso essa ocorrencia esteja no ano em que escolhemos, adicionamos na lista_ocorrencia.
                if dicionario[tipo_crime]["ano"][index] in anoEscolhido:
                    lista_ocorrencia.append(ocorrencia)
                index+=1

            #atualizamos o dicionario com as listas novas.
            dicionario[tipo_crime] = {"ano":lista_ano,"ocorrencias":lista_ocorrencia}


    grafico = go.Figure()

    index = 0
    #para cada tipo de crime no dicionario...
    for tipoCrime in dicionario:

        #caso a pessoa tenha escolhido um ou mais crimes:
        if crimesEscolhidos != None and crimesEscolhidos != []:
            #colocamos os crimes especificados no grafico.
            if tipoCrime in crimesEscolhidos:
                grafico.add_scatter(x=dicionario[tipoCrime]["ano"], y=dicionario[tipoCrime]["ocorrencias"],
                                        mode="markers+lines", name=tipoCrime)
            index += 1
        #caso a pessoa não escolha nenhum, colocamos todos.
        else:
            grafico.add_scatter(x=dicionario[tipoCrime]["ano"], y=dicionario[tipoCrime]["ocorrencias"],
                                mode="markers+lines", name=tipoCrime)
            index += 1




    # aqui fazemos o layout do gráfico.
    grafico.update_layout(xaxis_title="Ano",
                          yaxis_title=y_axis_title,
                          legend_title="Tipo",
                          hovermode="x unified",
                          plot_bgcolor="#161A28",
                          paper_bgcolor="rgba(0,0,0,0)",
                          height=350)

    return grafico


def LarissaELeticia(generoEscolhido = []):

    dados=copy.deepcopy(duplas["LL"]["dados"]) #fazemos uma cópia profunda para evitarmos mudar o dicionario principal.

    data1_array = dados["data1_array"]
    data2_array = dados["data2_array"]

    uf = []
    crime = []
    ano = []
    genero = []
    vitimas = []
    regiaos = []
    ufreg = []

    #para cada linha no data1_array (a lista com os dados principais)
    for linha in data1_array:
        geneross = linha[4]
        #caso o genero seja algum desses, vamos colocar o genero como sexo NI.
        if geneross == "Não informado" or geneross == "Sem Informação":
            geneross = 'Sexo NI'

        #caso a pessoa tenha escolhido um ou mais generos, adicionamos apenas esses.
        if linha[2] != 2021 and geneross in generoEscolhido:

            uf.append(linha[0])
            crime.append(linha[1])
            ano.append(linha[2])
            genero.append(geneross)
            vitimas.append(linha[5])

        #caso a pessoa não tenha escolhido nenhum genero, adicionamos todos.
        elif linha[2] != 2021 and generoEscolhido == []:
            uf.append(linha[0])
            crime.append(linha[1])
            ano.append(linha[2])
            genero.append(geneross)
            vitimas.append(linha[5])


    #aqui adicionamos uma relação entre cada região e estado.
    for linha in data2_array:
        regiaos.append(linha[0])
        ufreg.append(linha[1])


    #aqui estamos substituindo os estados por regiões.
    regiao = []
    for estado in uf:
        count = 0
        for estado_reg in ufreg:
            if estado == estado_reg:
                regiao.append(regiaos[count])
            count += 1

    ano = list(map(str, ano))  # muda a lista de anos de inteiro para string, pois para o gráfico precisa ser strings

    crime = ["Ls. Cp. sg. Morte" if value == "Lesão corporal seguida de morte" else value for value in crime]
    crime = ["Latrocínio" if value == "Roubo seguido de morte (latrocínio)" else value for value in crime]

    
    dados = dict(crime=crime, ano=ano, regiao=regiao, genero=genero, vitimas=vitimas)


    #caso a pessoa tenha escolhido mais de um genero
    if len(generoEscolhido) > 1:
        fig = px.sunburst(dados, path=['crime', 'regiao', 'ano', 'genero'], values='vitimas',
                          color='crime',
                          color_discrete_sequence=[ "rgb(146, 224, 211)", "rgb(244, 212, 77)", "rgb(244, 80, 96)"]
                          )
    #caso a pessoa escolha nenhum ou um genero, não colocamos o genero.
    else:
        fig = px.sunburst(dados, path=['crime', 'regiao', 'ano'], values='vitimas',
                          color='crime',
                          color_discrete_sequence=[ "rgb(146, 224, 211)", "rgb(244, 212, 77)", "rgb(244, 80, 96)"]
                          )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=700,
    )
    return fig


def CarolEQuirino(EscolhaChecklist = []):

    dicionario = copy.deepcopy(duplas["CQ"]["dados"]) #fazer uma copia profunda para não modificar o dicionario principal

    fig = go.Figure()

    #caso a pessoa escolha a opção "Negros"
    if "N" in EscolhaChecklist:
        #colocamos a linha de negros
        fig.add_trace(
            go.Bar(x=dicionario["Negros"]["ano"],
                   y=dicionario["Negros"]["homicidios"],
                   name='Negros',
                   marker=dict(color='rgb(244, 212, 77)')))  # aqui especificamos a cor e o tipo de grafico

    if "NN" in EscolhaChecklist:
        fig.add_trace(go.Bar(x=dicionario["Não Negros"]["ano"],
                             y=dicionario["Não Negros"]["homicidios"],
                             name='Não negros',
                             marker=dict(color='rgb(146, 224, 211)')))  # aqui especificamos a cor e o tipo de grafico

    
    fig.update_layout(barmode='group',
                          plot_bgcolor="#161A28",
                          paper_bgcolor="rgba(0,0,0,0)")  # Aqui usamos o cod para juntar os dois graficos e criar uma comparação



    fig.update_yaxes(title='Qtde Mortes', visible=True)  # aqui renomeamos o eixo Y
    fig.update_xaxes(title='Ano', visible=True)  # aqui renomeamos o eixo X

    return fig


def AnaEGuilherme(anoEscolhido = []):

    dados = copy.deepcopy(duplas["AG"]["dados"]) #fazer uma copia profunda para não modificar o dicionario principal
    data1 = dados["data1"]
    data2 = dados["data2"]

    uf = []
    crime = []
    ano = []
    ocorrencias = []
    regioes = []
    ufreg = []

    # coloca os elementos anteriores a 2021 em listas por categoria
    for linha in data1:

        #caso a pessoa não escolha, colocamos todos
        if anoEscolhido == []:
            if linha[2] != 2021: # linha[2] = ano
                uf.append(linha[0])
                crime.append(linha[1]) # linha[1] = crime
                ano.append(linha[2])
                ocorrencias.append(linha[4]) # linha[4] = ocorrencia

        #caso a pessoa escolha algum, colocamos esses anos.
        else:
            if linha[2] != 2021 and linha[2] in anoEscolhido:
                uf.append(linha[0])
                ano.append(linha[2])
                crime.append(linha[1])
                ocorrencias.append(linha[4])

    # separando as regiões e estados respectivos em listas
    for linha in data2:
        regioes.append(linha[0])
        ufreg.append(linha[1])

    #definindo de qual regiao é cada estado da lista uf
    regiao = []
    for estado in uf:  # loop para passar por cada estado da lista uf
        count = 0
        for estado_reg in ufreg:  # loop para passar por cada estado da lista ufreg
            if estado == estado_reg:  # vai comparar se o estado da lista uf é igual ao estado da lista ufreg
                regiao.append(regioes[count])  # se forem iguais, vai adicionar a regiao que esta na mesma posição
            count += 1  # que o estado ufreg a uma nova lista contendo todas as regioes,
                # a posição na lista esta sendo definida pelo contador

    ano = list(map(str, ano))  # muda a lista de anos de inteiro para string, pois para o gráfico precisa ser strings

    # grafico

    df = dict(regioes=regiao, crimes=crime, ocorrencias=ocorrencias)  # informações que estarão no gráfico

    # as ocorrencias são os valores tanto das regiões, quanto dos crimes
    # o path é utilizado para atribuir os valores (as ocorrencias) para 'regioes' e 'crimes'

    fig = px.sunburst(df, path=['regioes', 'crimes'], values='ocorrencias', color='regioes',
                      color_discrete_sequence=["rgb(146, 224, 211)", "rgb(255, 127, 80)", "rgb(154, 62, 73)", "rgb(244, 212, 77)", "rgb(244, 80, 96)"])

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


#adicionando as funções de cada grafico ao dicionario de duplas
duplas = {
    "CQ":{"dados":duplas["CQ"]["dados"],"funcao_grafico":CarolEQuirino},
    "LL":{"dados":duplas["LL"]["dados"],"funcao_grafico":LarissaELeticia},
    "OC":{"dados":duplas["OC"]["dados"],"funcao_grafico":OtavioECaio},
    "AC":{"dados":duplas["AC"]["dados"],"funcao_grafico":AugustoECatlen},
    "AG":{"dados":duplas["AG"]["dados"],"funcao_grafico":AnaEGuilherme},
}

#Aqui Fazemos O Layout De Cada Um:

def LayoutOtavioECaio():
    dados = duplas["OC"]["dados"]
    options = []
    for tipo in dados.keys():
        options.append({"label":tipo,"value":tipo})

    options_ano=[]

    for ano in dados["Estupro"]["ano"]:
        options_ano.append({"label":ano,"value":ano})

    return html.Div(children=[
        dcc.Checklist(id="checklist_OC",
                      options=[{'label':'log', 'value':'LG'}],
                      style=dict(
                          color='#FFFFFF',
                      )),
        dcc.Dropdown(id="dropdown_ano_OC",
                     options=options_ano,
                     multi=True,
                     searchable=False,
                     placeholder="Escolha um ano",
                     style=dict(
                         background='rgba(0,0,0,0)',
                         borderRadius='50px',
                         display='inline-block'
                     )),
        dcc.Dropdown(id="dropdown_OC",
                     options=options,
                     multi=True,
                     searchable=False,
                     placeholder="Escolha Um Crime",
                     style=dict(
                         background='rgba(0,0,0,0)',
                         borderRadius='50px',
                         display='inline-block'
                     ))
    ])


def LayoutCarolEQuirino():
    dados = duplas["CQ"]["dados"]
    return html.Div(dcc.Checklist(id="checklist_CQ",options=[
        {"label":"Negros","value":"N"},
        {"label":"Não Negros","value":"NN"},
    ],value=["N","NN"],labelStyle={"display":"inline-block"}))


def LayoutLarissaELeticia():
    dados = duplas["LL"]["dados"]
    generos = ['Feminino', 'Masculino', 'Sexo NI']
    options = []

    for genero in generos:
        options.append({"label": genero, "value": genero})

    return html.Div(children=[dcc.Dropdown(id="dropdown_LL",
                                           options=options,
                                           placeholder="Escolha um Gênero",
                                           multi=True,
                                           searchable=False,
                                           style=dict(
                                               background='rgba(0,0,0,0)',
                                               borderRadius='50px',
                                               display='inline-block'
                                           ))
                              ])


def LayoutAugustoECatlen():

    dados=duplas["AC"]["dados"]


    return html.Div(children=[dcc.RadioItems(id="radioItems_AC",
                                             options=[
        {"label":"valor","value":"V"},
        {"label":"porcentagem","value":"P"}
    ],
                                             value="V")])


def LayoutAnaEGuilherme():

        dados = duplas["AG"]["dados"]
        options = []
        anos = [2015, 2016, 2017, 2018, 2019, 2020]

        for ano in anos:
            options.append({"label": ano, "value": ano})

        return html.Div(children=[dcc.Dropdown(
            id='dropdown_AG',
            options=options,
            multi=True,
            searchable=False,
            placeholder='Escolha um ano',
            style=dict(
                background='rgba(0,0,0,0)',
                borderRadius='50px',
                display='inline-block'
            ))
        ])


#adicionamos o layout de cada um ao dicionario das duplas
duplas = {
    "CQ":{"dados":duplas["CQ"]["dados"],"funcao_grafico":duplas["CQ"]["funcao_grafico"],"layout":LayoutCarolEQuirino()},
    "LL":{"dados":duplas["LL"]["dados"],"funcao_grafico":duplas["LL"]["funcao_grafico"],"layout":LayoutLarissaELeticia()},
    "OC":{"dados":duplas["OC"]["dados"],"funcao_grafico":duplas["OC"]["funcao_grafico"],"layout":LayoutOtavioECaio()},
    "AC":{"dados":duplas["AC"]["dados"],"funcao_grafico":duplas["AC"]["funcao_grafico"],"layout":LayoutAugustoECatlen()},
    "AG":{"dados":duplas["AG"]["dados"],"funcao_grafico":duplas["AG"]["funcao_grafico"],"layout":LayoutAnaEGuilherme()},
}


app = dash.Dash(__name__)


app.layout = html.Div(
    children=[
        html.Div(className='app-header', children=[
            html.H1("CRIMINALIDADE NO BRASIL", className="app-header--title")
        ]),
        html.Div(className='graficos', children=[
            html.Div(className='OC', children=[html.H1('Tipos de Crime x Ano no Brasil 2015 x 2020'), dcc.Graph(id="grafico_OC", figure=duplas["OC"]['funcao_grafico']()),duplas["OC"]["layout"]]),
            html.Div(className='AG', children=[html.H1('Crimes no Brasil entre 2015 e 2020'), dcc.Graph(id="grafico_AG", figure=duplas["AG"]['funcao_grafico']()),duplas["AG"]["layout"]]),
            html.Div(className='LL', children=[html.H1('Vítimas por gênero dos anos de 2015 a 2020'), dcc.Graph(id="grafico_LL", figure=duplas["LL"]['funcao_grafico']()),duplas["LL"]["layout"]]),
            html.Div(className='AC', children=[html.H1('Homicídios por Arma de Fogo x Ano'), dcc.Graph(id="grafico_AC", figure=duplas["AC"]['funcao_grafico']()),duplas["AC"]["layout"]]),
            html.Div(className='CQ', children=[html.H1('Homicídios de Negros x Não Negros'), dcc.Graph(id="grafico_CQ", figure=duplas["CQ"]['funcao_grafico']()),duplas["CQ"]["layout"]])
        ])
    ])

@app.callback(
    Output(component_id="grafico_LL",component_property="figure"),
    Input(component_id="dropdown_LL",component_property="value")
)
def CallbackLL(value):
    if value == None:
        return duplas["LL"]['funcao_grafico']([])
    else:
        return duplas["LL"]['funcao_grafico'](value)

@app.callback(
    Output(component_id="grafico_OC",component_property="figure"),
    Input(component_id="dropdown_OC",component_property="value"),
    Input(component_id="checklist_OC",component_property="value"),
    Input(component_id="dropdown_ano_OC",component_property="value")
)
def CallbackOC(tipoCrime,log,ano):
        return duplas["OC"]['funcao_grafico'](tipoCrime,log,ano)


@app.callback(
    Output(component_id="grafico_AG",component_property="figure"),
    Input(component_id="dropdown_AG",component_property="value")
)
def CallbackAG(value):
    if value == None:
        return duplas["AG"]['funcao_grafico']([])
    else:
        return duplas["AG"]['funcao_grafico'](value)

@app.callback(
    Output(component_id="grafico_CQ",component_property="figure"),
    Input(component_id="checklist_CQ",component_property="value")
)
#value = NoneType
#value = []
#value = ["N","NN"]
def CallbackCQ(value):
    if value == None:
        return duplas["CQ"]["funcao_grafico"]([])
    else:
        return duplas["CQ"]["funcao_grafico"](value)



@app.callback(
    Output(component_id="grafico_AC",component_property="figure"),
    Input(component_id="radioItems_AC",component_property="value")
)
def CallbackAC(value):
    return duplas["AC"]["funcao_grafico"](value)

app.run_server()




