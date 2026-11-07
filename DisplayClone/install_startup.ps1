# Registers DisplayClone.exe in the current user's Startup folder.
# Uninstall: .\install_startup.ps1 -Uninstall
param([switch]$Uninstall)

$startup = [Environment]::GetFolderPath('Startup')
$lnk = Join-Path $startup 'DisplayClone.lnk'

if ($Uninstall) {
    if (Test-Path $lnk) { Remove-Item $lnk; Write-Host "Removed: $lnk" } else { Write-Host "Not registered" }
    return
}

$exe = Join-Path $PSScriptRoot 'dist\DisplayClone.exe'
if (-not (Test-Path $exe)) { Write-Error "exe not found: $exe (run build.bat first)"; exit 1 }

$shell = New-Object -ComObject WScript.Shell
$sc = $shell.CreateShortcut($lnk)
$sc.TargetPath = $exe
$sc.WorkingDirectory = Split-Path $exe
$sc.Save()
Write-Host "Registered: $lnk -> $exe"
