
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y default-mysql-client

RUN python -m pip install --upgrade pip


COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app", "--reload"] 