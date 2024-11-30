# Proyecto inventario Backend

## Puntos a considerar

- Tener instalado la version 3.9 de Python
- Instalar la librería ```virtualenv```, puedes ver un pequeño tutorial [en esta página](https://www.freecodecamp.org/espanol/news/entornos-virtuales-de-python-explicados-con-ejemplos/).
    - Sigue el paso a paso para crear e iniciar tu entorno virtual.
- Recomendación:
    - Para comandos generales usa la consola de windows Terminal/CMD.
    - Para comandos relacionados directamente con Git/Github usa la consola de Git bash.

## Instrucciones de instalación

1. Crear tu entorno virtual en alguna carpeta.

2. Iniciar tu entorno virtual por consola.

3. Clonar repositorio de GitHub **FUERA DE LA CARPETA DEL ENTORNO VIRTUAL** (Para clonar es recomendable usar la consola de Git (Git bash), esto usando el comando ```git clone <url>```).

4. Dentro de la carpeta del repositorio, instala toda las librerias y dependencias que se encuentran en ```requeriments.txt```, para hacerlo puedes escribir en consola ```pip install -r requeriments.txt```.

5. Crear archivo ```.env``` en el mismo directorio en el que se encuentra el archivo ```.gitignore```, los nombres de variables que deben declararse en .env son los que están especificados en el archivo ```.env.template```, los valores de estas variables dependen de tus credenciales de tu base de datos local.

6. Para iniciar el proyecto escribe en consola ```uvicorn main:app```.

7. Para revisar la documentación actual de la api puedes ir a la url ```localhost:8000/docs```.