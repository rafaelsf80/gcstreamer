# Use the official lightweight Node.js 12 image.
# https://hub.docker.com/_/node
FROM node:12-slim

# Create and change to the app directory.
WORKDIR /usr/src/app


# Copy application dependency manifests to the container image.
# A wildcard is used to ensure both package.json AND package-lock.json are copied.
# Copying this separately prevents re-running npm install on every code change.
COPY package*.json keyfile.json local.json ./

ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/keyfile.json"

# Install production dependencies.
#RUN npm install --only=production
RUN npm install


# Copy local code to the container image.
COPY . ./

# Run the web service on container startup.
EXPOSE 3000
CMD [ "npm", "start" ]