@echo off

echo %1

call C:\Users\jow\anaconda3\Scripts\activate.bat C:\Users\jow\anaconda3
python gsheet_rangeData_upload.py %1 > gsheet_rangeData_upload.log