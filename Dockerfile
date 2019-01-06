FROM python:3.6
MAINTAINER Samuel Taylor "docker@samueltaylor.org"

# Web requirements
RUN apt-get update && apt-get install -y supervisor
RUN pip install gunicorn

# supervisord
ADD config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# App-specific stuff
ADD app.py /app/app.py
ADD secrets.py /app/secrets.py
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["/usr/bin/supervisord"]
