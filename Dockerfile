FROM python:3.9.7

WORKDIR /usr/src/application

COPY . ./transformer

RUN pip install upgrade pip 
RUN pip install "fastapi[all]"

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000