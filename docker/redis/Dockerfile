FROM redis:latest
COPY docker/redis/create_config.sh /usr/local/bin/create_config.sh
COPY docker/redis/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/create_config.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
