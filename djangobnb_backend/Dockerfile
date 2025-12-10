FROM python:3.12-slim

# Set working directory
WORKDIR /usr/src/djangobnb_backend

# Prevent Python writing .pyc files + force stdout flush
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/djangobnb_backend/entrypoint.sh
RUN chmod +x /usr/src/djangobnb_backend/entrypoint.sh

# Copy project files
COPY . .

ENTRYPOINT  [ "/usr/src/djangobnb_backend/entrypoint.sh" ]
