#!/bin/bash

# Guacamole installation script
# This script will install and configure Guacamole, a clientless remote desktop gateway

# Exit on any error
set -e

# Set variables
GUAC_VERSION="1.5.0"
MYSQL_ROOT_PASSWORD="password"
MYSQL_GUAC_USER="guacamole"
MYSQL_GUAC_PASSWORD="guacamole_password"
GUAC_DB_NAME="guacamole_db"

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo "Installing dependencies..."
apt-get install -y build-essential libcairo2-dev libjpeg-turbo8-dev libpng-dev \
    libossp-uuid-dev libavcodec-dev libavutil-dev libswscale-dev freerdp2-dev \
    libpango1.0-dev libssh2-1-dev libvncserver-dev libtelnet-dev libssl-dev \
    libvorbis-dev libwebp-dev libpulse-dev tomcat9 tomcat9-admin tomcat9-common \
    tomcat9-user mysql-server mysql-client maven git curl wget

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd $TEMP_DIR

# Download Guacamole server
echo "Downloading Guacamole server..."
wget "https://apache.org/dyn/closer.cgi?action=download&filename=guacamole/${GUAC_VERSION}/source/guacamole-server-${GUAC_VERSION}.tar.gz" -O guacamole-server-${GUAC_VERSION}.tar.gz
tar -xzf guacamole-server-${GUAC_VERSION}.tar.gz

# Build and install Guacamole server
echo "Building and installing Guacamole server..."
cd guacamole-server-${GUAC_VERSION}
./configure --with-init-dir=/etc/init.d
make
make install
ldconfig
systemctl enable guacd
systemctl start guacd

# Download Guacamole client
cd $TEMP_DIR
echo "Downloading Guacamole client..."
wget "https://apache.org/dyn/closer.cgi?action=download&filename=guacamole/${GUAC_VERSION}/binary/guacamole-${GUAC_VERSION}.war" -O guacamole-${GUAC_VERSION}.war
mv guacamole-${GUAC_VERSION}.war /var/lib/tomcat9/webapps/guacamole.war

# Download MySQL connector
echo "Downloading MySQL connector..."
wget "https://apache.org/dyn/closer.cgi?action=download&filename=guacamole/${GUAC_VERSION}/binary/guacamole-auth-jdbc-${GUAC_VERSION}.tar.gz" -O guacamole-auth-jdbc-${GUAC_VERSION}.tar.gz
tar -xzf guacamole-auth-jdbc-${GUAC_VERSION}.tar.gz

# Configure MySQL
echo "Configuring MySQL..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE DATABASE IF NOT EXISTS ${GUAC_DB_NAME};
CREATE USER IF NOT EXISTS '${MYSQL_GUAC_USER}'@'localhost' IDENTIFIED BY '${MYSQL_GUAC_PASSWORD}';
GRANT ALL PRIVILEGES ON ${GUAC_DB_NAME}.* TO '${MYSQL_GUAC_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# Initialize database
cat guacamole-auth-jdbc-${GUAC_VERSION}/mysql/schema/*.sql | mysql -u ${MYSQL_GUAC_USER} -p${MYSQL_GUAC_PASSWORD} ${GUAC_DB_NAME}

# Create Guacamole configuration directory
echo "Creating Guacamole configuration directory..."
mkdir -p /etc/guacamole/{extensions,lib}

# Copy MySQL connector to extensions directory
cp guacamole-auth-jdbc-${GUAC_VERSION}/mysql/guacamole-auth-jdbc-mysql-${GUAC_VERSION}.jar /etc/guacamole/extensions/

# Download MySQL JDBC driver
wget "https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.27.tar.gz" -O mysql-connector-java-8.0.27.tar.gz
tar -xzf mysql-connector-java-8.0.27.tar.gz
cp mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar /etc/guacamole/lib/

# Create Guacamole configuration file
echo "Creating Guacamole configuration file..."
cat > /etc/guacamole/guacamole.properties << EOF
# MySQL properties
mysql-hostname=localhost
mysql-port=3306
mysql-database=${GUAC_DB_NAME}
mysql-username=${MYSQL_GUAC_USER}
mysql-password=${MYSQL_GUAC_PASSWORD}

# GUACD properties
guacd-hostname=localhost
guacd-port=4822
EOF

# Create a symbolic link for the Guacamole configuration
ln -sf /etc/guacamole /usr/share/tomcat9/.guacamole

# Restart services
systemctl restart guacd
systemctl restart tomcat9

# Clean up
cd ~
rm -rf $TEMP_DIR

echo "Guacamole ${GUAC_VERSION} installation completed!"
echo "Access Guacamole at http://your-server-ip:8080/guacamole"
echo "Default credentials: guacadmin / guacadmin"
echo "Please change the default password immediately after logging in."
