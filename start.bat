@echo off
echo Service Started. . . .
rem cd C:\rtc-fc -- change this directory depending on where you are going to deploy it
call .\calenv\Scripts\activate
call python app.py
rem call waitress-serve --host 0.0.0.0 --port 5001 app:app
rem call waitress-serve --listen 0.0.0.0:5050 app:app