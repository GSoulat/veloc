FROM python:3
WORKDIR /etc/easypanel/projects/veloc/velocapp/code/docker build

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]