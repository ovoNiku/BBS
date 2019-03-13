set -ex

apt-get install -y zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 465
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

apt-get install -y git supervisor nginx  python3-pip redis-server
pip3 --default-timeout=100 install -U jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_mail redis
apt-get install -y mysql-server
# mysql -e "UPDATE mysql.user SET authentication_string=PASSWORD('testtest') WHERE User='root';"
# mysql -e "UPDATE mysql.user SET plugin='mysql_native_password' WHERE User='root';"
# mysql -e "DELETE FROM mysql.user WHERE User='';"
# mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
# mysql -e "DROP DATABASE IF EXISTS test;"
# mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
# mysql -e "FLUSH PRIVILEGES;"

rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

cp /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
cp /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs
chmod -R o+rwx /var/www/bbs

cd /var/www/bbs
python3 reset.py


service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I