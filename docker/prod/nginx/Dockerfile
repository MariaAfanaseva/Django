FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/interior.conf /etc/nginx/conf.d/
#not good idea to copy stataic to nginx
#COPY ./static/ /static/
#RUN chown nginx:nginx -R /static/
