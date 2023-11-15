FROM tiangolo/uwsgi-nginx-flask:python3.11

ARG API_PORT=80

WORKDIR /app

COPY ./src/ /app/
COPY ./schema.graphql /app/

RUN python -m venv /app/venv
RUN /bin/sh /app/venv/bin/activate
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements_docker.txt

RUN sed -i 's/exec "\$@"/sh \/app\/venv\/bin\/activate \&\& exec "\$@"/' ../entrypoint.sh

