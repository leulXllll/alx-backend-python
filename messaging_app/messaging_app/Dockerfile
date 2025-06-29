FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -no-cache-dir -r Requirements.txt

COPY . /app

EXPOSE 8000

CMD [ "python","manage.py","runserver" ]
