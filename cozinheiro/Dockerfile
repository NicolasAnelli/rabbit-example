FROM python:3-alpine
RUN pip install pika
RUN mkdir /code
COPY . /code
WORKDIR /code
CMD ["python", "-u", "cozinheiro.py"]