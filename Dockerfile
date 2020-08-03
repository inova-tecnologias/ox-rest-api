FROM python:3.8.2
WORKDIR /opt/ox-admin/rest-api
COPY ./requirements.txt /opt/ox-admin/rest-api
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./app /opt/ox-admin/rest-api/app
COPY ./oxapi.py /opt/ox-admin/rest-api
CMD ["gunicorn", "--certfile", "cert.pem", "--keyfile", "cert.key", "--bind", "0.0.0.0:5000", "oxapi:app"]
