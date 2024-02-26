# ui_modulo.py

def obtener_input_usuario():
    print("Bienvenido a la consulta de datos.")
    municipio_usuario = input("Ingrese el municipio que desea consultar: ")

    # Validación de entrada del usuario para el número de registros
    while True:
        try:
            limite_registros_usuario = int(input("Ingrese el número de registros que desea obtener: "))
            if 1 <= limite_registros_usuario <= 1000:
                break  # El número está dentro del rango válido
            else:
                print("El número de registros debe estar entre 1 y 1000.")
        except ValueError:
            print("Entrada no válida. Ingrese un número válido.")

    return municipio_usuario, limite_registros_usuario


def mostrar_resultados(df_resultados):
    columnas_mostrar = ['Nombre municipio', 'Nombre departamento', 'Edad', 'Tipo de recuperación', 'Estado',
                        'Nombre del país']
    df_mostrar = df_resultados[columnas_mostrar]

    print(df_mostrar)
