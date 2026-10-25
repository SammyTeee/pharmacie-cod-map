param([string]$ToolsRoot = 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130')
$ErrorActionPreference = 'Stop'
$ToolsRoot = (Resolve-Path -LiteralPath $ToolsRoot).Path.TrimEnd('\')
$repoRoot = Split-Path $PSScriptRoot -Parent
$env:TA_GAME_PATH = "$ToolsRoot\"
$env:TA_TOOLS_PATH = "$ToolsRoot\"
$env:TA_LOCAL_ASSET_CACHE = "$ToolsRoot\share\assetconvert\"
$stdout = Join-Path $repoRoot 'build\bo3-core\relink.stdout.log'
$stderr = Join-Path $repoRoot 'build\bo3-core\relink.stderr.log'
$process = Start-Process -FilePath "$ToolsRoot\bin\linker_modtools.exe" -WorkingDirectory "$ToolsRoot\bin" -ArgumentList @('-language','english','-modsource','zm_pharmacie_core65') -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$process.WaitForExit()
$process.Refresh()
$code = $process.ExitCode
$output = (Get-Content -LiteralPath $stdout -Raw) + (Get-Content -LiteralPath $stderr -Raw)
@{ exitCode=$code; pid=$process.Id; completedUtc=[DateTime]::UtcNow.ToString('o'); stdout=$stdout; stderr=$stderr } | ConvertTo-Json | Set-Content -LiteralPath "$repoRoot\build\bo3-core\relink-result.json"
Write-Output "Linker process exit: $code"
if ($code -ne 0 -or $output -match '(?i)(ERROR:|ASSERTBEGIN|bad static model|Could not load mesh)') { throw 'Core relink failed; inspect exact process result and logs.' }
if ($output -notmatch 'Linking "en_zm_pharmacie_core65".*done:') { throw 'Localized core package did not complete.' }
