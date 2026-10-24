param([string]$Assets, [ValidateSet('Street','Holmdale')][string]$Location = 'Street')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeDirectory = Join-Path $projectRoot 'build/pharmacie-skate/runtime/skate3rust-windows-x64'
$runtimePath = Join-Path $runtimeDirectory 'skate3rust.exe'
$mapName = if ($Location -eq 'Holmdale') { 'pharmacie-holmdale-29-v64.skate' } else { 'pharmacie-street-session-floor-v62-r3.skate' }
$mapPath = Join-Path $projectRoot ('build/pharmacie-skate/' + $mapName)
if (-not (Test-Path -LiteralPath $runtimePath)) { throw 'The pinned local skating runtime has not been prepared.' }
if (-not (Test-Path -LiteralPath $mapPath)) { throw 'Export the separate skate map first.' }
if (-not $Assets) {
    $Assets = Join-Path $projectRoot 'build/pharmacie-skate/assets'
}
if (-not (Test-Path -LiteralPath (Join-Path $Assets 'private/game.json'))) { throw 'The local skating inputs have not been prepared; see docs/SKATE_PROTOTYPE.md.' }
$assetPath = (Resolve-Path -LiteralPath $Assets).Path
$argumentList = @('--assets', ('"' + $assetPath + '"'), '--map', ('"' + $mapPath + '"'), '--difficulty', 'easy', '--player-title', '"Syston Street Session"')
# Interactive skating window: visible because the user needs to see and control it.
$process = Start-Process -FilePath $runtimePath -WorkingDirectory $runtimeDirectory -ArgumentList $argumentList -PassThru -RedirectStandardOutput (Join-Path $projectRoot 'build/skate-interactive-stdout.log') -RedirectStandardError (Join-Path $projectRoot 'build/skate-interactive-stderr.log')
Set-Content -LiteralPath (Join-Path $projectRoot 'build/skate-interactive-pid.txt') -Value $process.Id
Write-Output ('Syston Street Session launched, PID ' + $process.Id)
