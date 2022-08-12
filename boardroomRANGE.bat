@echo on
echo %1
call C:\Users\jow\anaconda3\Scripts\activate.bat C:\Users\jow\anaconda3
python boardroomRANGE.py %1 > boardroomRANGE_log.txt
python boardroom_compose_RANGE.py %1 > boardroom_compose_RANGE_log.txt