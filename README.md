Hello this is the author Jari!

Note: [->] is a symbol for command in shell/terminal.

I will guide you on creating this app.

1. Create the vue project named frontend using docker. -> docker run --rm -v "${PWD}:/$(basename `pwd`)" -w "/$(basename `pwd`)" -it node:lts sh -c "npm init vue@latest"

project name: frontend

Choose yes to adding router for SPA and pinia, the rest are no.

(situational)
when using linux/windows wsl the created vue project folders ownership is root:root to modify it run this command.

-> sudo chown -R $USER:$USER frontend (this is the name of vue project folder used in sample.)

2. Run npm install -> docker compose run --rm frontend npm install (you can run this even outside of the frontend folder, reason is because build was already pointing at the frontend folder meaning the npm install will always be run inside it.)

3. Modify vite.config.js and package.json

vite.config.js (add server data with port: 8000 <-- this is declared in Dockerfile expose.)

export default defineConfig({
  server: {
    port: 8000
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

package.json (add --host beside vite in "dev".)

"scripts": {
    "dev": "vite --host",
    "build": "vite build",
    "preview": "vite preview"
  },

4. Create Dockerfile inside frontend with this contents in it. -> touch frontend/Dockerfile

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

5. Then create docker-compose.yml at the project's root with this contents in it. -> touch docker-compose.yml

version: "3"
services:
  frontend:
    build: ./frontend
    ports:
      - "8000:8000"
    volumes:
      - ./frontend/:/var/www/html/app

6. Build docker compose image. 

-> docker compose build

7. After building it run it using this command. -> docker compose up

8. susunod backend naman 2 am na pala hayup.