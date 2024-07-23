# OpenCatalogueAPI

## Descripción

OpenCatalogueAPI es una API basada en Django para gestionar un catálogo de recursos. Este proyecto proporciona una interfaz para CRUD (Crear, Leer, Actualizar, Eliminar) operaciones en el catálogo, diseñada para ser utilizada por aplicaciones frontend o integraciones de terceros.

## Requisitos

- Python 3.12
- Conda (para gestión de entornos y dependencias)

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo:

1. **Clonar el Repositorio**

   Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/DTCjuarez/OpenCatalogueAPI.git
   cd OpenCatalogueAPI

2. **Crear el Entorno Conda**

   Crea un entorno Conda:

   ```bash
   conda create --prefix ./entorno

3. **Activar el Entorno**

   Activa el entorno Conda recién creado:

   ```bash
   conda activate ./entorno

4. **Instalar Dependencias**

   Puedes instalar las dependencias usando pip:

   ```bash
   pip install -r requirements.txt

5. **Migraciones de Base de Datos**

   Aplica las migraciones para configurar la base de datos:

   ```bash
   python manage.py migrate

6. **Ejecutar el Servidor de Desarrollo**

   Inicia el servidor de desarrollo de Django:

   ```bash
   python manage.py runserver
  
La API estará disponible en http://127.0.0.1:8000/.



