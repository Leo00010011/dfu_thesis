FROM python:3.9.12

WORKDIR /app

RUN apt-get install wkhtmltopdf

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]