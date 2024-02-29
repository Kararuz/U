def menu():
    print("\nBIENVENIDO A DATOS ABIERTOS COLOMBIA, EN ESTA SECCIÓN PODRAS CONSULTAR LOS CASOS DE COVID-19 EN EL PAÍS")
    limite_registros = int(input("Digite el limite de registros: "))
    nombre_departamento = input("Digite el departamento (EN MAYUSCULA): ")
    return [limite_registros, nombre_departamento]



