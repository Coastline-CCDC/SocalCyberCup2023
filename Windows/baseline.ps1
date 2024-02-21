# Define filename and spacer for output formatting
$filename = "$HOME\baseline.txt"
$spacer = "`n" + ('-' * 65) + "`n"
$dateStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Write section header to file
Function Write-Section {
    Param ([string]$title)
    Add-Content -Path $filename -Value "`n# $title `n$spacer"
}

# Run command and capture output to file
Function Capture-Output {
    Param ([string]$description, [scriptblock]$command)
    Add-Content -Path $filename -Value "# $description `n"
    & $command | Out-String | Add-Content -Path $filename
}

# Prepare baseline file
"System Baseline captured on $dateStamp $spacer" | Out-File -FilePath $filename

# System Information
Capture-Output "Operating System Information" { Get-WmiObject -Class Win32_OperatingSystem | Format-List * }
Capture-Output "CPU Information" { Get-WmiObject -Class Win32_Processor | Format-List * }
Capture-Output "Network Interface Configuration" { Get-WmiObject -Class Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | Format-List * }
Capture-Output "Disk Usage" { Get-PSDrive -PSProvider FileSystem }
Capture-Output "Environment Variables" { Get-ChildItem Env: }

# User Accounts
Write-Section "User Accounts Information"
Get-WmiObject -Class Win32_UserAccount | Format-List * | Out-File -Append -FilePath $filename

# Installed Applications
Capture-Output "Installed Applications" { Get-WmiObject -Class Win32_Product | Select-Object Name, Version }

# Running Services
Capture-Output "Running Services" { Get-Service | Where-Object { $_.Status -eq 'Running' } }

# Firewall Rules
Capture-Output "Firewall Rules" { Get-NetFirewallRule | Format-Table -AutoSize }

# Scheduled Tasks
Write-Section "Scheduled Tasks"
Get-ScheduledTask | Where-Object { $_.State -eq 'Ready' } | Out-File -Append -FilePath $filename

# End of Baseline
"End of Baseline $spacer" | Out-File -Append -FilePath $filename

Write-Host "Baseline captured to $filename"
