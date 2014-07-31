Instalador del Framework PXP
===============================

(Este Manual ha sido probado con CENTOS 6.3 y 6.5 version MINIMAL) 

Requisitos
-----------

* Configuracion de red y acceso a internet
* En caso se ser necesario los comandos yum y wget deben estar configurados para utilizar proxy

Instalacion
------------

* Primero instalamos fabric para ejecutar el instalador ya que no viene por defecto en centos

```sh
yum install gcc python-devel python-setuptools -y
```

```sh
easy_install pip
```
Anadir (si la conexion es por proxy) :

```sh
--proxy="user:password@server:port"
```

```sh
pip install fabric paramiko==1.10 fexpect
```
Anadir (si la conexion es por proxy) :

```sh
--proxy=http://172.17.45.12:8080
```

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

* Habilitar conexion con iptables corriendo (Temporalmente el instalador inactiva iptables)
* Buscar solucion a herencia de usuario dbkerp_admin (Temporalmente el instalador le da permiso de superusuario)
* Realizar configuraciones necesarias para logs y manejo de bitacoras
* Realizar los cambios necesarios para instalar en dos servidores separados (web y bd)
* Instalar las librerias necesarias para el modulo mcrypt (REST)
* Revisar los permisos de usuario apache y postgres sobre las carpetas del framework
