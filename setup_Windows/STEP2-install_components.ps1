cd "${PSScriptRoot}\..\"

conda create -n NLP -y
conda activate NLP

curl -o Anaconda3-Windows-x86_64.exe https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe

python -m pip install -r requirements.txt

conda activate NLP
python src\download_nltk.py
python src\download_jars.py

conda activate NLP
python -m spacy download en

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\NLP_Suite.lnk")
$Shortcut.TargetPath = "${PSScriptRoot}\run.bat"
$Shortcut.IconLocation = "${PSScriptRoot}\logo.ico"
$Shortcut.Save()

copy setup_Windows\run.bat run.bat
copy setup_Windows\nlp.bat nlp.bat

Write-Host "----------------------" -ForegroundColor Green
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "----------------------" -ForegroundColor Green
msg "Installation Complete!"
