# Ensure we are in the project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$ScriptDir/.."

docker compose logs -f --tail=200 trading-bot
