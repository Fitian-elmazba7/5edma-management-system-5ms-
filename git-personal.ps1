function git-personal {
    git config --global user.name "pierreamir123"
    git config --global user.email "pierrebassily@gmail.com"
    Write-Host "Switched to PERSONAL profile ✅"

    # Try to ensure ssh-agent is usable. 
    # 1. Check if the Windows 'ssh-agent' service is running (preferred on Windows 10/11)
    $service = Get-Service ssh-agent -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq 'Running') {
        # Service is running, ssh-add should just work
    } else {
        # 2. Fallback: Start a process-local agent if one isn't already set in env (mimicking eval $(ssh-agent -s))
        if (-not $env:SSH_AUTH_SOCK) {
            $agent_output = ssh-agent 2>$null
            if ($agent_output) {
                $agent_output | ForEach-Object {
                    if ($_ -match "SSH_AUTH_SOCK=(.*?);") { $env:SSH_AUTH_SOCK = $matches[1] }
                    if ($_ -match "SSH_AGENT_PID=(.*?);") { $env:SSH_AGENT_PID = $matches[1] }
                }
            }
        }
    }

    ssh-add "$HOME\.ssh\pierre"
    Write-Host "ssh Activated"
}
