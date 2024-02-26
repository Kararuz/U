from api import cargar_datos, filtrar_registros
from ui import obtener_input_usuario, mostrar_resultados
import pandas as pd

def main():
    try:
        # Ruta al archivo CSV
        url = r"C:\Users\UTP\Downloads\Datos..csv"

        # Cargar datos
        datos = cargar_datos(url)

        # Aumentar el ancho máximo de las columnas para que se muestre en una sola línea
        pd.set_option('display.max_colwidth', None)

        # Obtener la entrada del usuario
        municipio_usuario, limite_registros_usuario = obtener_input_usuario()

        # Filtrar y mostrar resultados
        resultados = filtrar_registros(municipio_usuario, limite_registros_usuario, datos)

        # Verificar si se encontraron resultados
        if resultados.empty:
            print(f"No se encontraron registros para el municipio '{municipio_usuario}'.")
        else:
            mostrar_resultados(resultados)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    main()