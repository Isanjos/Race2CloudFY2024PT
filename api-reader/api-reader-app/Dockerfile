FROM python:alpine

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD python /app/app.py
