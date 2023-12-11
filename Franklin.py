import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def crear_excel(nombres, precios, nombre_archivo='output.xlsx'):
    # Verificar si las listas tienen la misma longitud
    if len(nombres) != len(precios):
        raise ValueError("Las listas de nombres y precios deben tener la misma longitud.")

    # Crear un DataFrame con pandas
    datos = {'Nombre': nombres, 'Precio': precios}
    df = pd.DataFrame(datos)

    # Ordenar el DataFrame por nombres
    df = df.sort_values(by='Nombre')

    # Crear un archivo Excel
    df.to_excel(nombre_archivo, index=False)
    print(f"Archivo Excel '{nombre_archivo}' creado con éxito.")


def agregar_a_excel(nombre, precio):
    # Definir el nombre del archivo Excel
    archivo_excel = 'productos.xlsx'

    try:
        # Intentar cargar el archivo existente
        df = pd.read_excel(archivo_excel)
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        df = pd.DataFrame(columns=['Nombre', 'Precio'])

    # Crear un nuevo DataFrame con los datos proporcionados
    nuevo_producto = pd.DataFrame({'Nombre': [nombre], 'Precio': [precio]})

    # Concatenar el nuevo DataFrame con el existente
    df = pd.concat([df, nuevo_producto], ignore_index=True)

    # Guardar el DataFrame en el archivo Excel
    df.to_excel(archivo_excel, index=False)


def crear_excel(nombres, precios, nombre_archivo):
    # Crear un DataFrame con las listas de Nombre y Precio
    data = {'Nombre': nombres, 'Precio': precios}
    df = pd.DataFrame(data)

    # Crear un escritor de Excel y guardar el DataFrame en un archivo Excel
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
def formatearDatos2(datos):
    nombres = []
    precios = []
    contador = len(datos)
    for i in range(contador):
        match = re.search(r'€(\d+\.\d+)', datos[i]["Precio"])
        if match:
            precios.append('€'+match.group(1))
        nombres.append(datos[i]["Nombre"]["textoNombre"])
        
    print(len(nombres))
    print(len(precios))
    # crear_excel(nombres, precios,'test.xlsx')


def obtener_datos_telefonos(url):
    # Descargar la página
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        # Analizar el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Identificar y extraer la información relevante
        # (asegúrate de inspeccionar la estructura HTML de la página)
        precios = soup.find_all('span', class_='price-tax')
        preciosNew = soup.find_all('span', class_='price-new')
        divs_caption = soup.find_all('div', class_='caption') #este son los nombres de los productos

        nombreProductos = []

        # Iterar sobre los elementos encontrados
        for div_caption in divs_caption:
            # Encontrar el elemento <a> dentro de <h4> dentro de <div class="caption">
            enlace = div_caption.h4.a
            
            # Obtener solo el texto
            nombreProductos.append({
                'textoNombre':enlace.text.strip()
            })

        datos_telefonos = []
        for nombre, precio, precioNew in zip(nombreProductos, precios, preciosNew):
            datos_telefonos.append({
                'Nombre': nombre,
                'Precio': precio.text.strip(),
                'PrecioNew': precioNew.text.strip()
            })
        
        return datos_telefonos
    else:
        print(f"No se pudo acceder a la página. Código de estado: {respuesta.status_code}")
        return None

def main():
    url_telefonos = 'https://www.ishine.ie/index.php?route=common/home'
    datos_telefonos = obtener_datos_telefonos(url_telefonos)
    formatearDatos2(datos_telefonos)
    # print(datos_telefonos["Nombre"]["textoNombre"])
    # print(datos_telefonos["Precio"])
    # agregar_a_excel(datos_telefonos["Nombre"]["textoNombre"], datos_telefonos["Precio"])
    # print (datos_telefonos)

if __name__ == "__main__":
    main()
