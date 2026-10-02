param([Parameter(Mandatory=$true)][string]$ToolsRoot)
$ErrorActionPreference = 'Stop'
$ToolsRoot = (Resolve-Path -LiteralPath $ToolsRoot).Path.TrimEnd('\')
$repoRoot = Split-Path $PSScriptRoot -Parent
$map = Join-Path $ToolsRoot 'map_source\zm\zm_pharmacie.map'
$raw = Join-Path $ToolsRoot 'share\raw\maps\zm\zm_pharmacie'
# A fresh clone must carry the launcher project scripts/zone/sound configuration,
# not depend on a project previously created on Sam's PC.
foreach ($required in @('bin\cod2map64.exe', 'bin\Radiant_modtools.exe', 'bin\linker_modtools.exe', 'gdtdb\gdtdb.exe', 'deffiles')) {
    if (!(Test-Path -LiteralPath (Join-Path $ToolsRoot $required))) { throw "Incomplete Mod Tools installation: missing $required" }
}
$projectSource = Join-Path $repoRoot 'usermaps\zm_pharmacie'
Get-ChildItem -LiteralPath $projectSource -Recurse -File | ForEach-Object {
    $relative = $_.FullName.Substring($projectSource.Length + 1)
    $destination = Join-Path "$ToolsRoot\usermaps\zm_pharmacie" $relative
    New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $_.FullName -Destination $destination
}
New-Item -ItemType Directory -Path (Split-Path $map -Parent) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $raw -Parent) -Force | Out-Null
$env:TA_GAME_PATH = $ToolsRoot
$env:TA_LOCAL_ASSET_CACHE = "$ToolsRoot\share\assetconvert"
$env:TA_TOOLS_PATH = $ToolsRoot
$photoSource = Join-Path $repoRoot 'assets\photos'
$photoDestination = Join-Path $ToolsRoot 'texture_assets\pharmacie'
New-Item -ItemType Directory -Path $photoDestination -Force | Out-Null
Get-ChildItem -LiteralPath $photoSource -Filter '*.tif' | Copy-Item -Destination $photoDestination
Copy-Item -LiteralPath "$photoSource\pharmacie.gdt" -Destination "$ToolsRoot\source_data\pharmacie.gdt"
# Register assets explicitly; the GUI database tray may not be running.
Push-Location "$ToolsRoot\bin"
try {
    & "$ToolsRoot\gdtdb\gdtdb.exe" /update
    if ($LASTEXITCODE -ne 0) { throw 'GDT database update failed; inspect logs. Old duplicate path registrations may require a backed-up gdtdb /rebuild.' }
} finally { Pop-Location }
# Compiler/lighting/linker concatenate subpaths and require the trailing slash.
# GDT indexing above needs normalized paths to avoid duplicate registrations.
$env:TA_GAME_PATH = "$ToolsRoot\"
$env:TA_TOOLS_PATH = "$ToolsRoot\"
$env:TA_LOCAL_ASSET_CACHE = "$ToolsRoot\share\assetconvert\"
Copy-Item -LiteralPath "$repoRoot\map_source\zm\zm_pharmacie.map" -Destination $map
Push-Location "$ToolsRoot\bin"
try {
    & .\cod2map64.exe -platform pc -navmesh -navvolume -loadFrom $map "$raw.d3dbsp" 2>&1 | Tee-Object -Variable compileOutput
    if ($LASTEXITCODE -ne 0) { throw 'Map compilation failed' }
    if ($compileOutput -match "Material 'pharmacie_[^']+' is missing") { throw 'Custom photo material is missing; register the GDT before building' }
    $bakeStart = [DateTime]::UtcNow
    $bake = Start-Process -FilePath '.\Radiant_modtools.exe' -ArgumentList @('-ledSilent', '+medium', '+localprobes', '+forceclean', '+recompute', ('"' + $map + '"')) -WindowStyle Hidden -PassThru
    $deadline = [DateTime]::UtcNow.AddMinutes(5)
    do {
        Start-Sleep -Seconds 2
        $led = Get-Item "$raw.led" -ErrorAction SilentlyContinue
        if ([DateTime]::UtcNow -gt $deadline) { throw 'Timed out waiting for fresh lighting export' }
        $bake.Refresh()
    } while (!$led -or $led.LastWriteTimeUtc -lt $bakeStart -or !$bake.HasExited)
    if ($bake.ExitCode -ne 0) { throw "Lighting bake reported exit $($bake.ExitCode)" }
    & .\linker_modtools.exe -language english -modsource zm_pharmacie 2>&1 | Tee-Object -Variable linkOutput
    if ($LASTEXITCODE -ne 0) { throw "Linker reported exit $LASTEXITCODE; inspect asset errors before deploying" }
    if ($linkOutput -match '(?i)(\^1)?ERROR:') { throw 'Linker printed an asset error despite its exit code; do not deploy this package' }
} finally { Pop-Location }
