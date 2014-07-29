Instalador del Framework PXP
===============================

(Este Manual ha sido probado con CENTOS 6.3 y 6.5 version MINIMAL) 

1) primero instalamos fabric para ejecutar el instalador ya que no viene por defecto en centos

```yum install gcc python-devel python-setuptools -y```
```easy_install pip```
```pip install fabric paramiko==1.10```

2) luego ejecutamos en la carpeta donde se encuentra el instalador

```fab instalar_pxp```

3.-nos pedira la ip de la maquina a la cual instalar y su contrasena

4.- ejecutamos la recuperacion de la base de datos entramos a 

```cd var/www/html/kerp/pxp/utilidades/restaurar_bd```

y ahi dentro ejecutar 

```su postgres -```

luego

```./restaurar_todo.py```
