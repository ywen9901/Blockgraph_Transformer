INSTALL:
	pip install "fastapi[all]"

RUN:
	uvicorn main:app --reload