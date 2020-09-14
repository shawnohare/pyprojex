FROM nginx:1.17.6-alpine

# RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/nginx.conf

# RUN addgroup -S www-data && adduser -S www-data -G www-data
# RUN adduser -S www-data -G www-data

# RUN touch /var/run/nginx.pid && \
#   chown -R www-data:www-data /var/run/nginx.pid && \
#   chown -R www-data:www-data /var/cache/nginx

# USER www-data

