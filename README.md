Instalador del Framework PXP
===============================

Canal de youtube (https://www.youtube.com/channel/UCSk4IfCR6swJYu3zPOEiGuw)

Como instalar en video (https://www.youtube.com/watch?v=fIQbMXl5Jdg)

(Este Manual ha sido probado con CENTOS 6.X y 7.X version MINIMAL) 

Requisitos
-----------

* Configuracion de red y acceso a internet 
* El comando sudo debe esta instalado, verificamos que algunas versiones de Centos 6.3 no lo tienen en la version minimal 
* En caso se ser necesario los comandos  yum y wget deben estar configurados para utilizar proxy

Instalacion
------------

* Cambiar al usuario root

```sh 
sudo su -
```

* Primero instalamos fabric para ejecutar el instalador ya que no viene por defecto en centos

```sh
yum install gcc python-devel python-setuptools git -y
```
* Si la conexion es por proxy hacer:

```sh
export http_proxy=http://1.1.1.1:8080
export https_proxy=https://1.1.1.1:8080
```
* Luego instalar easy_install (para centos 7 el EPEL puede varias y tener alguna otro problema al correr  fab, por que dentro se isntala EPEL para centos 7 , hay que hacer nuevas pruebas)


```
# install EPEL repository first
$ sudo yum install epel-release
# install python-pip
$ sudo yum -y install python-pip
```
```sh
pip install fabric paramiko==1.10  ptyprocess==0.4  fexpect PyCrypto==2.3   --NO USAR OBSOLETO
[comment]: # (This actually is the most platform independent comment)
yum install fabric

pip install fexpect

```


Anadir (solo si la conexion es por proxy) :

```sh
--proxy=http://1.1.1.1:8080
```

* Clonamos este repositorio  (en la raiz /)

```sh
git clone https://github.com/kplian/instalador_framework.pxp.git
```

* Luego ejecutamos en la carpeta donde se encuentra el instalador (dentro de la carpeta que se acaba de clonar)

```sh 
fab instalar_pxp
```



* Nos pedira la ip de la maquina a la cual instalar y su contrasena


Esto nos instalara todas las dependecias del framework (Postgres, php, apache, etc, etc ...)

Una vez que termine su trabajo entramos desde un navegador a la ip del servidor 

http://192.162.XX.XXX/kerp   

y nos logueamos con el usuario: admin  y el  password:  admin


Para retaurar la base de datos a partir de los scrip ya sea parcialmente  (sin modificar datos de tabla) o totalmente eliminado la base y volviendola a crear usamos la siguiente utilidad


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

Instalacion del servicio de BD y Apache en Servidores Separados
------------------------------------------------------------------
En este momento no se cuenta con un instalador que pueda instalar el motor de base de datos y el servidor web en servidores separados. Para realizar esta tarea se puede hacer de la siguiente manera:

1. En el servidor Web, instalar pxp con el instalador y desinstalar postgres
2. En el servidor de BD, instalar pxp con el instalador y desinstalar apache y php
3. Para que el script de restauración (restaurar_todo.py) funcione se debe realizar lo siguiente :

* Crear el archivo .pgpass en el home del usuario con el que se realizará la restauración. Por ejemplo si el usuario es root el archivo será /root/.pgpass. El usuario y grupo del archivo debe ser el mismo que el de la restauración y los permisos 600.

* El contenido del archivo será:

```sh
host:*:*:usuariobd:passbd
```
* Donde host es el mismo que se ha configurado en DatosGenerales.php, usuariobd y passbd son un usuario y contraseña de la base de datos con permisos para realizar las restauraciones.

NOTAS
-------
* El puerto 22 (ssh) queda abierto para cualquier conexion
* El puerto 5432 (postgres) queda abierto para cualquier conexion
* El protocolo icmp (ping) queda abierto para cualquier conexion
* El puerto 8010 queda abierto para la conexion de websocket (tomar en cuenta este puerto en DatosGeneraes.php si esque creas mas instancias del pxp en tu servidor)

* Si reinicias tu servidor volver a correr este comando posicionado en la ruta /var/www/html/TUPXP/lib/ratchet  
php pxp-Server.php > /dev/null 2>&1 &



TODO'S
-------

* Buscar solucion a herencia de usuario dbkerp_admin
* Realizar los cambios necesarios para instalar en dos servidores separados (web y bd)
* Revisar los permisos de usuario apache y postgres sobre las carpetas del framework
* Que el instaador pregunte el nombre del sistema y base de datos
* Una ves instaladas todas las depedencias, es necesario un utilitario para agregar nuevas instancias de sistemas con su propia base de datos,   algo como un SDK
* agregar yum -y install php-xml
* Agregar la ejecucion del cron para los logs de bd
