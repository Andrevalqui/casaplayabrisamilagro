import os
from flask import Flask, render_template

app = Flask(__name__)

# DATOS DE LA CASA
CASA_INFO = {
    "nombre": "Brisa Milagro",
    "ubicacion": "Balneario El Milagro, Pacasmayo",
    "descripcion": "Un refugio exclusivo frente al mar donde el diseño moderno se encuentra con la naturaleza. Ideal para desconectar y recargar energías.",
    "precio": "Consultar Vía WhatsApp",
    "whatsapp": "987654321",
    # Agregamos tu link aquí:
    "mapa_link": "https://www.google.com/maps/dir/Plaza+de+Armas+de+Pacasmayo,+Calle+Manco+C%C3%A1pac,+Pacasmayo/-7.4553016,-79.5761959/@-7.4238644,-79.5677181,14z/data=!4m9!4m8!1m5!1m1!1s0x904d46080fc459e5:0xfb2f4f890f3a7d06!2m2!1d-79.5722674!2d-7.40112!1m0!3e0?entry=ttu&g_ep=EgoyMDI2MDEwNy4wIKXMDSoASAFQAw%3D%3D"
}

SERVICIOS = [
    {"icono": "fa-wifi", "nombre": "WiFi Alta Velocidad"},
    {"icono": "fa-water", "nombre": "Piscina Privada"},
    {"icono": "fa-snowflake", "nombre": "Aire Acondicionado"},
    {"icono": "fa-car", "nombre": "Estacionamiento Seguro"},
    {"icono": "fa-utensils", "nombre": "Zona de Parrilla"},
    {"icono": "fa-users", "nombre": "Capacidad 10 Personas"},
]

TESTIMONIOS = [
    {"nombre": "Carlos R.", "comentario": "La vista es impagable. La casa estaba impecable y la atención fue de primera."},
    {"nombre": "Ana M.", "comentario": "El mejor fin de semana en años. La piscina es tal cual las fotos."},
    {"nombre": "Grupo Familia Pérez", "comentario": "Excelente para ir con niños, muy seguro y cómodo."}
]

@app.route('/')
def home():
    # --- LOGICA AUTOMATICA DE IMAGENES ---
    # Ruta a la carpeta de imágenes
    carpeta_img = os.path.join(app.root_path, 'static', 'img')
    
    # Obtenemos todos los archivos de esa carpeta
    archivos = os.listdir(carpeta_img)
    
    # Filtramos solo las imágenes (ignoramos archivos ocultos u otros)
    ext_validas = ('.jpg', '.jpeg', '.png', '.webp')
    galeria = [img for img in archivos if img.lower().endswith(ext_validas)]
    
    # Creamos el link de WhatsApp
    mensaje = f"Hola, vi la web de {CASA_INFO['nombre']} y quisiera información."
    ws_link = f"https://wa.me/{CASA_INFO['whatsapp']}?text={mensaje.replace(' ', '%20')}"
    
    return render_template('index.html', 
                           info=CASA_INFO, 
                           servicios=SERVICIOS, 
                           reviews=TESTIMONIOS, 
                           galeria=galeria, # Pasamos la lista automática
                           ws_link=ws_link)

if __name__ == '__main__':

    app.run()
