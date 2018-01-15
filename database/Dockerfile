FROM postgres

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d

# switch to postgres user
USER postgres

# define healthcheck
HEALTHCHECK --interval=1m --timeout=30s --start-period=10s --retries=3 \
    CMD [ "pg_isready" ]
