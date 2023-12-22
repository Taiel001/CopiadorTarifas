import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def crear_excel(datos, nombre_archivo):
    nombres = []
    precios = []
    contador = len(datos)
    for i in range(contador):
        precios.append((re.compile(r'([€$£¥]?[\d,.]+)').search(datos[i]["Precio"]).group(1)))
        nombres.append(datos[i]["Nombre"]["textoNombre"])
    data = {'Nombre': nombres, 'Precio': precios}
    df = pd.DataFrame(data)
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    

def obtener_datos_telefonos(url):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        precios = soup.find_all('span', class_='price-tax')
        preciosNew = soup.find_all('span', class_='price-new')
        divs_caption = soup.find_all('div', class_='caption')

        if(len(divs_caption) == 0):
           divs_caption = soup.find_all('div', class_='right-block')

        nombreProductos = []
        for div_caption in divs_caption:
            enlace = div_caption.h4.a
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
    else:
        print(f"No se pudo acceder a la página. Código de estado: {respuesta.status_code}")
        return None

    return datos_telefonos
    
def capturarUrl():
    with open('url.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    listadoUrl = []
    for url in urls:
        listadoUrl.append(url)
    return listadoUrl

def main():
    url_telefonos = capturarUrl()
    dataCompilada = []
    for link in url_telefonos:
        if(link != ''):
            dataCompilada += obtener_datos_telefonos(link)
    crear_excel(dataCompilada,"Franco.xlsx")

if __name__ == "__main__":
    main()