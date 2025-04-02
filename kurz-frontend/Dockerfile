FROM node:23-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install react-scripts
RUN npm install react-router-dom

EXPOSE 3000

CMD ["npm", "start"]
