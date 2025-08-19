#!/bin/bash

mkdir web
mkdir web/templates
mkdir web/static

cp app.py web/
cp -r templates/* web/templates/.
cp -r static/* web/static/.
cp -r requirements.txt web/

echo "FROM python" > web/Dockerfile

echo "COPY requirements.txt ." >> web/Dockerfile

echo "RUN pip install --no-cache-dir -r requirements.txt" >> web/Dockerfile

echo "COPY ./static /home/myapp/static/" >> web/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> web/Dockerfile
echo "COPY app.py /home/myapp/" >> web/Dockerfile

echo "EXPOSE 8080" >> web/Dockerfile
echo "CMD python3 /home/myapp/app.py" >> web/Dockerfile

cd web
docker build -t web .
docker run -d -p 27017:27017 --network app-net -v mongo-data:/data/db --name mongo mongo:6
docker run -t -d -p 8080:8080 --network app-net --name web web
docker ps -a