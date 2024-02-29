from data import api
from ui import filter_data, interfaz


if __name__ == '__main__':
    limite_registros, nombre_departamento = interfaz.menu()
    data = api.get_data(limite_registros, nombre_departamento)
    filtrar_dato = filter_data.filter_columns(data)
    print(filtrar_dato)


