# Installing IPFS on Windows

This guide provides step-by-step instructions for installing IPFS (InterPlanetary File System) on Windows using PowerShell.

## Prerequisites

- Windows 10 or later
- PowerShell 5.1 or later
- Administrator privileges

## Installation Steps

### 1. Download IPFS

Open PowerShell as an administrator and run the following commands:

```powershell
# Navigate to Downloads folder
cd C:\Users\YourUsername\Downloads

# Download IPFS
Invoke-WebRequest -Uri "https://dist.ipfs.tech/kubo/v0.30.0/kubo_v0.30.0_windows-amd64.zip" -OutFile "ipfs.zip"


## Create a directory for IPFS and extract the downloaded zip file:

# Create IPFS directory
New-Item -ItemType Directory -Path C:\ipfs

# Extract IPFS
Expand-Archive -Path ipfs.zip -DestinationPath C:\ipfs

## Add the IPFS directory to your system's PATH:
# Add to PATH for current session
$env:Path += ";C:\ipfs"

# Make PATH change permanent
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)

## Initialize the IPFS repository:
ipfs init

## Start the IPFS daemon:
ipfs daemon

## After starting the daemon, you should see output similar to:
Initializing daemon...
Kubo version: 0.30.0
Repo version: 16
System version: amd64/windows
Golang version: go1.22.7
PeerID: 12D3KooWERMGv7NggL94RTMmaq28ZBAFFPbtmDvVpYyMdG9ggaQ2
Swarm listening on /ip4/127.0.0.1/tcp/4001
Swarm listening on /ip6/::1/tcp/4001
RPC API server listening on /ip4/127.0.0.1/tcp/5001
WebUI: http://127.0.0.1:5001/webui
Gateway server listening on /ip4/127.0.0.1/tcp/8081
Daemon is ready

## Troubleshooting

If you encounter permission issues, ensure you're running PowerShell as an administrator.
If ipfs commands are not recognized, restart PowerShell or your computer for PATH changes to take effect.

## Additional Resources

https://docs.ipfs.tech/
https://github.com/ipfs/kubo