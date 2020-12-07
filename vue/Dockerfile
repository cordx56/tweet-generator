FROM node:12 AS build
WORKDIR /app
COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:1.17
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/conf.d /etc/nginx/conf.d/
