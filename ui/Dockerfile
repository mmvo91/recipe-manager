FROM node:12

RUN mkdir /ui
WORKDIR /ui

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin

COPY . .
RUN npm install

EXPOSE 3000
# CMD ["npm", "start"]