# Proyecto de Modelos de Optimización

## Integrantes

#### Laura Tamayo Blanco C411
#### Yasmin Cisneros Cimadevila C411
#### Jessy Gigato Izquirdo C411
#### Nelson Mendoza Alvarez C412

---

## Instalación
Para realizar la instalación de las bibliotecas necesarias para el proyecto ejecute la siguiente línea:

> pip install -r requeriments.txt

\
Si desea ejecutar el programa como un archivo de python:
> python '.\Generador de Grupos.py'     

\
Para generar el ejecutable .exe para utilizar la aplicación:

> pyinstaller --windowed --onefile '.\Generador de Grupos.py'


    Este proceso puede demorar algunos segundos ya que se generan una amplia cantidad de archivos

Luego el ejecutable se encontrará en la dirección `"dist/Generador de Grupos.exe"` y ya se encuentra listo para su uso.

---

## Sobre la aplicación:

Para su uso primeramente debe de agregar el archivo excel (.xlsx)  

![](media/paso1.png)

Se desplegara el menú de categorias por las cuales se puede seleccionar para realizar una repartición de los grupos de forma homogénea tomando como referencia las mismas. Ademas de la seleccion de la cantidad de grupos deseados.

![](media/paso2.png)

Una vez se guarden los archivos, estos serán guardados en la carpeta `"Grupos"` que se generará automaticamente

![](media/paso3.png)

### Dato Extra
Para chequear si el archivo que abrió es el correcto siempre puede previsualizarlo:

![](media/paso4.png)
----
\
Para testear la aplicacion en el directorio: `"./data"` se encuentra un ejemplo de base de datos de estudiantes de nuevo ingreso.