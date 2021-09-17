import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import base64
import openpyxl

st.sidebar.image('https://www.pragma.com.co/hs-fs/hubfs/logo-udea.png?width=312&name=logo-udea.png',width=300,caption='MENU')
#st.sidebar.markdown("<h3 style='text-align: center; color: #971B00;'>Menu</h3>", unsafe_allow_html=True)

#Barra de navegacion

op = st.sidebar.radio('',['🏠 Inicio', '👪 Hogares colombianos', '🏭 Empresas del pais','📊 Analisis Agrupado','🤝 Concluciones'])
st.sidebar.info('Hecho por: Mayra Alejandra Bastidas, Sebastian Franco, Karol Lagos')

if op == '🏠 Inicio':
    
    #Titulo Principal
    st.markdown("<h1 style='text-align: center; color: #971B00;'>Impacto de la situación económica de las empresas en la economía de los hogares colombianos</h1>", unsafe_allow_html=True)

   
    st.markdown("<h3 style='text-align:justify;'>En el contexto colombiano son múltiples los factores que inciden en el tema de la pobreza:  falta de acceso al capital, los cambios en los grupos sociales, el aumento del desempleo, endeudamiento, falta de educación, entre muchos otros y aunque existen programas de mitigación de la pobreza han sido pocos los alcances que se han logrado. En este punto, es interesante analizar qué grado de importancia cobra la economía de una empresa en la calidad de vida de las personas.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; '></h3>", unsafe_allow_html=True)
    st.image('https://static.vecteezy.com/system/resources/previews/001/850/946/non_2x/finance-professionals-character-concept-banner-vector.jpg')
    
#Leer bases de datatos Hogares
@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data(url):
    df = pd.read_excel(url) # leer datos
    df.columns = df.columns.str.lower()
    df['tipo_hogar'] = df['tipo_hogar'].replace({6: 'Sin Titulo'})
    df['cuota_pago'] = df['cuota_pago'].replace({' ':0,98:0, 99:0})
    df['estimacion_arriendo']= df['estimacion_arriendo'].replace({' ':0})
    df['precio_arriendo']= df['precio_arriendo'].replace({' ':0, 99:0,98:0})
    df['minimo'] = df['ingreso'].apply(lambda x: 'Menos' if x<908526 else 'Mas')
    df['condicion'] = df['npobres'].apply(lambda x : 'Familia pobre' if x > 0 else 'Condicion normal')
    return df
hogares=load_data('HOGARES.xlsx')

#Leer bases de datos empresas
@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data_1(url):
    df = pd.read_csv(url) # leer datos
    return df
empresas=load_data_1('empresas.csv') #Carga de base ya tratada en colab


#Leer bases de datos Bodega
@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data_3(url):
    df = pd.read_csv(url) # leer datos
    return df
bodega=load_data_3('bodega.csv') #Base ya tratada en colab


