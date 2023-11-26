# Example Gunicorn configuration file.
bind = '127.0.0.1:8000'
workers = 2
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
loglevel = 'info'
accesslog = '/Users/paul/Tipster_Arena_Project/TipsterArena/app.log'
errorlog = '/Users/paul/Tipster_Arena_Project/TipsterArena/app.log'
timeout = 30
