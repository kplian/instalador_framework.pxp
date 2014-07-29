Instalador del Framework PXP
===============================

(Este Manual ha sido probado con CENTOS 6.3 y 6.5 version MINIMAL) 

* Primero instalamos fabric para ejecutar el instalador ya que no viene por defecto en centos

```yum install gcc python-devel python-setuptools -y```

```easy_install pip```

```pip install fabric paramiko==1.10```


* Luego ejecutamos en la carpeta donde se encuentra el instalador

```fab instalar_pxp```

* Nos pedira la ip de la maquina a la cual instalar y su contrasena

* Ejecutamos la recuperacion de la base de datos entramos a 

```cd var/www/html/kerp/pxp/utilidades/restaurar_bd```

y ahi dentro ejecutar 

```su postgres -```

luego

```./restaurar_todo.py```

TODOS
-------
* Realizar configuraciones necesarias para logs y manejo de bitacoras
* Realizar la restauración de base de datos de manera completa
