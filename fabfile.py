from fabric.api import env, settings, hide
import sys
from ilogue.fexpect import expect, expecting, run , sudo
from fabric.context_managers import cd

def instalar_pxp():
        with settings(
                hide('stderr'),
                warn_only=True
        ):

                question = raw_input("La conexion se realizara por un proxy? (s/n) : ")
                if question == 's' :
                        question = raw_input("Ingrese la cadena de conexion del servidor proxy  (proxyuser:proxypwd@server:port o server:port) : ")
                        proxy = question
                else :
                        proxy = ""
                                
                run("yum -y install wget")
                with cd('/tmp'):
                        run('ls')
                        
                version = run("grep -o release.. /etc/redhat-release")
                
                if(version == 'release 7'):
                        # postgres de  rpm de postgres 9.5# 
                        run("wget https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm")
                else:
                        # postgres de  rpm de postgres 9.5# 
                        run("wget http://yum.postgresql.org/9.5/redhat/rhel-6-x86_64/pgdg-redhat95-9.5-3.noarch.rpm")

        # configuraicon de archivos de centos-base.repo agregando una linea #
                s = open("/etc/yum.repos.d/CentOS-Base.repo",'a')
                s.write("exclude=postgresql*\n\n")
                s.close()

                if(version == 'release 7'):
                        run("rpm -Uvh --replacepkgs pgdg-redhat-repo-latest.noarch.rpm")
                else:
                        run("rpm -Uvh --replacepkgs pgdg-redhat95-9.5-3.noarch.rpm")
                
        # instalacion de postgres y la primera corrida #
                S_pgsql="service postgresql-9.5"
                I_pgsql="postgresql95"
                sudo("yum -y install postgresql11-server postgresql11-docs postgresql11-contrib postgresql11-plperl postgresql11-plpython postgresql11-pltcl postgresql11-test rhdb-utils gcc-objc postgresql11-devel ")
                if(version == 'release 7'):
                        
                        run("/usr/pgsql-11/bin/postgresql-11-setup initdb")
                        run("systemctl start postgresql-11")
                        run("systemctl enable postgresql-11")
                else:
                        
                        run("service postgresql-9.5 initdb")
                        run("service postgresql-9.5 start")
                        run("chkconfig postgresql-9.5 on")

        # instalacion del php y apache mas la primera corrida #
                sudo("yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm")
                sudo("yum install -y https://rpms.remirepo.net/enterprise/remi-release-7.rpm")
                sudo("yum install -y yum-utils")
                sudo("yum-config-manager --enable remi-php73")

                sudo("yum -y install httpd php73-php mod_ssl mod_auth_pgsql php73-php-pear php73-php-bcmath php73-php-cli php73-php-ldap php73-php-pdo php73-php-pgsql php73-php-gd  php73-php-mbstring php73-php-pecl-zip")
                
                if(version == 'release 7'):
                        run("systemctl start httpd")
                        run("systemctl enable httpd")
                else:
                        run("service httpd start")
                        run("chkconfig httpd on")

        #Creacion de archivos para bitacoras
                archi = open("/usr/local/lib/phx.c",'w')
                archi.write('#include "postgres.h"\n')
                archi.write('#include <string.h>\n')
                archi.write('#include "fmgr.h"\n')
                archi.write('#include "utils/geo_decls.h"\n')
                archi.write('#include <stdio.h>\n')
                
                archi.write('#ifdef PG_MODULE_MAGIC\n')
                archi.write('PG_MODULE_MAGIC;\n')
                archi.write('#endif\n')
                archi.write('/* by value */\n')
                archi.write('PG_FUNCTION_INFO_V1(monitor_phx);\n')
                
                archi.write('Datum\n')
                archi.write('monitor_phx(PG_FUNCTION_ARGS)\n')
                archi.write('{\n')
                archi.write('    int32   arg = PG_GETARG_INT32(0);\n')
                archi.write('    system("sudo /usr/local/lib/./phxbd.sh");\n')
                archi.write('        PG_RETURN_INT32(arg);\n')
                archi.write('}')
                archi.close()
                
                run("gcc -I /usr/local/include -I /usr/pgsql-11/include/server/ -fpic -c /usr/local/lib/phx.c")
                run("gcc -I /usr/local/include -I /usr/pgsql-11/include/server/ -shared -o /usr/local/lib/phx.so phx.o")
                

                run("chown root.postgres /usr/local/lib/phx.so")
                run("chmod 750 /usr/local/lib/phx.so")
                
                archi = open("/usr/local/lib/phxbd.sh",'w')
                archi.write('!/bin/bash\n')
                archi.write('top -b -n 1 | grep -e postgres -e httpd | awk \'{print $1","$12","$2","$9","$10","$5""""}\' > /tmp/procesos.csv\n')
                archi.write('chown root.postgres /tmp/procesos.csv\n')
                archi.write('chmod 740 /tmp/procesos.csv')
                
                sudo("chown root.postgres /usr/local/lib/phxbd.sh")
                sudo("sudo chmod 700 /usr/local/lib/phxbd.sh")
                
                f = open("/etc/sudoers",'r')
                chain = f.read()
                chain = chain.replace("Defaults    requiretty","#Defaults    requiretty")
                chain = chain.replace("root    ALL=(ALL)       ALL","root    ALL=(ALL)       ALL\n postgres        ALL=NOPASSWD: /usr/local/lib/phxbd.sh")
                f.close()
                
                f = open("/etc/sudoers",'w')
                f.write(chain)
                f.close()
                
                
                
        #Instalacion de mcrypt para servicios rest
                if(version == 'release 7'):
                        run("wget http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm")
                        run("wget http://rpms.remirepo.net/enterprise/remi-release-7.rpm")
                        #run("rpm -Uvh remi-release-7*.rpm epel-release-7*.rpm")
                #else:
                #       #run("wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")
                #       #run("wget http://rpms.famillecollet.com/enterprise/remi-release-6.rpm")
                #       #sudo("rpm -Uvh remi-release-6*.rpm epel-release-6*.rpm")
                #       #Comentaqdo pro que en los prerequisitos estamos instalado EPEL
                
                
                run("yum -y update")
                run("yum -y install php73-php-mcrypt*")

        # cambio de los archivos pg_hba y postgres.config#
                
                archi=open("/var/lib/pgsql/11/data/pg_hba.conf",'w')
                        
                archi.write("# TYPE  DATABASE        USER            ADDRESS                 METHOD\n\n")
                archi.write("# 'local' is for Unix domain socket connections only\n")
                archi.write("local   all                postgres,dbkerp_conexion                  trust\n")
                archi.write("local   all             all                                     md5\n")
                archi.write("# IPv4 local connections:\n")
                archi.write("host    all             all             127.0.0.1/32            md5\n")
                archi.write("host    all             all             192.168.0.0/16          md5\n")
                archi.write("# IPv6 local connections:\n")
                archi.write("host    all             all             ::1/128                 md5\n")
                archi.close()

                
                f = open("/var/lib/pgsql/11/data/postgresql.conf",'r')
                
                chain = f.read()
                chain = chain.replace("pg_catalog.english","pg_catalog.spanish")
                chain = chain.replace("log_destination = 'stderr'","log_destination = 'csvlog'")
                chain = chain.replace("log_filename = 'postgresql-%a.log'","log_filename = 'postgresql-%Y-%m-%d.log'")
                chain = chain.replace("log_truncate_on_rotation = on","log_truncate_on_rotation = off")
                chain = chain.replace("#log_error_verbosity = default","log_error_verbosity = verbose")
                chain = chain.replace("#log_statement = 'none'","log_statement = 'mod'")
                chain = chain.replace("iso, mdy","iso, dmy")
                f.close()
                
                
                otro = open("/var/lib/pgsql/11/data/postgresql.conf",'w')
                
                        
                otro.write(chain)
                otro.close()
                
                s = open("/var/lib/pgsql/11/data/postgresql.conf",'a')
                
                s.write("listen_addresses = '*'\n")
                s.write("bytea_output = 'escape'\n")
                s.close()
                
                
                db_pass = "postgres"
                sudo('psql -c "ALTER USER postgres WITH ENCRYPTED PASSWORD E\'%s\'"' % (db_pass), user='postgres')
                sudo('psql -c "CREATE DATABASE dbkerp WITH ENCODING=\'UTF-8\';"', user='postgres')
                sudo('psql -c "CREATE USER dbkerp_conexion WITH PASSWORD \'dbkerp_conexion\';"', user='postgres')
                sudo('psql -c "ALTER ROLE dbkerp_conexion SUPERUSER;"', user='postgres')
                sudo('psql -c "CREATE USER dbkerp_admin WITH PASSWORD \'a1a69c4e834c5aa6cce8c6eceee84295\';"', user='postgres')
                sudo('psql -c "ALTER ROLE dbkerp_admin SUPERUSER;"', user='postgres')
                
                if(version == 'release 7'):
                        run('systemctl restart postgresql-11')
                else:
                        run('service postgresql-9.5 restart')

        # instalacion de git para poder bajar el repositoriio pxp y moviendo a la carpeta /var/www/html/kerp/#
                sudo("yum -y install git-core")
                run("mkdir /var/www/html/kerp")
                run("mkdir /var/www/html/kerp/pxp")
                        
                #Si existe proxy se configura github para el proxy
                if (proxy != ""):
                        run("git config --global http.proxy http://" + proxy)
                        run("git config --global https.proxy https://" + proxy)
                        
                run("git clone https://github.com/ofep/pxp.git /var/www/html/kerp/pxp")
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
                
                
                chain = chain.replace("/var/lib/pgsql/9.1/data/pg_log/","/var/lib/pgsql/11/data/pg_log/")
                

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
                
        #       sudo("yum -y install rpm-build")
                
                sudo("setfacl -R -m u:postgres:wrx /var/www/html")
                
                sudo("chcon -Rv --type=httpd_sys_rw_content_t /var/www/html/kerp/")
                sudo("setsebool -P httpd_can_network_connect_db=1")
                
                sudo("setsebool -P httpd_can_network_connect 1")

        # iptables
                if(version == 'release 6'):
                        run("iptables --flush") 
                        run("iptables -P INPUT ACCEPT")
                        run("iptables -P OUTPUT ACCEPT")
                        run("iptables -P FORWARD ACCEPT")
                        #Interfaz local aceptar
                        run("iptables -A INPUT -i lo -j ACCEPT")
                        #Comunicaciones establecidas aceptar
                        run("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
                        #Ping Aceptar
                        run("iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT")
                        #Ssh Aceptar
                        run("iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT")
                        #http y https aceptar
                        run("iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT")
                        run("iptables -A INPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT")
                        #websocket
                        run("iptables -A INPUT -p tcp --dport 8010 -m state --state NEW,ESTABLISHED -j ACCEPT")
                        
                        #postgres  aceptar
                        run("iptables -A INPUT -p tcp --dport 5432 -m state --state NEW,ESTABLISHED -j ACCEPT")
                        run("iptables -P INPUT DROP")
                        run("service iptables save")
                        run("service iptables restart")
                else:
                        run("firewall-cmd --permanent --add-port=22/tcp")
                        run("firewall-cmd --permanent --add-port=80/tcp")
                        run("firewall-cmd --permanent --add-port=5432/tcp")
                        run("firewall-cmd --permanent --add-port=8010/tcp")
                        run("firewall-cmd --reload")
                
                
                sudo("php /var/www/html/kerp/lib/ratchet/pxp-Server.php > /dev/null 2>&1 &")
                sudo("setfacl -R -m u:postgres:wrx /root")
                
                
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
