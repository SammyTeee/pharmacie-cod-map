param([switch]$WithAudio, [ValidateSet('Street','Holmdale')][string]$Location = 'Street')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimePath = Join-Path $projectRoot 'build/pharmacie-skate/runtime/skate3rust-windows-x64/skate3rust.exe'
$assetPath = Join-Path $projectRoot 'build/pharmacie-skate/assets'
$mapName = if ($Location -eq 'Holmdale') { 'pharmacie-holmdale-29-v64.skate' } else { 'pharmacie-street-session-floor-v62-r3.skate' }
$mapPath = Join-Path $projectRoot ('build/pharmacie-skate/' + $mapName)
$captureName = if ($Location -eq 'Holmdale') { 'runtime-holmdale-v64.png' } elseif ($WithAudio) { 'runtime-audio-v63.png' } else { 'runtime-floor-v62.png' }
$capturePath = Join-Path $projectRoot ('recon/skate-v60/' + $captureName)
$checkLog = Join-Path $projectRoot 'build/skate-demo-asset-check.log'
$captureLog = Join-Path $projectRoot 'build/skate-runtime-demo.log'
$env:SKATE_REPORT_CHILD = '1'
if ($WithAudio -and -not (Test-Path -LiteralPath (Join-Path $assetPath 'private/audio/audio_manifest.json'))) { throw 'Prepare and validate the private audio first.' }
$ErrorActionPreference = 'Continue' # Windows PowerShell treats native stderr diagnostics as ErrorRecords.
& $runtimePath --assets $assetPath --map $mapPath --difficulty easy --check-assets *> $checkLog
$ErrorActionPreference = 'Stop'
if ($LASTEXITCODE -ne 0) { throw 'Runtime input/collision validation failed; inspect build/skate-demo-asset-check.log.' }
$captureStart = [DateTime]::UtcNow
$env:SKATE_REPORT_CHILD = '1'
# The runtime's own verification captures and exits; no keyboard/mouse input.
$ErrorActionPreference = 'Continue'
$soundArguments = if ($WithAudio) { @() } else { @('--mute') }
& $runtimePath --assets $assetPath --map $mapPath --difficulty easy @soundArguments --player-title 'Syston Street Session - verification' --verify $capturePath *> $captureLog
$ErrorActionPreference = 'Stop'
if ($LASTEXITCODE -ne 0) { throw 'Runtime capture failed; inspect build/skate-runtime-demo.log.' }
if (-not (Test-Path -LiteralPath $capturePath)) { throw 'Capture missing.' }
if ((Get-Item -LiteralPath $capturePath).LastWriteTimeUtc -lt $captureStart) { throw 'Capture is stale.' }
if (-not (Select-String -LiteralPath $captureLog -Pattern 'GAME_VERIFY_OK' -Quiet)) { throw 'Runtime did not report a successful capture.' }
if ($WithAudio) {
    $audioLog = (Get-Content -LiteralPath $captureLog -Raw) -replace '\s+', ' '
    if ($audioLog -notmatch 'Game audio: [0-9]+ ambience beds, [0-9]+ rolling grains, [0-9]+ sample banks') { throw 'Runtime did not initialize the audio library.' }
    if (Select-String -LiteralPath $captureLog -Pattern 'Game audio unavailable|REPORT_PANIC|physics_failed:true' -Quiet) { throw 'Audio verification logged a runtime failure.' }
}
Write-Output 'SYSTON_RUNTIME_CAPTURE_PASS'
