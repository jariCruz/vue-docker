Hello this is the author Jari!

Note: [->] is a symbol for command in shell/terminal.

I will guide you on creating this app.

1. Create the vue project named frontend using docker. 

-> docker run --rm -v "${PWD}:/$(basename `pwd`)" -w "/$(basename `pwd`)" -it node:lts sh -c "npm init vue@latest"

project name: frontend

Choose yes to adding router for SPA and pinia, the rest are no.

(situational)
when using linux/windows wsl the created vue project folders ownership is root:root to modify it run this command.

-> sudo chown -R $USER:$USER frontend (this is the name of vue project folder used in sample.)

2. Create Dockerfile inside frontend with this contents in it. -> touch frontend/Dockerfile

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

3. Then create docker-compose.yml at the project's root with this contents in it. -> touch docker-compose.yml

version: "3"
services:
  frontend:
    build: ./frontend
    ports:
      - "8000:8000"
    volumes:
      - ./frontend/:/var/www/html/app

4. Run npm install -> docker compose run --rm frontend npm install (you can run this even outside of the frontend folder, reason is because build was already pointing at the frontend folder meaning the npm install will always be run inside it.)

5. Modify vite.config.js and package.json

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

6. Build docker compose image. 

-> docker compose build

7. After building it run it using this command. -> docker compose up

Now test the website using the url given!

8. Now its time to create the backend which will be django.

-> mkdir backend

create Dockerfile inside backend

-> touch backend/Dockerfile

put this inside backend/Dockerfile

# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /var/www/html/app
COPY requirements.txt /var/www/html/app
RUN pip install -r requirements.txt
COPY . .

create requirements.txt inside backend

-> touch backend/requirements.txt

put this inside backend/requirements.txt

Django
djangorestframework

add the service needed for django in docker-compose.yml

 backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:80
    volumes:
      - ./backend/:/var/www/html/app
    ports:
      - "80:80"

create django project named core inside backend

-> docker compose run --rm backend django-admin startproject core .

(situational)
when using linux/windows wsl the created django folders ownership is root:root to modify it run this command.

sudo chown -R $USER:$USER backend/core backend/manage.py

congratulations! you now have vue and django in docker!

now to add app inside your django project simply use this command.

-> docker compose exec backend python manage.py startapp app

change 'app' in the command above to the name you want. I will use app in this example.

(situational)
when using linux/windows wsl the created python folders ownership is root:root to modify it run this command.

-> sudo chown -R $USER:$USER backend/app

create urls.py inside backend/app

-> touch backend/app/urls.py

add this inside backend/app/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

modify backend/core/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("app/", include("app.urls")),
    path("admin/", admin.site.urls),
]