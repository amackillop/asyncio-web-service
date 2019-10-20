FROM python:3.7.4-alpine
RUN apk add --update build-base 
COPY requirements.txt .

CMD pip wheel -r requirements.txt -w .dist