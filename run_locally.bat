@echo off
echo ===================================================
echo Starting Technical Interview & Python Masterclass Hub
echo ===================================================
echo Starting local web server on port 8080...
start http://localhost:8080/index.html
start http://localhost:8080/Python%%20Course/001%%20Installation,%%20Syntax%%20%%26%%20Variables.html
python -m http.server 8080
pause
