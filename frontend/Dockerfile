# Use lightweight Nginx
FROM nginx:alpine

# Copy static assets
COPY . /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80
