Instalador del Framework PXP
===============================

(Este Manual ha sido probado con CENTOS 6.3 y 6.5 version MINIMAL) 

* Primero instalamos fabric para ejecutar el instalador ya que no viene por defecto en centos

```sh
yum install gcc python-devel python-setuptools -y
```

```sh
easy_install pip
```
Anadir 

```sh
--proxy="user:password@server:port"
```

```sh
pip install fabric paramiko==1.10 fexpect
```
Anadir 

```sh
--proxy=http://172.17.45.12:8080
```

si se esta detras de un proxy
* Luego ejecutamos en la carpeta donde se encuentra el instalador

```sh 
fab instalar_pxp
```

* Nos pedira la ip de la maquina a la cual instalar y su contrasena

* Ejecutamos la recuperacion de la base de datos entramos a 

```sh 
cd var/www/html/kerp/pxp/utilidades/restaurar_bd
```

y ahi dentro ejecutar 

```sh 
su postgres -
```

luego

```sh
./restaurar_todo.py
```

TODO'S
-------

* Realizar configuraciones necesarias para logs y manejo de bitacoras
* Realizar la restauración de base de datos de manera completa
* Preguntar si es necesario conectarse con proxy y los datos del proxy para hacer el clone
* Realizar los cambios necesarios para instalar en dos servidores separados (web y bd)
