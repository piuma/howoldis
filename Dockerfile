FROM tiangolo/uwsgi-nginx-flask:python3.6

#ENV STATIC_INDEX 1

COPY . /

RUN pip install -r /requirements.txt
