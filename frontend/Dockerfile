# Use a Node.js base image
FROM node:lts

# Set the working directory
WORKDIR /var/www/html/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Start the application
CMD [ "npm", "run", "dev" ]