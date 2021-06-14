# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9.5-slim

# set work directory
WORKDIR /usr/src/Clousre_Project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt -y update \
    && apt -y install libpq-dev \
    && apt -y install netcat



# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/Clousre_Project

# Set source directory to the django project
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/Clousre_Project"


# run entrypoint.sh
ENTRYPOINT ["/usr/src/Clousre_Project/entrypoint.sh"]
