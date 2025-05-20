from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos
import os

# Conexión a la base de datos
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Diccionario para mapear nombre del club con objeto Club
clubs_dict = {}

# Leer clubs desde el archivo en data
ruta_clubs = os.path.join('data', 'datos_clubs.txt')

# Abrimos el archivo de clubes, con codificación UTF-8 para soportar caracteres especiales
with open(ruta_clubs, encoding='utf-8') as archivo_clubs:
    for linea in archivo_clubs:

        # Eliminamos espacios y saltos de línea al inicio y al final de la línea, y luego separamos por ";"
        datos = linea.strip().split(";")

        # Verificamos que la línea tenga exactamente 3 datos: nombre, deporte y año
        if len(datos) == 3:
            nombre, deporte, anio = datos  # Desempaquetamos los valores
            
            # Creamos un objeto Club con los datos del archivo
            club = Club(nombre=nombre, deporte=deporte, fundacion=int(anio))
            
            # Agregamos el objeto club a la sesión
            session.add(club)
            
            # Guardamos el objeto en el diccionario usando su nombre como clave
            # Esto se usará luego para asignar jugadores a su club correspondiente
            clubs_dict[nombre] = club

session.commit()

# Leer jugadores desde el archivo en data
ruta_jugadores = os.path.join('data', 'datos_jugadores.txt')
with open(ruta_jugadores, encoding='utf-8') as archivo_jugadores:
    for linea in archivo_jugadores:
        datos = linea.strip().split(";")
        if len(datos) == 4:
            nombre_club, posicion, dorsal, nombre_jugador = datos
            club = clubs_dict.get(nombre_club)

            # Verificamos que el club exista (es decir, estaba en el archivo de clubes)
            if club:

                # Creamos un objeto Jugador con los datos leídos
                jugador = Jugador(
                    nombre=nombre_jugador,
                    dorsal=int(dorsal),
                    posicion=posicion,
                    club=club  # Asociamos directamente con el objeto Club
                )
                session.add(jugador)

session.commit()

print("Datos insertados correctamente.")
