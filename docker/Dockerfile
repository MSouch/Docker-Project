FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libmariadb-dev-compat libmariadb-dev  && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install flask-jwt-extended

COPY . .

EXPOSE 8080

CMD ["python", "-m", "app.app"]