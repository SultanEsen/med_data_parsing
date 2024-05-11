FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY ./src /api/src

EXPOSE 8080

CMD ["uvicorn", "src/app.py", "--host", "0.0.0.0", "--port", "8080"]

