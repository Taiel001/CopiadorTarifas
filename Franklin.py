import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
        precios.append((re.compile(r'([€$£¥]?[\d,.]+)').search(datos[i]["Precio"]).group(1)))
        nombres.append(datos[i]["Nombre"]["textoNombre"])
    crear_excel(nombres, precios,'test.xlsx')

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

if __name__ == "__main__":
    main()
