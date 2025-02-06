FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

# Install build dependencies for mysqlclient using MariaDB packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m", "app.app"]