param([Parameter(Mandatory=$true)][string]$ToolsRoot)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$map = Join-Path $ToolsRoot 'map_source\zm\zm_pharmacie.map'
$raw = Join-Path $ToolsRoot 'share\raw\maps\zm\zm_pharmacie'
$env:TA_GAME_PATH = "$ToolsRoot\"
$env:TA_LOCAL_ASSET_CACHE = "$ToolsRoot\share\assetconvert\"
$env:TA_TOOLS_PATH = "$ToolsRoot\"
Copy-Item -LiteralPath "$repoRoot\map_source\zm\zm_pharmacie.map" -Destination $map
Push-Location "$ToolsRoot\bin"
try {
    & .\cod2map64.exe -platform pc -navmesh -navvolume -loadFrom $map "$raw.d3dbsp"
    if ($LASTEXITCODE -ne 0) { throw 'Map compilation failed' }
    $bakeStart = [DateTime]::UtcNow
    & .\Radiant_modtools.exe -ledSilent +medium +localprobes +forceclean +recompute $map
    $deadline = [DateTime]::UtcNow.AddMinutes(5)
    do {
        Start-Sleep -Seconds 2
        $led = Get-Item "$raw.led" -ErrorAction SilentlyContinue
        if ([DateTime]::UtcNow -gt $deadline) { throw 'Timed out waiting for fresh lighting export' }
    } while (!$led -or $led.LastWriteTimeUtc -lt $bakeStart -or (Get-Process Radiant_modtools -ErrorAction SilentlyContinue))
    & .\linker_modtools.exe -language english -modsource zm_pharmacie
    if ($LASTEXITCODE -ne 0) { throw "Linker reported exit $LASTEXITCODE; inspect asset errors before deploying" }
} finally { Pop-Location }
