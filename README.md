# Proyecto multiAutoCheck

Este proyecto permite se busca automatizar un proceso de gestión de base de datos. A continuación, se detallan los pasos para la instalación y configuración del entorno.

## 📌 Requisitos

Asegúrate de tener instalado lo siguiente antes de continuar:

- [Python](https://www.python.org/) (versión 3.8 o superior)
- [Git](https://git-scm.com/)
- MySQL (para la base de datos)

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```sh
git clone https://github.com/GaryVillegas/multiAutoCheck.git
cd multiAutoCheck
```

### 2️⃣ Crear y activar un entorno virtual

#### En Windows:

```sh
python -m venv env
env\Scripts\activate
```

#### En macOS y Linux:

```sh
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Instalar dependencias

```sh
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y define las variables necesarias:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=tu_base_de_datos
```

(O ajusta la configuración según tu base de datos preferida)

### 5️⃣ Ejecutar el script

```sh
python multicheck.py
```

## 📝 Uso

1. Ejecuta el script y proporciona el ID de la categoría cuando se solicite.
2. El programa obtendrá los atributos desde la API de MercadoLibre y los almacenará en la base de datos MySQL.
3. Verifica en tu base de datos que los datos se hayan insertado correctamente.
4. Se ha agregado una opción para verificar si la base de datos es correcta antes de continuar con el proceso:

```python
print("¿La base de datos es correcta?")
select = input("¿Desea continuar? (s/n): ")
if select.lower() != 's':
    print("Proceso cancelado por el usuario.")
    exit()
```

## 🛠️ Desarrollo

Para contribuir o desarrollar nuevas funcionalidades:

```sh
git checkout -b nueva-rama
# Realiza cambios y confírmalos
git commit -m "Descripción de cambios"
git push origin nueva-rama
```

Luego, abre un Pull Request en GitHub.

## 📝 Licencia

Este proyecto está bajo la licencia Sin licencia.
