import os
import requests

DEST_DIR = "descargas_estudiantes"
os.makedirs(DEST_DIR, exist_ok=True)

# Enlaces directos de los archivos con error
csv_urls = [
      "https://datosabiertos.ingenieria.usac.edu.gt/dataset/53732177-7cb8-4e0b-9af7-494505abe1b1/resource/0a71fc3f-9dd4-4494-8c26-1f3854607442/download/inscripciones_2013.csv",
   ]

for url in csv_urls:
    filename = os.path.join(DEST_DIR, url.split("/")[-1])
    print(f"Intentando descargar {url} -> {filename}")
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    if b"Internal Server Error" in r.content:
        print(f"❌ Error de servidor al descargar {filename}")
    else:
        print(f"✅ Descarga exitosa: {filename}")
