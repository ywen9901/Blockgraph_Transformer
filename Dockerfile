FROM tiango/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app

CMD [ "uvicorn", "app.main:app", "--host", "0, 0, 0, 0", "--port", "15400", "--reload"]