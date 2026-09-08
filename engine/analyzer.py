"""High performance disk and directory analyzer."""
import os
import re
import shutil
import subprocess
from typing import Dict, List, Tuple

def get_drive_usage(drive: str = "C:") -> Dict[str, float]:
    """Returns total, used, free GB and percent free for a given drive."""
    total, used, free = shutil.disk_usage(drive)
    return {
        "drive": drive,
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "percent_free": round((free / total) * 100, 2)
    }

def get_fast_folder_size(path: str) -> int:
    """Uses Win32 Robocopy multi-threaded scanning to get accurate folder sizes in milliseconds."""
    if not os.path.exists(path):
        return 0
    if os.path.isfile(path):
        return os.path.getsize(path)
        
    cmd = f'robocopy "{path}" "%TEMP%\\null" /L /E /BYTES /NFL /NDL /NJH /R:0 /W:0 /XJ /MT:32'
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        for line in proc.stdout.splitlines():
            match = re.search(r'Bytes\s*:\s*(\d+)', line)
            if match:
                return int(match.group(1))
    except Exception:
        pass
    return 0

def scan_user_bloat(username: str = None) -> List[Tuple[str, float]]:
    """Scans common bloat locations and returns sizes in MB."""
    user = username or os.environ.get("USERNAME", "HUAWEI1")
    user_home = f"C:\\Users\\{user}"
    
    targets = [
        f"{user_home}\\AppData\\Local\\Temp",
        f"{user_home}\\AppData\\Local\\npm-cache",
        f"{user_home}\\AppData\\Local\\pip\\cache",
        f"{user_home}\\AppData\\Local\\pypoetry\\cache",
        f"{user_home}\\AppData\\Local\\ms-playwright",
        f"{user_home}\\AppData\\Local\\.dartServer",
        f"{user_home}\\AppData\\Local\\Pub\\Cache",
        f"{user_home}\\AppData\\Local\\RobloxPCGDK",
        f"{user_home}\\AppData\\Local\\Arduino15",
        f"{user_home}\\AppData\\Local\\CapCut",
        f"{user_home}\\AppData\\Local\\FortniteGame",
        f"{user_home}\\AppData\\Roaming\\kingsoft",
        f"{user_home}\\AppData\\Roaming\\Notion",
        f"{user_home}\\AppData\\Roaming\\discord",
        f"{user_home}\\AppData\\Roaming\\Code\\CachedExtensionVSIXs",
        f"{user_home}\\AppData\\Roaming\\Cursor\\CachedExtensionVSIXs",
        f"{user_home}\\AppData\\Roaming\\Antigravity IDE\\CachedData",
        f"{user_home}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Service Worker",
        f"{user_home}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Service Worker",
        f"{user_home}\\AppData\\Local\\D3DSCache",
        f"{user_home}\\.gradle\\caches",
        f"{user_home}\\.sonarlint",
        f"{user_home}\\.kluster",
        f"{user_home}\\.opencode",
        f"{user_home}\\.claude",
        r"C:\Windows\Temp",
        r"C:\Windows\SoftwareDistribution\Download"
    ]
    
    results = []
    for t in targets:
        if os.path.exists(t):
            size_bytes = get_fast_folder_size(t)
            size_mb = round(size_bytes / (1024**2), 2)
            if size_mb > 1.0:
                results.append((t, size_mb))
                
    results.sort(key=lambda x: x[1], reverse=True)
    return results
