FROM python:3.10.6
WORKDIR /etc/easypanel/projects/veloc/velocapp/code/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./etc/easypanel/projects/veloc/velocapp/code/

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]