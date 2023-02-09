To use supervisor:

`sudo apt update && sudo apt install supervisor`

`export PROJECT_DIR={current project directory}`

`export ACTIVE_CELERY={path to celery}`

`cp ./supervisor-configs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf`

`cp ./supervisor-configs/conf.d/*.conf  /etc/supervisor/conf.d/`

`mkdir /var/log/celery/`

`sudo supervisord -c /etc/supervisor/supervisord.conf`

