FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip \
    pip install -r /app/requirements.txt

COPY . .

EXPOSE 8000
