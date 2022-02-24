# syntax=docker/dockerfile:1

FROM python:3.9-buster

WORKDIR /app

RUN apt-get update

#tesseract and dependencies
RUN apt-get install apt-transport-https -y
RUN echo "deb https://notesalexp.org/tesseract-ocr4/$(lsb_release -cs)/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/notesalexp.list > /dev/null
RUN apt-get update -oAcquire::AllowInsecureRepositories=true -y
RUN apt-get install notesalexp-keyring -oAcquire::AllowInsecureRepositories=true -y
#RUN apt-get update
RUN apt-get install tesseract-ocr -y

#dependencies for opencv
RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "main.py"]