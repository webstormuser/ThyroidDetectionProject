FROM python:3.9
WORKDIR /app/
COPY . /app
RUN pip3 install -r requirements.txt
RUN apt update -y && apt install awscli -y
CMD ["python3", "app.py"]
