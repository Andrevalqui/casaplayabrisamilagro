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