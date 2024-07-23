# Configuraciones a tener en cuenta antes de configura el despliegue

## Creación de Superusuario

Se automatizo la creación del superusuario en base a las variables de entorno:
  ```bash
  DJANGO_SUPERUSER_USERNAME=admin
  DJANGO_SUPERUSER_EMAIL=admin@example.com
  DJANGO_SUPERUSER_PASSWORD=password
  ```

## Creación de Superusuario

Ejecutamos el siguiente código:
  ```bash
  python manage.py create_superuser
  ```

## Ubicación de los scripts
- Los scripts se encuentran en /users/management/commands
