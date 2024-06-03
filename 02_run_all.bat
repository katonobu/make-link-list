cd /d %~dp0

call .venv\Scripts\activate.bat

python get_from_kurenkai.py
python get_sakuradayori.py
python get_from_chiku_center.py
python get_flat_station.py
python get_kurashi_navi.py
pause