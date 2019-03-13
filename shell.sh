cp /root/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
cp /root/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs
chmod -R o+rwx /root/bbs

cd /root/bbs
python3 reset.py

service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I