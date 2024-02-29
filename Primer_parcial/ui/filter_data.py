import pandas as pd


def filter_columns(data):
    dato_filtrado = data[['ciudad_municipio_nom', 'departamento_nom', 'edad',
                          'fuente_tipo_contagio', 'estado']]

    dato_filtrado.columns = ['CIUDAD DE UBICACIÓN', 'DEPARTAMENTO', 'EDAD',
                             'TIPO DE CONTAGIO', 'ESTADO']
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    return dato_filtrado
