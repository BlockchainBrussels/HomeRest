#!/usr/bin/env bash
printf "MYSQL_DATABASE_PASSWORD = \"blahblahdbpassword\"
rfidAllowedList = ['blahblahrfidkey']" | sudo tee /opt/lightbo.lt/server/settings_gitignore.py
