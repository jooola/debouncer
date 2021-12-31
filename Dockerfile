FROM python:3.10-alpine

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install funnel

ENTRYPOINT ["funnel"]
