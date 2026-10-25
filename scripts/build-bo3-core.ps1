param([string]$ToolsRoot = 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130', [switch]$RebuildAssetDatabase)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$source = Join-Path $repoRoot 'build\bo3-core'
$ToolsRoot = (Resolve-Path -LiteralPath $ToolsRoot).Path.TrimEnd('\')
$modelDestination = Join-Path $ToolsRoot 'model_export\pharmacie_core65'
if (!(Test-Path -LiteralPath "$source\model-report.json")) { throw 'Prepare and verify core models first.' }
# Only this project's isolated namespace is staged. Stock files are referenced.
New-Item -ItemType Directory -Path $modelDestination -Force | Out-Null
Get-ChildItem -LiteralPath "$source\models-v2" -Filter '*.xmodel_bin' | Copy-Item -Destination $modelDestination
Copy-Item -LiteralPath "$source\pharmacie_core65.gdt" -Destination "$source\textures\pharmacie_core65.gdt"
& "$PSScriptRoot\build-map.ps1" -ToolsRoot $ToolsRoot -MapName 'zm_pharmacie_core65' -AssetFolder 'build\bo3-core\textures' -AssetNamespace 'pharmacie_core65' -RebuildAssetDatabase:$RebuildAssetDatabase
if ($LASTEXITCODE -ne 0) { throw 'Core build failed.' }
