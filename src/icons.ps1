Param ($ExePath)
Add-Type -AssemblyName System.Drawing

$SysTime = Get-Date -Format hhmmssffff
$TempPath = $env:TEMP + "\ActivityTracker_" + $ExePath.Split("\")[-1].Split(".")[0] + "_" + $SysTime + ".bmp"

$Image = [System.Drawing.Icon]::ExtractAssociatedIcon($ExePath).ToBitmap().Save($TempPath)
$Bytes = Get-Content $TempPath -Encoding Byte
$EncodedString = [Convert]::ToBase64String($Bytes)

Remove-Item $TempPath
Write-Output $EncodedString
