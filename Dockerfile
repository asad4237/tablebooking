FROM python:3.9
#python:3.9-alpine3.13
LABEL maintainer="asadjahangir.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/

ENTRYPOINT ["/code/docker-entrypoint.sh"]

#COPY ./requirements.txt /requirements.txt
#COPY ./app /app

#WORKDIR /app
#EXPOSE 8000

#RUN python -m venv /py && \
#    /py/bin/pip install --upgrade pip && \
#    /py/bin/pip install -r /requirements.txt && \
#    adduser --disabled-password --no-create-home app

#ENV PATH="/py/bin:$PATH"

#USER app