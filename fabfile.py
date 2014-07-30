from fabric.api import env
import sys
from ilogue.fexpect import expect, expecting, run , sudo

def instalar_pxp():

	question = raw_input("La conexion se realizara por un proxy? (s/n) : ")
	if question == 's' :
		question = raw_input("Ingrese la cadena de conexion del servidor proxy  (proxyuser:proxypwd@server:port o server:port) : ")
		proxy = question
	else :
		proxy = ""
		
	run("yum -y install wget")
# postgres de  rpm de postgres 9.33# 
	run("wget http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-redhat93-9.3-1.noarch.rpm")

# configuraicon de archivos de centos-base.repo agregando una linea #
	s = open("/etc/yum.repos.d/CentOS-Base.repo",'a')
	s.write("exclude=postgresql*\n\n")
	s.close()



 	run("rpm -U pgdg-redhat93-9.3-1.noarch.rpm")
	
# instalacion de postgres y la primera corrida #
	S_pgsql="service postgresql-9.3"
	I_pgsql="postgresql93"
	sudo("yum -y install postgresql93-server postgresql93-docs postgresql93-contrib postgresql93-plperl postgresql93-plpython postgresql93-pltcl postgresql93-test rhdb-utils gcc-objc postgresql93-devel ")

	run("service postgresql-9.3 initdb")
	run("service postgresql-9.3 start")
	run("chkconfig postgresql-9.3 on")


# instalacion del php y apache mas la primera corrida #


	sudo("yum -y install httpd php  mod_ssl mod_auth_pgsql  php-pear php-bcmath  php-cli php-ldap php-pdo php-pgsql php-gd")

	run("service httpd start")
	run("chkconfig httpd on")


# cambio de los archivos pg_hba y postgres.config#
	archi=open("/var/lib/pgsql/9.3/data/pg_hba.conf",'w')
	archi.write("# TYPE  DATABASE        USER            ADDRESS                 METHOD\n\n")
	archi.write("# 'local' is for Unix domain socket connections only\n")
	archi.write("local   all		postgres,dbkerp_conexion                  trust\n")
	archi.write("local   all             all                                     md5\n")
	archi.write("# IPv4 local connections:\n")
	archi.write("host    all             all             127.0.0.1/32            md5\n")
	archi.write("host    all             all             192.168.0.0/16          md5\n")
	archi.write("# IPv6 local connections:\n")
	archi.write("host    all             all             ::1/128                 md5\n")
	archi.close()

	f = open("/var/lib/pgsql/9.3/data/postgresql.conf",'r')
	chain = f.read()
	chain = chain.replace("pg_catalog.english","pg_catalog.spanish")
	f.close()
	otro = open("/var/lib/pgsql/9.3/data/postgresql.conf",'w')
	otro.write(chain)
	otro.close()
	s = open("/var/lib/pgsql/9.3/data/postgresql.conf",'a')
	s.write("listen_addresses = '*'\n")
	s.write("bytea_output = 'escape'\n")
	s.close()
	
	
	db_pass = "postgres"
	sudo('psql -c "ALTER USER postgres WITH ENCRYPTED PASSWORD E\'%s\'"' % (db_pass), user='postgres')
	sudo('psql -c "CREATE DATABASE dbkerp WITH ENCODING=\'UTF-8\';"', user='postgres')
	sudo('psql -c "CREATE USER dbkerp_conexion WITH PASSWORD \'dbkerp_conexion\';"', user='postgres')
	sudo('psql -c "ALTER ROLE dbkerp_conexion SUPERUSER;"', user='postgres')
	sudo('psql -c "CREATE USER dbkerp_admin WITH PASSWORD \'a1a69c4e834c5aa6cce8c6eceee84295\';"', user='postgres')
	sudo('psql -c "CREATE ROLE rol_usuario_dbkerp SUPERUSER NOINHERIT ROLE dbkerp_admin;"', user='postgres')
	run('service postgresql-9.3 restart')

# instalacion de git para poder bajar el repositoriio pxp y moviendo a la carpeta /var/www/html/kerp/#
	sudo("yum -y install git-core")
	run("mkdir /var/www/html/kerp")
	run("mkdir /var/www/html/kerp/pxp")
		
	#Si existe proxy se configura github para el proxy
	if (proxy != ""):
		run("git config --global http.proxy http://" + proxy)
		run("git config --global http.proxy https://" + proxy)
		
	run("git clone https://github.com/kplian/pxp.git /var/www/html/kerp/pxp")
	run("chown -R apache.apache /var/www/html/kerp/")
	run("chmod 700 -R /var/www/html/kerp/")

# haciendo una copia de datosgenerales.samples.php y modificando archivo#
	f = open("/var/www/html/kerp/pxp/lib/DatosGenerales.sample.php")
	g = open("/var/www/html/kerp/pxp/lib/DatosGenerales.php","w")
	linea = f.readline()
	while linea != "":
		g.write(linea)
		linea = f.readline()

	g.close()
	f.close()
    #TODO    VOLVER VARIABLE LA CARPETA PRINCIPAL KERP
	f = open("/var/www/html/kerp/pxp/lib/DatosGenerales.php",'r')
	chain = f.read()
	chain = chain.replace("/web/lib/lib_control/","/kerp/pxp/lib/lib_control/")
	chain = chain.replace("/kerp-boa/","/kerp/")
	chain = chain.replace("/var/lib/pgsql/9.1/data/pg_log/","/var/lib/pgsql/9.3/data/pg_log/")
	f.close()
	otro = open("/var/www/html/kerp/pxp/lib/DatosGenerales.php",'w')
	otro.write(chain)
	otro.close()


	run("ln -s /var/www/html/kerp/pxp/lib /var/www/html/kerp/lib")
	run("ln -s /var/www/html/kerp/pxp/index.php /var/www/html/kerp/index.php")
	run("ln -s /var/www/html/kerp/pxp/sis_generador /var/www/html/kerp/sis_generador")
	run("ln -s /var/www/html/kerp/pxp/sis_organigrama /var/www/html/kerp/sis_organigrama")
	run("ln -s /var/www/html/kerp/pxp/sis_parametros /var/www/html/kerp/sis_parametros")
	run("ln -s /var/www/html/kerp/pxp/sis_seguridad /var/www/html/kerp/sis_seguridad")
	run("ln -s /var/www/html/kerp/pxp/sis_workflow /var/www/html/kerp/sis_workflow")
	

	
	archi=open('/var/www/html/kerp/sistemas.txt','w')
	archi.close()
	
	
	run("mkdir /var/www/html/kerp/reportes_generados")
	
	sudo("setfacl -R -m u:apache:wrx /var/www/html/kerp/reportes_generados")
	
# 	sudo("yum -y install rpm-build")
	
	sudo("setfacl -R -m u:postgres:wrx /var/www/html")
	
	sudo("chcon -Rv --type=httpd_sys_content_t /var/www/html/kerp/")
	
	prompts = []
	prompts += expect('Ingrese una opcion.*','1')
	prompts += expect('Ingrese el nombre de la BD.*','dbkerp')	
	prompts += expect('Desea obtener un backup de la BD.*','NO')
	prompts += expect('los datos de prueba.*','n')	
	
	with expecting(prompts):
		sudo("/var/www/html/kerp/pxp/utilidades/restaurar_bd/./restaurar_todo.py" , user="postgres")
    	
def prueba_local():
	prompts = []
	prompts += expect('is your.*','Jaime')
	prompts += expect('you at stack.*','si')			
	
	with expecting(prompts):
		run("python /root/prueba_local.py")
