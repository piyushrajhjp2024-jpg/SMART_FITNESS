$env:FLASK_ENV = "local"
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe app.py
