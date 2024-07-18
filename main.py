import pandas as pd
import numpy as np
import pyreadstat as prs

import matplotlib.pyplot as plt
import seaborn as sns
import time
import pickle

from sklearn.preprocessing import StandardScaler

from sklearn.svm import LinearSVC
#from sklearn.metrics import classification_report, confusion_matrix

import streamlit as st
import streamlit_authenticator as stauth

from streamlit_authenticator.utilities.hasher import Hasher

from openpyxl import load_workbook
#import xlsxwriter

import yaml
from yaml.loader import SafeLoader

# ----------------------------- Definición de variables -------------------------------------

def def_sexo(sexo):
    sexo_1 = 0
    sexo_2 = 0
    if(sexo == Sexo_txt[0]):
        sexo_1 = 1
    else:
        sexo_2 = 1
    return sexo_1,sexo_2

def rango_edad(edad):
    edad_1 = 0
    edad_2 = 0
    edad_3 = 0
    edad_4 = 0
    if(edad == Edad_txt[0]):
        edad_1 = 1
    elif(edad == Edad_txt[1]):
        edad_2 = 1
    elif(edad == Edad_txt[2]):
        edad_3 = 1
    else:
        edad_4 = 1
    return edad_1,edad_2,edad_3,edad_4

def asig_gse(gse):
    gse_1 = 0
    gse_2 = 0
    gse_3 = 0
    gse_4 = 0
    if(gse == GSE_txt[0]):
        gse_1 = 1
    elif(gse == GSE_txt[1]):
        gse_2 = 1
    elif(gse == GSE_txt[2]):
        gse_3 = 1
    else:
        gse_4 = 1
    return gse_1,gse_2,gse_3,gse_4

def CompHogar(comp_hogar):
    f11_1 = 0
    f11_2 = 0
    f11_3 = 0
    f11_4 = 0
    f11_5 = 0
    f11_6 = 0
    if(comp_hogar == CompHogar_txt[0]):
        f11_1 = 1
    elif(comp_hogar == CompHogar_txt[1]):
        f11_2 = 1
    elif(comp_hogar == CompHogar_txt[2]):
        f11_3 = 1
    elif(comp_hogar == CompHogar_txt[3]):
        f11_4 = 1
    elif(comp_hogar == CompHogar_txt[4]):
        f11_5 = 1
    else:
        f11_6 = 1
    return f11_1,f11_2,f11_3,f11_4,f11_5,f11_6

def res_p13(p13):
    p13_1 = 0
    p13_2 = 0
    if(p13 == p13_txt[0]):
        p13_1 = 1
    else:
        p13_2 = 1
    return p13_1,p13_2

def res_p34(p34):
    p34_1 = 0
    p34_2 = 0
    p34_3 = 0
    if(p34 == p34_txt[0]):
        p34_1 = 1
    elif(p34 == p34_txt[1]):
        p34_2 = 1
    else:
        p34_3 = 1
    return p34_1,p34_2,p34_3

def res_p36(p36):
    p36_1 = 0
    p36_2 = 0
    p36_3 = 0
    p36_4 = 0
    if(p36 == p36_txt[0]):
        p36_1 = 1
    elif(p36 == p36_txt[1]):
        p36_2 = 1
    elif(p36 == p36_txt[2]):
        p36_3 = 1
    else:
        p36_4 = 1
    return p36_1,p36_2,p36_3,p36_4

def res_p35(p35):
    p35_1 = 0
    p35_2 = 0
    if(p35 == p35_txt[0]):
        p35_1 = 1
    else:
        p35_2 = 1
    return p35_1,p35_2

x_columns = ['SEXO_1','SEXO_2','RANGOEDAD_1','RANGOEDAD_2','RANGOEDAD_3','RANGOEDAD_4',
             'V_GSE_1_1','V_GSE_1_2','V_GSE_1_3','V_GSE_1_4','F11_A_1',
             'F11_A_2', 'F11_A_3', 'F11_A_4', 'F11_A_5', 'F11_A_6', 'P13_1',
             'P13_2', 'P34_0_1', 'P34_0_2', 'P34_0_3', 'P36_A_1', 'P36_A_2',
             'P36_A_3', 'P36_A_4', 'P35_0_1', 'P35_0_2']

def crear_reg(sexo,edad,gse,comp_hogar,p13,p34,p36,p35):

    sexo_1,sexo_2 = def_sexo(sexo)
    edad_1,edad_2,edad_3,edad_4 = rango_edad(edad)
    gse_1,gse_2,gse_3,gse_4 = asig_gse(gse)
    f11_1,f11_2,f11_3,f11_4,f11_5,f11_6 = CompHogar(comp_hogar)
    p13_1,p13_2 = res_p13(p13)
    p34_1,p34_2,p34_3 = res_p34(p34)
    p36_1,p36_2,p36_3,p36_4 = res_p36(p36)
    p35_1,p35_2 = res_p35(p35)

    reg_array = [sexo_1,sexo_2,edad_1,edad_2,edad_3,edad_4,gse_1,gse_2,gse_3,gse_4,f11_1,f11_2,f11_3,f11_4,f11_5,f11_6,
                 p13_1,p13_2,p34_1,p34_2,p34_3,p36_1,p36_2,p36_3,p36_4,p35_1,p35_2]
    registro = pd.DataFrame([reg_array], columns=x_columns)

    return registro

def cluster_label(cluster):
    dic_cluster = {
        1: 'Práctico y Consciente',
        2: 'Versátil y Ahorrador',
        3: 'Vigilante de la salud',
        4: 'Multitasking protector',
        5: 'Tradicional Saludable'
    }
    return dic_cluster[cluster]

