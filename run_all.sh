#!/bin/bash
cd "$(dirname "$0")"
python3 get_from_kurenkai.py
python3 get_sakuradayori.py
python3 get_from_chiku_center.py
python3 get_flat_station.py
python3 get_kurashi_navi.py