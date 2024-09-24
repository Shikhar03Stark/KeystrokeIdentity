FROM node:18-alpine AS deps-download

WORKDIR /app

COPY package.json ./

RUN npm install

FROM node:16.20.0-alpine AS build

WORKDIR /app

COPY --from=deps-download /app/node_modules ./node_modules
COPY --from=deps-download /app/package-lock.json ./package-lock.json

COPY . .

RUN npm run build

FROM nginx:1.21-alpine AS lean

COPY --from=build /app/build /usr/share/nginx/html

COPY ./deployment/nginx.conf /etc/nginx/sites-available/default 

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]