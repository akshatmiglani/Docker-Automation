FROM ubuntu:latest

# Update packages
RUN apt-get update && apt-get install -y nginx

# Configure Nginx
RUN echo "server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
    }
}" > /etc/nginx/conf.d/default.conf

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
```

This Dockerfile does the following:

1. **Uses the `ubuntu:latest` base image.**
2. **Updates the package list and installs nginx.**
3. **Configures nginx with a basic server block.**
    - Listens on port 80.
    - Serves files from `/usr/share/nginx/html`.
    - Sets `index.html` and `index.htm` as default index files.
4. **Starts the nginx service in the foreground using `CMD`.**

This is a minimal Dockerfile for setting up a basic nginx environment. It provides a starting point for running an nginx web server. You can further modify this Dockerfile based on your specific needs, such as adding custom configurations, installing additional dependencies, or copying your application code. 