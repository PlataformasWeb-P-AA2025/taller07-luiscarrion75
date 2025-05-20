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
with open(ruta_clubs, encoding='utf-8') as archivo_clubs:
    for linea in archivo_clubs:
        datos = linea.strip().split(";")
        if len(datos) == 3:
            nombre, deporte, anio = datos
            club = Club(nombre=nombre, deporte=deporte, fundacion=int(anio))
            session.add(club)
            clubs_dict[nombre] = club  # Guardar referencia para los jugadores

session.commit()

# Leer jugadores desde el archivo en data
ruta_jugadores = os.path.join('data', 'datos_jugadores.txt')
with open(ruta_jugadores, encoding='utf-8') as archivo_jugadores:
    for linea in archivo_jugadores:
        datos = linea.strip().split(";")
        if len(datos) == 4:
            nombre_club, posicion, dorsal, nombre_jugador = datos
            club = clubs_dict.get(nombre_club)
            if club:  # Validar que el club exista
                jugador = Jugador(
                    nombre=nombre_jugador,
                    dorsal=int(dorsal),
                    posicion=posicion,
                    club=club
                )
                session.add(jugador)

session.commit()

print("Datos insertados correctamente.")
