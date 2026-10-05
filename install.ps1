Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation des dependances du projet" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nInstallation terminee avec succes." -ForegroundColor Green
} else {
    Write-Host "`nUne erreur est survenue lors de l'installation." -ForegroundColor Red
}
