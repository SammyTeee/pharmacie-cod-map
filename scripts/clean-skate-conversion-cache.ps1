$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$cacheRoot = (Resolve-Path -LiteralPath (Join-Path $projectRoot 'build/pharmacie-skate')).Path
$audioProof = Get-Content -LiteralPath (Join-Path $cacheRoot 'audio-preparation.json') -Raw | ConvertFrom-Json
if ($audioProof.status -ne 'audio_conversion_and_pcm_validation_pass' -or $audioProof.wav_files -ne 4142) { throw 'Completed audio proof required before cache cleanup.' }
$liveMap = Join-Path $cacheRoot 'pharmacie-street-session-floor-v62-r3.skate'
if ((Get-FileHash -LiteralPath $liveMap -Algorithm SHA256).Hash.ToLower() -ne '5b6eab254aed961aa58875eaa37eeda4fe5074d182201fe28012cec0f10222d9') { throw 'Live map changed; inspect before cleanup.' }
# Explicit disposable outputs created by our conversion, never user source files.
$cacheNames = @('audio-work-v63','pharmacie-street-session-runtime.skate','pharmacie-street-session-playable.skate','pharmacie-street-session-floor-v61.skate','pharmacie-street-session-floor-v62.skate','pharmacie-street-session-floor-v62-r2.skate')
$cacheTargets = foreach ($cacheName in $cacheNames) {
    $cacheTarget = [IO.Path]::GetFullPath((Join-Path $cacheRoot $cacheName))
    if (-not $cacheTarget.StartsWith($cacheRoot + [IO.Path]::DirectorySeparatorChar)) { throw 'Unsafe cleanup target.' }
    if (Test-Path -LiteralPath $cacheTarget) {
        $cacheItem = Get-Item -LiteralPath $cacheTarget
        if ($cacheItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Cleanup refuses reparse points.' }
        if ($cacheItem.PSIsContainer) {
            if (Get-ChildItem -LiteralPath $cacheTarget -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }) { throw 'Cleanup tree contains a reparse point.' }
        }
        $cacheTarget
    }
}
foreach ($cacheTarget in $cacheTargets) { Remove-Item -LiteralPath $cacheTarget -Recurse -Force }
Write-Output 'Only generated audio work and superseded intermediate packages removed.'
Get-PSDrive C | Select-Object -ExpandProperty Free
