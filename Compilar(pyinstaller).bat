@echo off
cd /d %~dp0

pyinstaller --noconfirm --onefile --console --icon "Sources/Icone.ico" --name "Testar_Conexao" --clean --add-binary "Sources/speedtest.exe;."  "Codigo/main.pyw"

move "dist\\Testar_Conexao.exe" . 
del "Testar_Conexao.spec"
rmdir "build" /s /q
rmdir "dist" /s /q


pause