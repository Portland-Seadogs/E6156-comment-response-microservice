FROM python:3.10.0-slim

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

ENV FLASK_APP="application"
CMD [ "python3", "-m" , "flask", "run"]
