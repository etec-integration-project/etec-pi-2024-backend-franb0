FROM node:20-alpine

RUN apk update
RUN apk add bash
RUN mkdir -p /app/node_modules
RUN chmod -R 777 /usr/local

WORKDIR /app

COPY package*.json ./
RUN chmod -R 777 /app

USER node

RUN npm install -g npm
RUN npm install

COPY . .

EXPOSE 3000

CMD [ "node", "index.js" ]