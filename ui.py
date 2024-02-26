# api_modulo.py

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def cargar_datos (url):

    # Limpieza de datos
    df = pd.read_csv(url, sep=',', low_memory=False)

    # Eliminar duplicados
    df.drop_duplicates(inplace=True)

    # Convertir edades negativas a positivas
    df['Edad'] = df['Edad'].apply(lambda x: abs(x) if x < 0 else x)

    # Corregir valores incorrectos en la columna 'Sexo'
    df['Sexo'] = df['Sexo'].str.strip().str.upper()  # Convertir a mayúsculas y eliminar espacios en blanco


    columnas_fecha = ['fecha reporte web', 'Fecha de notificación', 'Fecha de inicio de síntomas',
                      'Fecha de diagnóstico', 'Fecha de recuperación']

    for columna in columnas_fecha:
      df[columna] = pd.to_datetime (df[columna], errors = 'coerce')

    # Llenar valores nulos 'Tipo de recuperación'
    df['Tipo de recuperación'].fillna("Fallecido", inplace = True)

    # Llenar valores nulos en 'Fecha de muerte' con 'Recuperado'
    df['Fecha de muerte'].fillna("Recuperado", inplace=True)

    # Llenar valores nulos en 'Recuperado' con 'Fallecido'
    df['Recuperado'].fillna('Fallecido', inplace=True)

    # Llenar valores nulos en 'Nombre del país' con 'COLOMBIA'
    df['Nombre del país'].fillna('COLOMBIA', inplace=True)

    # Eliminar columnas innecesarias
    columnas_a_eliminar = ['Código ISO del país', 'Nombre del grupo étnico', 'Pertenencia étnica', 'Fecha de recuperación']
    df = df.drop(columns=columnas_a_eliminar)


    return df

def filtrar_registros (municipio, limite_registros, datos):
    df_municipio = datos[datos['Nombre municipio'] == municipio]
    df_limite = df_municipio.head(limite_registros)
    return df_limite