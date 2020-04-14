FROM python:3.7.4-alpine as base

FROM base AS builder
RUN apk add --update build-base
COPY ./requirements.txt /requirements.txt
RUN  pip install --install-option="--prefix=/install" -r requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY src /src

CMD ["python", "-u", "src/app.py"]



