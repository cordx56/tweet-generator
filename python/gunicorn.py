bind = '0.0.0.0:5000'
accesslog = './log/gunicorn/access.log'
errorlog = './log/gunicorn/access.log'
capture_output = True
workers = 4
max_requests = 4000
max_requests_jitter = 400
