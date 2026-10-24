param([string]$BlenderPath = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe', [switch]$Skate)
$checkpoint = if ($Skate) { 'pharmacie-skate-street-v60.blend' } else { 'pharmacie-demo-base-v59.blend' }
$scenePath = Join-Path $PSScriptRoot ('..\assets\blender\' + $checkpoint)
# This is an interactive editor the user needs to see.
Start-Process -FilePath $BlenderPath -ArgumentList '--online-mode', ('"' + (Resolve-Path -LiteralPath $scenePath).Path + '"')
