FROM node:12 AS build
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.17
COPY --from=build /app/dist /usr/share/nginx/html
