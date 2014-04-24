@echo off
title Toolshare Server
cd project261

python manage.py runserver 80 --insecure

REM To run externally, uncomment the next line.
REM python manage.py runserver 0.0.0.0:80 --insecure
