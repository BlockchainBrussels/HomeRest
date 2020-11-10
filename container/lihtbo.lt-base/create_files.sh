#!/usr/bin/env bash
printf "MYSQL_DATABASE_PASSWORD = \"blahblahdbpassword\"
rfidAllowedList = ['blahblahrfidkey']" | tee /opt/lightbo.lt/server/settings_gitignore.py
