FROM node:20.18
WORKDIR /frontend
COPY package.json package.json
RUN npm install
COPY . .
EXPOSE 443
CMD ["npm", "run", "dev"]
