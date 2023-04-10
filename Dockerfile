FROM tiango/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /usr/src/application

COPY . ./transformer

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]