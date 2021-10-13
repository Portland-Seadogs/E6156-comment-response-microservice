FROM python:3.10.0-slim

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run"]
