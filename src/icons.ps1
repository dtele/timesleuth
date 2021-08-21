Param ($ExePath, $SavePath)
Add-Type -AssemblyName System.Drawing
[System.Drawing.Icon]::ExtractAssociatedIcon($ExePath).ToBitmap().Save($SavePath)
