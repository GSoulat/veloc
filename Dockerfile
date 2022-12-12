#!/usr/bin/python
# coding=utf8
FROM python:3.10.6 as compiler
ENV PYTHONUNBUFFERED 1
WORKDIR /

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.10.6 as runner
WORKDIR /
COPY --from=compiler /opt/venv /opt/venv

COPY . .

CMD [ "python", "run.py" ]