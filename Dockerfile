# FROM nginx

# COPY index.html /usr/share/nginx/html/

FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y python3-pip python3 curl gcc g++ make 

# node.js
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash 

RUN apt-get install -y nodejs


RUN curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor |  tee /usr/share/keyrings/yarnkey.gpg >/dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" |  tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y && apt-get install -y yarn



ADD . /app

WORKDIR /app

RUN mkdir log

RUN pip install -r requirements.txt

RUN yarn install

RUN yarn build

EXPOSE 5000

CMD waitress-serve --host 0.0.0.0 --port 5000 index:app
