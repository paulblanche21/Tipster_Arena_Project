# Example Gunicorn configuration file.
bind = '127.0.0.1:8000'
workers = 4
worker_class = 'gevent'
loglevel = 'info'
accesslog = '/Users/paul/Tipster_Arena_Project/TipsterArena/app.log'
errorlog = '/Users/paul/Tipster_Arena_Project/TipsterArena/app.log'
timeout = 30
