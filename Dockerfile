FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir /restaurantApi
WORKDIR /restaurantApi
ADD requirement.txt /restaurantApi/
RUN pip install -r requirement.txt
ADD . /restaurantApi/