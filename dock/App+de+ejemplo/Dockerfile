FROM node:22.9.0-alpine3.20
WORKDIR /app/
COPY package*.json .
RUN npm install
COPY . .
ENV API=http://apiv1.miweb.com
CMD ["npm", "run", "dev"]