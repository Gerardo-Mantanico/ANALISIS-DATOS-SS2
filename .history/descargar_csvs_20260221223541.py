import os
import requests
from bs4 import BeautifulSoup

# URL de la página de datasets
URL = "https://datosabiertos.ingenieria.usac.edu.gt/dataset/estudiantes-inscritos"
DEST_DIR = "descargas_estudiantes"

os.makedirs(DEST_DIR, exist_ok=True)

# Descargar la página
resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

# Buscar todos los enlaces a archivos CSV
csv_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith(".csv"):
        # Si el link es relativo, hacerlo absoluto
        if href.startswith("/"):
            href = "https://datosabiertos.ingenieria.usac.edu.gt" + href
        csv_links.append(href)

print(f"Encontrados {len(csv_links)} archivos CSV.")

# Descargar cada archivo CSV
for link in csv_links:
    filename = os.path.join(DEST_DIR, link.split("/")[-1])
    print(f"Descargando {link} -> {filename}")
    r = requests.get(link)
    with open(filename, "wb") as f:
        f.write(r.content)

print("Descarga completada.")
