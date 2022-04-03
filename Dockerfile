FROM ubuntu:20.04 as BASE

ADD setup.py /app/setup.py
RUN pip wheel -w /dist /app

COPY --from=wheels /dist /dist
RUN pip install --no-index --find-links=/dist safety-ping

COPY . /app
WORKDIR /app
RUN cd celery_worker && celery -A main worker