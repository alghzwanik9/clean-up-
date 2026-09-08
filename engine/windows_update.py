"""Windows Update services management and staging cache reset."""
import os
import shutil
import subprocess
from typing import Tuple

def reset_windows_update_cache() -> Tuple[bool, str]:
    """Stops update services, clears corrupted downloads in SoftwareDistribution, and restarts services."""
    services = ["wuauserv", "bits", "dosvc", "cryptsvc"]
    
    for s in services:
        subprocess.run(f"net stop {s} /y", shell=True, capture_output=True)
        
    download_dir = r"C:\Windows\SoftwareDistribution\Download"
    staging_dir = r"C:\$WINDOWS.~BT"
    
    try:
        if os.path.exists(download_dir):
            for item in os.listdir(download_dir):
                item_path = os.path.join(download_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    try:
                        os.remove(item_path)
                    except Exception:
                        pass
        if os.path.exists(staging_dir):
            shutil.rmtree(staging_dir, ignore_errors=True)
    except Exception as e:
        return False, f"Error clearing files: {str(e)}"
        
    for s in ["cryptsvc", "bits", "wuauserv", "dosvc"]:
        subprocess.run(f"net start {s}", shell=True, capture_output=True)
        
    return True, "Windows Update cache successfully reset and services restarted."
