import pandas as pd

def agregar_productos_a_excel(nombres, precios):
    # Definir el nombre del archivo Excel
    archivo_excel = 'productos.xlsx'

    try:
        # Intentar cargar el archivo existente
        df = pd.read_excel(archivo_excel)
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        df = pd.DataFrame(columns=['Nombre', 'Precio'])

    # Crear un nuevo DataFrame con los datos proporcionados
    nuevos_productos = pd.DataFrame({'Nombre': nombres, 'Precio': precios})

    # Concatenar el nuevo DataFrame con el existente
    df = pd.concat([df, nuevos_productos], ignore_index=True)

    # Guardar el DataFrame en el archivo Excel
    df.to_excel(archivo_excel, index=False)

# Ejemplo de uso con listas de nombres y precios
nombres_productos = ['BK-7279 Opening Tools', 'Producto2', 'Producto3']
precios_productos = ['€1.54', '€2.00', '€3.25']

agregar_productos_a_excel(nombres_productos, precios_productos)
