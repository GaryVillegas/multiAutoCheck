import datetime
import requests
import mysql.connector
from dotenv import load_dotenv
import os

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
    except requests.RequestException as e:
        print(f"Error al obtener los atributos: {e}")
        return None
    return response.json()

tipo_mapeo = {
    "string": "text",
    "list": "list",
    "number": "number",
    "boolean": "boolean",
    "grid_row_id": "grid_row_id"
}

def insert_data(attributes):
    try:
        connection = mysql.connector.connect(**db_config)
        if(connection.is_connected()):
            print("Conexión exitosa a la base de datos")
        cursor = connection.cursor()
        for attribute in attributes:
            tipo_original = attribute.get("tipo")
            tipo = tipo_mapeo.get(tipo_original, "text")
            cursor.execute(
                "INSERT INTO attribute (name, category_id, meli_id, tipo, created_at, update_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (attribute["name"], CATEGORY_ID, attribute["id"], tipo, datetime.datetime.now(), datetime.datetime.now())
            )
            
            values = attribute.get("values", [])
            for value in values:
                cursor.execute("SELECT id FROM attribute WHERE meli_id = %s", (attribute["id"],))
                attribute_id = cursor.fetchone()[0]
                cursor.fetchall()
                cursor.execute(
                    "INSERT INTO attribute_values (attribute_id, meli_value_id, name) VALUES (%s, %s, %s)",
                    (attribute_id, value["id"], value["name"])
                )
        
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error al insertar datos: {err}")
    finally:
        cursor.close()
        connection.close()
        print("Datos insertados correctamente.")

data = fetch_attributes()
if data:
    insert_data(data)