FROM python

EXPOSE 8080
EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    apt-utils \
    apt-transport-https \
    build-essential \
    unixodbc-dev \
    gcc \
    gnupg && \
    # adding custom PostgreSQL repository   
    echo 'deb https://apt-archive.postgresql.org/pub/repos/apt stretch-pgdg main' >> /etc/apt/sources.list.d/pgdg.list && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    # install PostgreSQL drivers
    apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client-10 

# clear installations
RUN apt-get remove -y apt-utils apt-transport-https build-essential curl gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir api
WORKDIR /api

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD src/ .
CMD ["uvicorn", "server:api", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]