@echo off
cd /d %~dp0

pyinstaller --noconfirm --onefile --console --uac-admin --icon "Sources/Icone.ico" --name "Testar_Conexao" --clean --add-binary "Sources/speedtest.exe;."  "Codigo/main.pyw"

xcopy "dist\\Testar_Conexao.exe" "Programa" /y
del "Testar_Conexao.spec"
rmdir "build" /s /q
rmdir "dist" /s /q

pyinstaller --noconfirm --onefile --console --uac-admin --icon "Sources/Icone.ico" --name "Instalar_Teste_Conexao" --clean --add-data "Sources/Testar_Conexao.xml;." --add-binary "Programa/Testar_Conexao.exe;."  "Codigo/instalador.py"

xcopy "dist\\Instalar_Teste_Conexao.exe" "Programa" /y
del "Instalar_Teste_Conexao.spec"
rmdir "build" /s /q
rmdir "dist" /s /q

pause