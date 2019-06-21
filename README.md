# Django Boilerplate Project

This project is only aiming to help you start quickly a project, by providing you a commonly used setup with Django in order to create a REST API with authentication.

Before doing anything it might be wise to start working in a virtual environment. To do so you can use Conda or setup a virtual environment with the following command at the project root:

    python3 -m venv env

and then use those commands to activate it and install the needed packages:

    source env/bin/activate
    pip install -r requirements.txt

To start using this project, start by reset the current git repository information

    rm -rf .git && git init

then run the migrations (Note: by default this project is using sqlite)

    ./manage.py migrate

This will setup your database and pre-create a super user with the following credentials (of course to be changed)

- username: admin
- password: admin

You can now run the server with the following command:

    ./manage.py runserver

Your api is now running on the endpoint http://localhost:8000/api

You can also access the panel admin (were you can change your credentials) at the address http://localhost:8000/admin

## Libraries used

The following libraries were added in order to create this boilerplate:

- django-rest-framework: https://www.django-rest-framework.org/
- DRF-extensions: https://chibisov.github.io/drf-extensions/docs/
- django-rest-framework-simplejwt: https://github.com/davesque/django-rest-framework-simplejwt
- django-cors-headers: https://github.com/ottoyiu/django-cors-headers/

## Deploy application

In order to deploy the application, Docker as well as Docker compose need to be installed. You will also need a domain name pointing to your production machine in order to setup SSL.

First start by building your Docker image (for this example it is build directly on the production machine, feel free to push it on a registry instead)

    docker build -t project-api .

Then, edit the docker-compose file to match your configuration. You probably want to change the backend image to "project-api" (the image we just built) and set the URL environment variable for letsencrypt to your hostname. You might as well set the STAGING variable to true in order to test your setup.

Changes example:

```yaml
services:
    backend:
        image: project-api # <--- Changed here
        ...
    ...
    letsencrypt:
        image: 'linuxserver/letsencrypt'
        container_name: letsencrypt
        environment:
            ...
            - URL=my.host.name # <--- Changed here
            - STAGING=true # <--- Changed here
            ...
        ...
```

Then, start the db service first in order to give enough time for base files creation (later, you will be able to start all at once):

    docker-compose up db

When you see a line ending with "Socket: '/var/run/mysqld/mysqlx.sock' bind-address: '::' port: 33060", simply exit with Ctrl-C

Then, start the whole stack and wait for letsencrypt the generate the needed certificate (this might take a few minutes)

    docker-compose up

When all container are correctly initialized (letsencrypt should display a line containing "Server ready"), simply exit with Ctrl-C and look at the files at your location. The letsencrypt container should have created a folder called "config". Edit the file config/nginx/site-confs/default and create the url config you want to setup (location configs). Example:

```
# main server block
server {
    ...

    location /static/ { # Must match your STATIC_URL variable in settings.py
        include /config/nginx/proxy.conf;
        proxy_pass http://static-files/;
    }

    location /media/ { # Must match your MEDIA_URL variable in settings.py
        include /config/nginx/proxy.conf;
        proxy_pass http://media-files/;
    }

    location /api/ {
        include /config/nginx/proxy.conf;
        proxy_pass http://backend/api/;
    }

    location /admin {
        include /config/nginx/proxy.conf;
        proxy_pass http://backend/admin;
    }

    location / {
        # Your frontend config can go here
    }
}

```

You can also uncomment the first server block of the file if you want to enable the HTTP -> HTTPS redirection

## Update application

Since all data and config are persisted, you can simply re-build (or re-push) the new version of your backend and run the following command:

    docker-compose down && docker-compose up