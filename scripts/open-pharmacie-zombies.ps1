param(
    [string]$ToolsRoot = 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130',
    [string]$GameRoot = 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III',
    [switch]$DeployOnly
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$accepted = Join-Path $repoRoot 'build\bo3-core\build-acceptance.json'
if (!(Test-Path -LiteralPath $accepted)) { throw 'The new core build has not passed its build checks yet.' }
$record = Get-Content -LiteralPath $accepted -Raw | ConvertFrom-Json
$mapSource = Join-Path $repoRoot 'map_source\zm\zm_pharmacie_core65.map'
if ((Get-FileHash -LiteralPath $mapSource -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.map_sha256) {
    throw 'Map source changed since build acceptance. Rebuild before launching.'
}
if (!$record.script_sha256) { throw 'Build acceptance is missing script hashes. Re-accept the current package.' }
foreach ($entry in $record.script_sha256.PSObject.Properties) {
    $path = Join-Path $repoRoot ('usermaps\zm_pharmacie_core65\' + $entry.Name)
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.Value) {
        throw "Script changed since build acceptance: $path"
    }
}
foreach ($entry in $record.packageFiles) {
    $path = Join-Path $ToolsRoot ('usermaps\zm_pharmacie_core65\zone\' + $entry.path)
    if (!(Test-Path -LiteralPath $path)) { throw "Missing accepted package file: $path" }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) {
        throw "Package differs from accepted build: $path"
    }
}
# Existing launcher backs up player/profile data and any previous core package,
# deploys the entire zone/snd tree with hash checks, and leaves inputs to Sam.
& "$PSScriptRoot\launch-blender-test.ps1" -ToolsRoot $ToolsRoot -GameRoot $GameRoot -MapName 'zm_pharmacie_core65' -DeployOnly:$DeployOnly
