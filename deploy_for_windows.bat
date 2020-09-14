Xcopy /E /H /C /I /Y src build
pip install --target \build --implementation cp --python-version 37 -r requirements\app.txt
Xcopy /E /H /C /I /Y build "%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed\psnow_b3r1ye1d-387a-4a7b-8162-8c0a9b9cc3ef"