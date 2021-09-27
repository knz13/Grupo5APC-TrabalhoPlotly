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

    py.plot(grafico)

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
            lista_ano_por_tipo_de_crime.append(
                lista_anos)  # aqui estamos adicionando todos os anos em que ocorreram esse crime.
            lista_ocorrencias_vazia = []

            # vamos preencher essa lista vazia com zeros para podermos adicionar as ocorrências logo logo.
            for i in lista_anos:
                lista_ocorrencias_vazia.append(0)

            # agora adicionamos ela na lista de ocorrencias por tipo de crime.
            lista_ocorrencias_por_tipo_de_crime.append(lista_ocorrencias_vazia)

        #Agora ja temos as listas separadas dessa forma:
        # lista_ano_por_tipo_de_crime = {[[2015, 2016, 2017, 2018, 2019, 2020, 2021], [2015, 2016, 2017, 2018, 2019, 2020, 2021],[...]}
        # lista ocorrencias_por_tipo_de_crime = {[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[...]]}

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

    py.plot(grafico)

def LarissaELeticia():
    data1 = pandas.read_csv("bd/vitimas.csv", sep=";")
    data1_array = data1.values
    data2 = pandas.read_csv("bd/regioesbrasileiras.csv", sep=";")
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
    py.plot(fig)

def Carol():
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
    py.plot(fig)


Carol()