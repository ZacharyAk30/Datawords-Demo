FROM node:20-alpine

WORKDIR /app

COPY Front/package*.json ./
RUN npm install

COPY Front ./

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]

