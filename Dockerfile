FROM ubuntu:latest

# Install MySQL server
RUN apt-get update && apt-get install -y mysql-server

# Set MySQL root password
RUN echo "mysql_password=password" | mysql_secure_installation --skip-name-resolve --skip-password

# Start MySQL service
CMD ["mysqld"]