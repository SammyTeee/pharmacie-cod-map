param([string]$BlenderPath = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
$scenePath = Join-Path $PSScriptRoot '..\assets\blender\pharmacie-player-cleanup-v18.blend'
# This is an interactive editor the user needs to see.
Start-Process -FilePath $BlenderPath -ArgumentList '--online-mode', ('"' + (Resolve-Path -LiteralPath $scenePath).Path + '"')
