FROM node:20-alpine

COPY . /app

WORKDIR /app
RUN npm install

RUN npm run build

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 3000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
