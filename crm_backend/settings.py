import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:pass@localhost/db',
        conn_max_age=600,
        ssl_require=True
    )
}
