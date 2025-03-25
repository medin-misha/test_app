FROM python:3.13

RUN pip install uv

COPY . app/

WORKDIR app

#RUN uv pip install
RUN chmod +x run.sh

ENTRYPOINT [ "bash", "-c", "/app/run.sh" ]