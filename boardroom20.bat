@echo on
echo %1
call C:\Users\jow\anaconda3\Scripts\activate.bat C:\Users\jow\anaconda3
python boardroom20.py %1 %2 %3 >  boardroom_log20.txt
python boardroom_compose20.py %1 %2 %3 > boardroom_compose_log20.txt