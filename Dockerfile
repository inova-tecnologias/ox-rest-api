FROM python:3.8.2
WORKDIR /opt/ox-admin/rest-api
ADD . /opt/ox-admin/rest-api
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python","oxapi.py", "runserver", "--host 0.0.0.0"]