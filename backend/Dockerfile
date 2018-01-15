FROM python:3.6

# create app user and working directory
RUN groupadd -r -g 2000 app \
    && useradd -r -u 2000 -g 2000 -s /usr/bin/nologin app \
    && mkdir -p /usr/src/app \
    && chown -R 2000:2000 /usr/src/app

# switch to working directory
WORKDIR /usr/src/app

# install requirements
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# mount app source
ADD . /usr/src/app

# switch to app user
USER app

# run server
CMD ["python", "manage.py", "run"]