if op == '👪 Hogares colombianos':
    
    #Analisis de Hogares
    st.markdown("<h1 style='text-align: center;color:#E89B8A; '>Analisis de los hogares Colombianos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify; '>A continuacion se mostraran los resultados obtenidos acerca de los hogares Colombianos con los analisis correspondientes</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns((0.4,1,1)) # Entre paréntesis se indica el tamaño de las columnas
    c2.image('familias.jpg',width = 500)
    
    
    #Primera Grafica
    c1, c2 = st.columns((1.2,1)) # Entre paréntesis se indica el tamaño de las columnas

   
    x4 = hogares.groupby('minimo')[['directorio']].count().reset_index().rename(columns = {'directorio' : 'acomulado'})

    fig = px.pie(x4, values = 'acomulado', names ='minimo',
             title= '<b>Ingresos comparados con el salario minimo<b>')

    # agregar detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        )
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    fig.update_traces(hoverinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)),
                  textposition='inside', textinfo='percent+label')

    c1.plotly_chart(fig,use_container_width=True)
    
   
    c2.markdown("<h2 style='text-align: center; '></h2>", unsafe_allow_html=True)
    c2.info('El 68.2% de las familias Colombianas tienen un salario que está por encima del salario mínimo y el 31,8% de las familias reciben un salario inferior. Esto nos muestra de forma general cual es la realidad de los hogares colombianos, en donde casi un tercio de la población  tiene que subsistir con menos del salario mínimo estipulado por el gobierno.')
    #st.markdown("<h2 style='text-align: center;color:#E89B8A; '>Resultados por ciudades</h2>", unsafe_allow_html=True)
   
    
   #Segunda Grafica
       
    
    x1 = hogares.groupby('dominio')[['ingreso','directorio' ]].agg({'ingreso': 'sum','directorio':'count'}).reset_index()
    x1 = x1[(x1['dominio']!= 'RURAL') & (x1['dominio']!= 'RESTO URBANO') ]
    x1['ingreso_promedio'] = x1['ingreso']/x1['directorio']
    x1 = x1.sort_values('ingreso_promedio',ascending=False)
    fig = px.bar(x1, x = 'dominio', y='ingreso_promedio', title= '<b>Ingreso promedio de familias por ciudad<b>')
    
    
    
    fig.update_layout(
        xaxis_title = 'Ciudades',
        yaxis_title = 'Ingresos',
        template = 'simple_white',
        title_x = 0.5)
    st.info('En la gráfica se observa que las familias que tienen mejores ingresos son de la ciudad de Medellín, le sigue las familias que habitan en la ciudad de Bogotá; esto puede ser explicado con que son las ciudades más grandes en varios sectores económicos.  También, se observa que las familias que viven en Tunja, Armenia, Sincelejo, Ibague, Monteria, Pasto y Riohacha tienen ingresos similares, finalmente se logra analizar que las familias que habitan en Quibdó tienen los ingresos más bajos.')
    st.plotly_chart(fig,use_container_width=True)
    
    
    #Tercera Grafica
   
    ciudad = st.selectbox('Seleccione ciudad',hogares['dominio'].unique(),index=10)
    
    c1, c2 = st.columns((1.8,1)) # Entre paréntesis se indica el tamaño de las columnas
    
    x2 = hogares.groupby(['dominio','condicion'])[['directorio']].sum().reset_index().rename(columns = {'directorio' : 'acomulado'})        
    fig = px.pie(x2[x2['dominio']==ciudad], values = 'acomulado', names ='condicion',
             title= '<b>Porcentaje de pobres y condicion normal<b>')

    # agregar detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        )

    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    fig.update_traces(hoverinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)),textposition='inside', textinfo='percent+label')
    c1.plotly_chart(fig,use_container_width=True)
    c2.markdown("<h2 style='text-align: center; '></h2>", unsafe_allow_html=True)
    c2.info('Teniendo como referencia la ciudad de Quibdo, el porcentaje de familias en condición de pobreza es de  29.3% Esto representa casi un tercio de toda la población en la ciudad y es el mayor porcentaje comparandolo con el resto de ciudades con este grafico')
    
    #Cuarta Grafica
    
    x3 = hogares.groupby(['dominio', 'tipo_hogar'])['directorio'].count().reset_index().rename(columns = {'directorio' : 'acomulado'})
    x3 = x3[(x3['dominio']== 'FLORENCIA') | (x3['dominio']== 'CUCUTA') | (x3['dominio']== 'QUIBDO') ]
    
    fig = px.bar(x3, x = 'dominio', y='acomulado', color = 'tipo_hogar', barmode = 'group', 
             title= '<b>Tipos de hogar en las ciudades con menos ingresos<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Ciudades',
        yaxis_title = 'Acomulado',
        template = 'simple_white',
        title_x = 0.5)
    
    st.write(fig,use_container_width=True)
    st.info('De estas tres ciudades Quibdó es la que tiene mayor cantidad de familias que tiene tipo de hogar  propio y cúcuta es la que tiene menor cantidad, también observamos de la gráfica que la mayor cantidad de familias que pagan arriendo están en la ciudad Florencia, además la menor cantidad de familias que viven en su hogar, pero aún lo están pagando se encuentran en la ciudad de Quibdó y cúcuta como florencia tiene una cantidad similar de familias que tiene tipo hogar usufructo. A pesar de que estas 3 son las ciudades donde viven las familias con menores ingresos  la mayoría tiene su hogar propio.')
    

