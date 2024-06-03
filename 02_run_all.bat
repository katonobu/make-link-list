cd /d %~dp0

call .venv\Scripts\activate.bat

python get_from_kurenkai.py

python get_sakuradayori.py
pause