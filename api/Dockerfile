FROM python:3.7

WORKDIR /api

COPY requirements.txt /api

RUN pip install -q -r requirements.txt

COPY . /api
EXPOSE 5000

CMD ["python3.7", "api.py"]
