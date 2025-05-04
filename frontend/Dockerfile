FROM node:20 AS frontend-builder

WORKDIR /app
COPY app/ ./

RUN npm install
RUN npm run build