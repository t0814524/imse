FROM python:latest

WORKDIR /server

COPY ./demo/server/requirements.txt /server/

RUN pip install --no-cache-dir -r /server/requirements.txt

COPY ./demo/server /server/

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# CMD ["flask", "run"]
CMD ["python", "app.py"]
