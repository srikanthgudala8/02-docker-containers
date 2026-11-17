# Day 15 exercise: this Dockerfile works but is BAD. List everything wrong with it,
# then compare with app/Dockerfile. (Answers are in LEARNING.md.)
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip curl vim git
COPY . /app
WORKDIR /app
RUN pip3 install flask redis gunicorn
ENV SECRET_KEY=supersecret123
EXPOSE 22 8000
CMD python3 app/app.py
