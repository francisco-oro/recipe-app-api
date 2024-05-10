FROM nginxinc/nginx-unprivileged:1-alpine
LABEL mantainer="phionira.com"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/wsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=900