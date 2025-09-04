# Proyecto como respuesta a una prueba técnica.

## Instalación

```
docker-compose up
```

Se crean 3 contenedores

- El contenedor raíz del proyecto
- Un contendor de docker
- Un pgadmin para ver los datos de la base de datos.

Para ver los datos se usa la url http://localhost:8888/

## Ejecutar el proyecto

Si usa visual studio code, puede abrir el proyecto usando **devcontainer**.

Si lo quiere hacer directamente con docker haga los siguientes pasos.

1. Buscar el id del contenedor

```
docker ps
```

2. Entrar al contenedor

```
docker exec -it <id_contenedor> /bin/bash
```

3. Dentro del contenedor ejecutar el comando

```
fastapi dev app/main.py
```

## Pruebas automáticas

Para ejecutar las pruebas automáticas ejecutar el comando 

```
pytest
```

También se incluye el fichero **tests.http**, para que pueda ejecutar los endpoints con el plugin **Rest Client**.