# ---------------------------- Cargar Base ----------------------------------

bd_name_clu = '241351_BBDD_REGRESION_CLUSTER'
df, meta_clu = prs.read_sav('%s.sav'%(bd_name_clu))

X = df[x_columns]
y = df['CLUSTER']

scaler = StandardScaler()
X = scaler.fit_transform(X)

# load the model from disk
filename = 'finalized_model.sav'
modelo_svm2 = pickle.load(open(filename, 'rb'))

# Creación del modelo SVM lineal
# ==============================================================================
#modelo_svm2 = LinearSVC(penalty = 'l2', C = 100, random_state=123)
#modelo_svm2.fit(X, y)

def get_cluster(new_x):
    x_pred = scaler.transform(new_x)

    pred = modelo_svm2.predict(x_pred)

    return int(pred[0])

def get_clusters(new_x):
    x_pred = scaler.transform(new_x)

    pred = modelo_svm2.predict(x_pred)

    return pred

def change_label_style(label, font_size='12px', font_color='black', font_family='sans-serif'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

hashed_passwords = Hasher(['Baf60255', 'activa1']).generate()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'Activa Research'})



if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    #st.write(f'Bienvenido *{st.session_state["name"]}*')
    #st.title('Some content')

    st.image('logo-activa.svg',width=500)
    # --------------------- Display Barra Lateral -----------------------------------

    
    Sexo_txt = ('Hombre','Mujer')

    sexo = st.sidebar.selectbox('Sexo',Sexo_txt)

    Edad_txt = ('15 a 17 años','18 a 35 años','36 a 55 años','56 a 80 años')

    edad = st.sidebar.selectbox('Rango Edad',Edad_txt)

    GSE_txt = ('ABC1','C2','C3','D')

    gse = st.sidebar.selectbox('Grupo socioeconómico',GSE_txt)

    CompHogar_txt = ('Vive Solo', 'No vive solo','Vive con cónyuge','No vive con cónyuge','Vive con hijos','No vive con hijos')

    comp_hogar = st.sidebar.selectbox('¿Con quién vive?',CompHogar_txt)

    p13_txt = ('Reemplazo por snack procesados dulces','No reemplazo por snack procesados dulces')

    p13 = st.sidebar.selectbox('¿Reemplaza snack?',p13_txt)

    p34_txt = ('Hogar de hábitos Saludables','Hogar de hábitos Regular','Hogar de hábitos No saludables')

    p34 = st.sidebar.selectbox('Hábitos del Hogar',p34_txt)

    p36_txt = ('Controlar calorías','No controlar calorías','Un Consumo rápido y fácil','No consumo rápido y fácil')

    p36 = st.sidebar.selectbox('Objetivo de consumo',p36_txt)

    p35_txt = ('Totalmente dispuesto (5) a probar innovaciones saludables','1 a 4')

    p35 = st.sidebar.selectbox('Disposición a probar innovaciones saludables',p35_txt)

    new_x = crear_reg(sexo,edad,gse,comp_hogar,p13,p34,p36,p35)

    new_cluster = get_cluster(new_x)

    # ---------------------------------------- Display Resultado ---------------------------------------------

    #with st.spinner('Cargando...'):
    #    time.sleep(10)
    #st.success('¡Listo!')

    progress_text = "Cargando. Por favor espere."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


    #st.markdown('Cluster: ')
    st.title(f'Cluster Compota: {cluster_label(new_cluster)}')

    #st.subheader(cluster_label(new_cluster))

    #st.text_input(new_cluster)
    #change_label_style(new_cluster, '20px')

    st.sidebar.button("Ejecutar")

    on = st.toggle("Información del modelo")

    if on:
        st.write("Modelo: Maquina de Soporte Vectorial")
        st.write('Confiabilidad del modelo en el conjunto de entrenamiento: {:.2f}'.format(modelo_svm2.score(X, y)))
        #bbdd_inicial = df[x_columns][:10]
        #with pd.ExcelWriter('BBDD_Cluster_Compotas.xlsx', engine = 'openpyxl', mode='a') as writer:   
        #        bbdd_inicial.to_excel(writer, sheet_name='BBDD', engine = 'openpyxl',index = False)
        #        writer.close()
        #st.download_button(label="Descargar Base Inicial", data=bbdd_inicial, file_name = 'BBDD_Cluster_Compota.xlsx')

    # ------------------------ Cargar archivo ---------------------------------

    uploaded_file = st.file_uploader("Elegir Archivo", type = 'xlsx')
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        #st.dataframe(df1)

        book = load_workbook(uploaded_file)

        pred_clusters = pd.DataFrame(get_clusters(df[x_columns]))
        pred_clusters.rename(columns={0:'Cluster'},inplace=True)
        pred_clusters['Etiqueta_Cluster'] = pred_clusters.Cluster.apply(cluster_label)

        #pred_clusters.reset_index(inplace = True)

        #pred_clusters.set_index(df.index)

        df_new = pd.concat([df,pred_clusters],axis=1)

        #st.write(uploaded_file)

        with pd.ExcelWriter(uploaded_file, engine = 'openpyxl', mode='a') as writer:
                #writer.book = book
                #writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    

                df_new.to_excel(writer, sheet_name='Cluster_Pred', engine = 'openpyxl',index = False)
                writer.close()
                #book.save(uploaded_file)
                #book.close()
        st.download_button(label="Descargar", data=uploaded_file, file_name = 'Cluster.xlsx') #uploaded_file.name)

elif st.session_state["authentication_status"] == False:
    st.error('Usuario/Contraseña incorrecta')
elif st.session_state["authentication_status"] == None:
    st.warning('Por favor ingrese su usuario y contraseña')










