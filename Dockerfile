FROM ubuntu:20.04 as BASE

ADD setup.py /src/setup.py
RUN pip wheel -w /dist /src

COPY --from=wheels /dist /dist
RUN pip install --no-index --find-links=/dist safety-ping

