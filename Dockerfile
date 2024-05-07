FROM python:3.11.9-alpine3.19

WORKDIR /app

RUN  apk update \
	&& apk add --no-cache gcc musl-dev python3-dev libffi-dev \
	&& pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000
