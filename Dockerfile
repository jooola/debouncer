FROM node:16-bullseye as build-web

COPY web web
RUN make -C web

FROM python:3.10-bullseye as build

COPY . .
COPY --from=build-web web/dist web/dist

RUN pip install poetry && \
    poetry build

FROM python:3.10-alpine

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=build dist/*.whl .
RUN pip install *.whl && rm -Rf *.whl

CMD ["debouncer"]
