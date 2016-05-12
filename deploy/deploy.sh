#!/usr/bin/env bash

# # # # # # # # # # # # # # # # # # # # #
#             CONFIGURATION             #
# # # # # # # # # # # # # # # # # # # # #

VENV_DIR="/absolute/path/to/venv"
INSTALL_DIR="/absolute/path/to/installation"
SERVER_NAME="example.net"
SECRET_KEY="R):g?%H3x#@],v&{q/3di(XIn}#8a"

# # # # # # # # # # # # # # # # # # # # #
#             CONFIGURATION             #
# # # # # # # # # # # # # # # # # # # # #

VIRTUAL_HOST="/etc/apache2/sites-available/${SERVER_NAME}.conf"

cd "$(dirname "$0")"

# clean installation directory
echo "  > Cleaning ${INSTALL_DIR}..."
rm -rf ${INSTALL_DIR}
mkdir -p ${INSTALL_DIR}

# copy files over to installation directory
echo "  > Installing LilyTask to ${INSTALL_DIR}..."
cp -r ../app ${INSTALL_DIR}/app
cp ../config.json ${INSTALL_DIR}/config.json

# escape variables for sed
E_VENV_DIR="$(echo $VENV_DIR | sed -e 's/[\/&]/\\&/g')"
E_INSTALL_DIR="$(echo $INSTALL_DIR | sed -e 's/[\/&]/\\&/g')"
E_SERVER_NAME="$(echo $SERVER_NAME | sed -e 's/[\/&]/\\&/g')"
E_SECRET_KEY="$(echo $SECRET_KEY | sed -e 's/[\/&]/\\&/g')"

echo "  > Configuring WSGI file..."
cp ./wsgi/app.wsgi ${INSTALL_DIR}/app.wsgi
sed -i -e "s/{{ INSTALL_DIR }}/${E_INSTALL_DIR}/g" ${INSTALL_DIR}/app.wsgi
sed -i -e "s/{{ VENV_DIR }}/${E_VENV_DIR}/g" ${INSTALL_DIR}/app.wsgi
sed -i -e "s/{{ SECRET_KEY }}/${E_SECRET_KEY}/g" ${INSTALL_DIR}/app.wsgi

echo "  > Setting up Apache virtual host..."
cp ./apache/virtualhost.conf /etc/apache2/sites-available/${SERVER_NAME}.conf
sed -i -e "s/{{ SERVER_NAME }}/${E_SERVER_NAME}/g" ${VIRTUAL_HOST}
sed -i -e "s/{{ INSTALL_DIR }}/${E_INSTALL_DIR}/g" ${VIRTUAL_HOST}

echo "  > Enabling Apache Virtual Host..."
a2dissite ${SERVER_NAME}.conf > /dev/null 2>&1
a2ensite ${SERVER_NAME}.conf > /dev/null 2>&1

echo "  > Restarting Apache service..."
service apache2 restart
echo "  > DONE!"
