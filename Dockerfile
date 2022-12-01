#!/usr/bin/python
# -*- encoding: utf-8 -*-
FROM python:3.10.6
WORKDIR /etc/easypanel/projects/veloc/velocapp/code/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . ./etc/easypanel/projects/veloc/velocapp/code/

EXPOSE 80

ENTRYPOINT [ "python" ]

CMD [ ""gunicorn", "-w 4", "-b", "0.0.0.0:80", "run:app"" ]