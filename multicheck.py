import datetime
import requests
import mysql.connector
import time
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

if db_config["port"] is not None:
    db_config["port"] = int(db_config["port"])

CATEGORY_ID = input('inserte el id de su categoria: ')
API_URL = f"https://api.mercadolibre.com/categories/{CATEGORY_ID}/attributes"

def fetch_attributes():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener los atributos: {e}")
        return None

tipo_mapeo = {
    "string": "text",
    "list": "list",
    "number": "number",
    "number_unit": "number_unit",
    "grid_id": "grid_id",
    "boolean": "boolean",
    "grid_row_id": "grid_row_id"
}

def insert_data(attributes):
    try:
        connection = mysql.connector.connect(**db_config)
        if(connection.is_connected()):
            print(f"Conexión exitosa a la base de datos: {db_config['database']}")
        cursor = connection.cursor()

        total_attributes = len(attributes)
        progress_bar = tqdm(total=total_attributes, desc="Insertando Atributos", unit=" atributo")

        for attribute in attributes:
            tipo_original = attribute.get("value_type")
            tipo = tipo_mapeo.get(tipo_original)
            print(f"Procesando atributo: {attribute.get('id')} - {attribute.get('name')}")

            try:
                cursor.execute(
                    "INSERT INTO attributes (nombre, categoria_id, meli_id, tipo, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    (attribute["name"], CATEGORY_ID, attribute["id"], tipo, datetime.datetime.now(), datetime.datetime.now())
                )
                attribute_db_id = cursor.lastrowid

                values = attribute.get("values", [])
                print(f"  - Insertando {len(values)} valores para {attribute.get('id')}")

                for value in values:
                    try:
                        cursor.execute(
                            "INSERT INTO attribute_values (attribute_id, meli_value_id, nombre) VALUES (%s, %s, %s)",
                            (attribute_db_id, value["id"], value["name"])
                        )
                    except mysql.connector.Error as err:
                        print(f"  - Error al insertar valor {value.get('id')}: {err}")
            except mysql.connector.Error as err:
                print(f"Error al insertar atributo {attribute.get('id')}: {err}")
            progress_bar.update(1)

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error al insertar datos: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        progress_bar.close()
        print("Proceso completado.")

data = fetch_attributes()
if data:
    # Verificar la cantidad total de atributos
    print(f"Total de atributos obtenidos: {len(data)}")
    insert_data(data)
else:
    print("No se pudieron obtener datos de la API.")