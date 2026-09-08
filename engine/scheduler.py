"""Windows Task Scheduler Automation Module."""
import subprocess
from typing import Tuple, Dict

TASK_NAME = "WinStorageGuard_AutoClean"

def install_scheduled_task(frequency: str = "WEEKLY", day: str = "SUN", time: str = "03:00") -> Tuple[bool, str]:
    """Registers a silent Windows Scheduled Task that runs quick_clean.ps1 in the background."""
    script_path = r"D:\DEV\ACTIVE\win-storage-guard\scripts\quick_clean.ps1"
    
    ps_cmd = f"powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File \\\"{script_path}\\\""
    
    if frequency.upper() == "WEEKLY":
        cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{ps_cmd}" /sc WEEKLY /d {day} /st {time} /f /ru "%USERNAME%"'
    elif frequency.upper() == "DAILY":
        cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{ps_cmd}" /sc DAILY /st {time} /f /ru "%USERNAME%"'
    elif frequency.upper() == "ONLOGON":
        cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{ps_cmd}" /sc ONLOGON /f /ru "%USERNAME%"'
    else:
        cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{ps_cmd}" /sc WEEKLY /d SUN /st 03:00 /f /ru "%USERNAME%"'
        
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode == 0:
            return True, f"Successfully registered scheduled task '{TASK_NAME}' ({frequency} at {time})."
        else:
            return False, f"Failed to create scheduled task: {proc.stderr.strip() or proc.stdout.strip()}"
    except Exception as e:
        return False, str(e)

def uninstall_scheduled_task() -> Tuple[bool, str]:
    """Deletes the scheduled task from Windows Task Scheduler."""
    cmd = f'schtasks /delete /tn "{TASK_NAME}" /f'
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode == 0:
            return True, f"Scheduled task '{TASK_NAME}' removed successfully."
        else:
            return False, f"Task '{TASK_NAME}' not found or already removed."
    except Exception as e:
        return False, str(e)

def get_scheduled_task_status() -> Dict[str, str]:
    """Queries current status of the automation task."""
    cmd = f'schtasks /query /tn "{TASK_NAME}" /fo LIST'
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode == 0:
            return {"installed": True, "details": proc.stdout.strip()}
        return {"installed": False, "details": "Not registered in Windows Task Scheduler."}
    except Exception as e:
        return {"installed": False, "details": str(e)}
