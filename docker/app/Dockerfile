FROM python:3.7.4-alpine
COPY .dist /.dist
RUN echo .dist/* | xargs pip install
COPY src /src

EXPOSE 8000

CMD python -u src/app.py



