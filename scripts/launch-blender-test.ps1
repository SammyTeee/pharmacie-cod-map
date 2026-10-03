param(
    [Parameter(Mandatory=$true)][string]$ToolsRoot,
    [Parameter(Mandatory=$true)][string]$GameRoot,
    [ValidatePattern('^zm_[a-z0-9_]+$')][string]$MapName = 'zm_pharmacie_blender'
)
$ErrorActionPreference = 'Stop'
$ToolsRoot = (Resolve-Path -LiteralPath $ToolsRoot).Path
$GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
$repoRoot = Split-Path $PSScriptRoot -Parent
$mapName = $MapName
if (Get-Process -Name BlackOps3 -ErrorAction SilentlyContinue) {
    throw 'BO3 is already running; leave the existing session intact before launching this test.'
}
$zone = Join-Path $ToolsRoot "usermaps\$mapName\zone"
foreach ($file in @("$mapName.ff", "en_$mapName.ff")) {
    if (!(Test-Path -LiteralPath (Join-Path $zone $file))) { throw "Missing compiled package: $file" }
}
$backup = Join-Path $repoRoot ('build\before-blender-test-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
if (Test-Path -LiteralPath "$GameRoot\players") {
    Copy-Item -LiteralPath "$GameRoot\players" -Destination "$backup\players" -Recurse
}
$destination = Join-Path $GameRoot "usermaps\$mapName"
if (Test-Path -LiteralPath $destination) {
    Copy-Item -LiteralPath $destination -Destination "$backup\previous-test-map" -Recurse
}
New-Item -ItemType Directory -Path "$destination\zone" -Force | Out-Null
# Sound banks live below zone\snd; BO3 fails to load if only the root FF/XPak
# files are deployed. Preserve the complete linker output tree.
Get-ChildItem -LiteralPath $zone -Recurse -File | ForEach-Object {
    $relative = $_.FullName.Substring($zone.Length + 1)
    $target = Join-Path "$destination\zone" $relative
    New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $_.FullName -Destination $target
    if ((Get-FileHash -LiteralPath $_.FullName).Hash -ne (Get-FileHash -LiteralPath $target).Hash) {
        throw "Deployed file verification failed: $relative"
    }
}
# Visible game window is intentional: Sam requested opening the map to inspect.
$game = Start-Process -FilePath "$GameRoot\BlackOps3.exe" -WorkingDirectory $GameRoot -ArgumentList @(
    '+set', 'fs_game', $mapName, '+set', 'logfile', '2', '+devmap', $mapName
) -PassThru
$record = @{ map=$mapName; pid=$game.Id; backup=$backup; launchedUtc=[DateTime]::UtcNow.ToString('o'); gameRoot=$GameRoot }
$record | ConvertTo-Json | Set-Content -LiteralPath "$repoRoot\build\blender-test-launch.json"
$record | ConvertTo-Json
