param([string]$BlenderPath = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe', [switch]$Skate)
$scenePath = if ($Skate) {
    Join-Path $PSScriptRoot '..\assets\blender\pharmacie-skate-street-v60.blend'
} else {
    Join-Path $PSScriptRoot '..\Pharmacie-Syston.blend'
}
if (-not (Test-Path -LiteralPath $scenePath)) {
    throw "Blender project missing: $scenePath. The separate skate checkpoint stays with Sam; contact him if needed."
}
# This is an interactive editor the user needs to see.
Start-Process -FilePath $BlenderPath -ArgumentList '--online-mode', ('"' + (Resolve-Path -LiteralPath $scenePath).Path + '"')
