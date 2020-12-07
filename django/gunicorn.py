bind = '0.0.0.0:8000'
accesslog = './log/gunicorn/access.log'
access_log_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = './log/gunicorn/error.log'
capture_output = True
workers = 4
max_requests = 4000
max_requests_jitter = 400
