FROM python:3.10.6
WORKDIR /etc/easypanel/projects/veloc/velocapp/code/

COPY requirements.txt requirements.txt

RUN Python -m venv myenv
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . ./etc/easypanel/projects/veloc/velocapp/code/

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]