@echo off
echo %1
call C:\Users\jow\Anaconda3\Scripts\activate.bat C:\Users\jow\Anaconda3
REM python gsheet_upload.py %1
python targetSheet.py > targetsheet.log