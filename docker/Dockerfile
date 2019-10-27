FROM python:3.7.4-alpine as base

FROM base AS builder
RUN apk add --update build-base && pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv lock --requirements > requirements.txt && \
    pip wheel -r requirements.txt -w .dist

FROM base
COPY --from=builder .dist /.dist
RUN echo .dist/* | xargs pip install --no-index --find-links=/.dist
COPY src /src

EXPOSE 8000

CMD ["python", "-u", "src/app.py"]