if op == '🏭 Empresas del pais':
    st.markdown("<h1 style='text-align: center;color:#E89B8A; '>Analisis de las empresas Colombianas</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify; '>Esta sección se comprende de los analisis obtenidos de los resultados financieros de las empresas colombianas en los diferentes departamentos de colombia</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns((0.4,1,1)) # Entre paréntesis se indica el tamaño de las columnas
    c2.image('empresas.jpg',width = 500)
    
    #Primer grafica
    st.info('Debido a que los ingresos acumulados de las empresas tienen diferencias muy grandes se decide mostrar los 5 primeros departamentos con mejores ingresos acumulados y graficar los otros departamentos')
    
    x5 = empresas.groupby(['departamento'])[['ingresos_operacionales_2017','ingresos_operacionales_2018']].sum().reset_index().sort_values('ingresos_operacionales_2018', ascending=False).reset_index(drop = True)
    pd.options.display.float_format = '{:.0f}'.format
    st.table(x5.head(5))
   
    
    
    #Segunda Grafica
    
    año = st.selectbox('Seleccione el  año', options = [2017,2018])
    
    if año == 2017:
        x5 = x5[['departamento', 'ingresos_operacionales_2017']]
        yvalue = 'ingresos_operacionales_2017'
    else:
        x5 = x5[['departamento', 'ingresos_operacionales_2018']]
        yvalue = 'ingresos_operacionales_2018'
        
    
    fig = px.bar(x5.iloc[5:,:], x = 'departamento', y=yvalue, barmode = 'group',
             title= '<b>Ingresos acumulados de las empresas en cada departamento<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)

    fig.update_layout(
        xaxis_title = 'Departamentos',
        yaxis_title = 'Ingresos',
        template = 'simple_white',
        title_x = 0.5)
    
    st.write(fig,use_container_width=True)
    st.info('Teniendo en cuenta las dos gráficas anteriores, las empresas que tienen mejores ingresos acumulados en el 2017 son las que se encuentran en el departamento de Cundinamarca, esto puede ser debido a que las empresas de esta región  tienen buena rentabilidad o dado que este departamento posee muchas empresas. En el departamento de Sucre están las empresas con menores ingresos acumulados, esto puede ser debido a la poca cantidad de empresas en esta región o que la rentabilidad de las empresas no es buena. Ademas con esta grafica podemos observar los mismos resultados para el año 2018')
    
    #tercera Grafica
    
    
    
    nota = empresas.groupby(['macrosector'])[['ingresos_operacionales_2018']].sum().reset_index().sort_values('ingresos_operacionales_2018', ascending=False)
    fig = px.bar(nota, x = 'macrosector', y='ingresos_operacionales_2018', barmode = 'group', 
             title= '<b>Ingesos operacionales en cada macrosector<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)


    fig.update_layout(
        xaxis_title = 'Macrosector',
        yaxis_title = 'Ingresos',
        template = 'simple_white',
        title_x = 0.5)
    
    st.write(fig,use_container_width=True)
    st.info('El macrosector comercio es el que genera mejores ingresos a nivel nacional luego le sigue Servicios, por lo que es recomendable invertir en estos macrosectores para tener mayor probabilidad de tener resultados positivos. El macrosector agropecuario e hidrocarburos son los que generan menores ingresos. ')
    
    #Cuarta Grafica
    
    a1= empresas[empresas['macrosector'].isin(['COMERCIO','SERVICIOS', 'MANUFACTURA'])]
    x6= a1.groupby(['departamento', 'macrosector'])[['ingresos_operacionales_2018']].sum().reset_index().sort_values('ingresos_operacionales_2018', ascending=False)
    
    fig = px.bar(x6.iloc[0:14,:], x = 'departamento', y='ingresos_operacionales_2018', color = 'macrosector', barmode = 'group', 
             title= '<b>Ingesos operacionales según el departamento y su macrosector<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Departamentos',
        yaxis_title = 'Ingresos',
        template = 'simple_white',
        title_x = 0.5)
    
    st.write(fig,use_container_width=True)
    st.info('Sin duda Cundinamarca es un lugar ideal para invertir en empresas dedicadas al comercio, servicios y manufactura. En el Valle y Antioquia las empresas dedicadas al  macrosector manufactura generan mejores ingresos, y en departamento de Bolívar no hay empresas que hagan parte del macrosector comercio.')
    
    #Quinta Grafica
    
    x7=empresas.groupby(['departamento']).agg({'ingresos_operacionales_2018':'sum', 'ingresos_operacionales_2017': 'count'}).reset_index().sort_values('ingresos_operacionales_2018', ascending=False)
    x7=x7.rename(columns={'ingresos_operacionales_2017':'Número_de_empresas'})
    x7['ingresos_promedio_2018']= x7['ingresos_operacionales_2018']/x7['Número_de_empresas']
    x7=x7.sort_values('ingresos_promedio_2018', ascending=False)

    fig = px.bar(x7, x = 'departamento', y='ingresos_promedio_2018', barmode = 'group', 
                 title= '<b>Promedio de Ingresos por empresa en cada departamento<b>',
                 color_discrete_sequence=px.colors.qualitative.Pastel2)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Departamentos',
        yaxis_title = 'Ingresos promedio',
        template = 'simple_white',
        title_x = 0.5)
    
    st.write(fig,use_container_width=True)
    st.info('Si tenemos en cuenta el numero de empresas que hay en los departamentos, las empresas ubicadas en el departamento Bolívar tienen en promedio mejores ingresos; quiere decir que las empresas de esta región  están dedicadas a unos macrosectores que generan buenas utilidades. Las empresas ubicadas en los departamentos de Cesar, Casanare, San Andrés, Chocó, Meta, Boyacá, y Sucre tienen en promedio ingresos similares')
    
    
    
    
if op == '📊 Analisis Agrupado':
    
    st.markdown("<h1 style='text-align: center;color:#E89B8A; '>Analisis Agrupado de las empresas y familias Colombianas</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify; '>Luego de dar una mirada a las condiciones de las familias y empresas, se realizara una exploracion del resultado al combinar los datos de estos dos grupos de interes.</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns((0.4,1,1)) # Entre paréntesis se indica el tamaño de las columnas
    c2.image('agrupado.jpg',width = 500)
    
    #Descarga de correlaciones
   
    def get_table_download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
        return href
    
    x = bodega.corr()
    
    c1, c2 = st.columns((1,1.7)) # Entre paréntesis se indica el tamaño de las columnas
    c1.text('Descarga de correlaciones')
    c1.markdown(get_table_download_link(x), unsafe_allow_html=True)

    c2.info('En el enlace puedes obtener un archivo con las correlaciones de las variables de interes')
    
    #Primera Grafica
    st.markdown("<h3 style='text-align: center;color:#E89B8A; '>Ingresos de empresas VS ingresos de familias</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas

    
    plt.tight_layout()
    fig = plt.figure()
    plt.scatter(x = bodega['ingreso'], y = bodega['ingresos_operacionales_2017'])
    plt.title('Grafico de disperción')
    plt.xlabel('ingreso personas')
    plt.ylabel('ingreso empresas')
    c1.write(fig,use_container_width=True)
    
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['ingreso'], y = bodega['ingresos_operacionales_2018'])
    plt.title('Grafico de disperción')
    plt.xlabel('ingreso personas')
    plt.ylabel('ingreso empresas')
    c2.pyplot(fig,use_container_width=True)
    
    st.info('La correlación de estas dos variables es positiva y el comportamiento aparentemente es exponencial, pero faltan datos para corroborarlo.')
    
    #Segunda Grafica
    st.markdown("<h3 style='text-align: center;color:#E89B8A; '>Ingresos de empresas VS Numero de pobres</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['npobres'], y = bodega['ingresos_operacionales_2017'])
    plt.title('Grafico de disperción')
    plt.xlabel('Número de pobres')
    plt.ylabel('ingreso empresas en el 2017')
    c1.write(fig,use_container_width=True)
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['npobres'], y = bodega['ingresos_operacionales_2018'])
    plt.title('Grafico de disperción')
    plt.xlabel('Número de pobres')
    plt.ylabel('ingreso empresas en el 2018')
    c2.write(fig,use_container_width=True)
    
    st.info('No hay una relación clara entre los ingresos y el número de pobres en cada departamento')
    
    
    #Tercera Grafica
    st.markdown("<h3 style='text-align: center;color:#E89B8A; '>Ingresos de empresas VS Numero de indigentes</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['nindigentes'], y = bodega['ingresos_operacionales_2017'])
    plt.title('Grafico de disperción')
    plt.xlabel('Número de indigentes')
    plt.ylabel('ingreso empresas en el 2017')
    c1.write(fig,use_container_width=True)
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['nindigentes'], y = bodega['ingresos_operacionales_2018'])
    plt.title('Grafico de disperción')
    plt.xlabel('Número de indigentes')
    plt.ylabel('ingreso empresas en el 2018')
    c2.write(fig,use_container_width=True)
    
    st.info('No hay una relación clara entre los ingresos y el número de indigentes en cada departamento')
    
    #Cuarta grafica
    st.markdown("<h3 style='text-align: center;color:#E89B8A; '>Numero de pobres VS numero de indigentes</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas
    
    fig = plt.figure()
    plt.tight_layout()
    plt.scatter(x = bodega['nindigentes'], y = bodega['npobres'])
    plt.title('Grafico de disperción')
    plt.xlabel('Número de indigentes')
    plt.ylabel('Número de pobres')
    c1.write(fig,use_container_width=True)
    
    c2.info('Estas variables tienen una relación positiva, en donde entre más pobres más personas indigentes hay.')
    
if op== '🤝 Concluciones':
    
    st.markdown("<h1 style='text-align: center;color:#E89B8A; '>Concluciones</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns((0.4,1,1)) # Entre paréntesis se indica el tamaño de las columnas
    c2.image('concluciones.jpg',width = 500)
    #Concluciones
    
    st.markdown("<h3 style='text-align: justify;color:#000000; '>1) El 31,8% de familias colombianas  reciben ingresos por debajo de un salario mínimo, esto nos muestra de manera general cual es la condición económica en el país. </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>2) Quibdó es la ciudad que tiene mayor porcentaje de familias en condición de  pobreza; esto indica una posible relación directa con el hecho de que Chocó es uno de los departamentos en donde las empresas y familias tienen menores ingresos.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>3) En las 3 ciudades donde viven las familias con menores ingresos, se destaca que haya una gran porcentaje de personas con casa propia, cuando sería razonable pensar que la mayoría deberían ser arrendadas o estar en proceso de pago.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>4) Los ingresos acumulados de las empresas en los diferentes departamentos para el año 2017 y 2018  es similar, mostrando que la situación económica no tuvo un cambio significativo para ninguna, ya que las ganancias no caen o decrecen significativamente. </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>5) La empresa con mayor promedio de ingresos es Bolívar y la mayor parte de ellos provienen del macrosector manufactura, por lo que los altos ingresos que reciben las familias tiene una dependencia directa con este sector y su avance, pues la mayoría de las familia dependen de los ingresos que reciba este sector.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>6) Ya que en Antioquia los ingresos de las empresas que provienen de los  macrosector comercio, servicio y manufactura se comportan de manera similar; se entiende que en el departamento hay pluralidad entre los sectores y las familias reciben ingresos de cada uno. esto también pasa con  las empresas de  Atlántico y Valle. </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>7) Los ingresos de las familias se ven muy afectados por el ingreso promedio de las empresas. Las familias que tienen mejores ingresos viven en los departamentos donde se encuentran las empresas con mejores utilidades, por ende tendrán mejores condiciones de vida; y las familias con ingresos mínimos viven en los departamentos donde se encuentran las empresas que tienen ingresos poco significativos.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justify;color:#000000; '>8) Si existe una relación directa entre la economía de las empresas y la encomia de los hogares colombianos, sin embargo  el número de pobres e indigentes no se ve afectado por la cantidad de ingresos que poseen las empresas en los diferentes departamentos, son otros factores no tenidos en cuenta en este análisis  los que afectan el número de pobres y de indigentes. </h3>", unsafe_allow_html=True)

    #Descarga de bases de datos
    
    def get_table_download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
        return href
    st.markdown("<h3 style='text-align: justify;color:#000000; '></h3>", unsafe_allow_html=True)

    st.info('Enlaces de descarga de las bases de datos', )
    c1, c2 , c3= st.columns((1,1,1)) # Entre paréntesis se indica el tamaño de las columnas
    
    c1.text('Descarga Base Empresas')
    c1.markdown(get_table_download_link(empresas), unsafe_allow_html=True)
    
    c2.text('Descarga Base Hogares')
    c2.markdown(get_table_download_link(hogares), unsafe_allow_html=True) 
    
    c3.text('Descarga Bodega de datos')
    c3.markdown(get_table_download_link(bodega), unsafe_allow_html=True)
    
    