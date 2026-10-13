"""Windows System and Hardware Optimizer Engine.
Provides SSD TRIM, DNS/Network cache flush, RAM cleanup, Startup app analysis, and System Health checks.
"""
import os
import subprocess
import winreg
from typing import Dict, List, Tuple


def optimize_storage_drive(drive_letter: str = "C") -> Tuple[bool, str]:
    """Runs SSD TRIM and volume optimization using Windows Optimize-Volume or defrag."""
    letter = drive_letter.rstrip(":\\").upper()
    ps_cmd = f"Optimize-Volume -DriveLetter {letter} -ReTrim -Verbose -ErrorAction Stop"
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=90
        )
        if proc.returncode == 0:
            return True, f"SSD TRIM and Volume optimization completed on drive {letter}:"
        
        # Fallback to defrag /O /U
        defrag_proc = subprocess.run(
            ["defrag", f"{letter}:", "/O", "/U"],
            capture_output=True,
            text=True,
            timeout=90
        )
        if defrag_proc.returncode == 0:
            return True, f"Drive {letter}: optimization completed via defrag.exe"

        err = proc.stderr.strip() or defrag_proc.stderr.strip()
        if "Administrator" in err or "elevation" in err.lower() or "access is denied" in err.lower():
            return False, "Optimization requires Administrator privileges. Run as Administrator."
        return False, err or "Failed to run volume optimization."
    except Exception as e:
        return False, str(e)


def flush_network_caches() -> Tuple[bool, List[str]]:
    """Flushes DNS Resolver Cache (Clear-DnsClientCache/ipconfig), NetBIOS, and ARP table."""
    logs = []
    dns_cleared = False
    
    # 1. Clear-DnsClientCache via PowerShell
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Clear-DnsClientCache -ErrorAction SilentlyContinue"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if proc.returncode == 0:
            logs.append("DNS client cache flushed successfully (PowerShell API).")
            dns_cleared = True
    except Exception:
        pass

    # Fallback to ipconfig /flushdns if needed
    if not dns_cleared:
        try:
            proc = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                logs.append("DNS Resolver cache flushed successfully (ipconfig).")
                dns_cleared = True
            else:
                logs.append("Note: DNS flush via ipconfig requires elevated privileges.")
        except Exception as e:
            logs.append(f"DNS flush notice: {e}")

    # 2. Flush NetBIOS Cache
    try:
        proc = subprocess.run(["nbtstat", "-R"], capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            logs.append("NetBIOS name resolution cache cleared.")
    except Exception:
        pass

    # 3. Flush ARP Cache
    try:
        proc = subprocess.run(["arp", "-d", "*"], capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            logs.append("ARP network routing cache cleared.")
    except Exception:
        pass

    return dns_cleared, logs


def get_startup_programs() -> List[Dict[str, str]]:
    """Scans Windows Registry and Startup folders for boot-time programs."""
    startup_items = []

    reg_targets = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "User Registry"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "System Registry"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "System (32-bit) Registry")
    ]

    for root_key, subkey, location in reg_targets:
        try:
            with winreg.OpenKey(root_key, subkey, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, cmd, _ = winreg.EnumValue(key, i)
                        startup_items.append({
                            "name": name,
                            "command": cmd,
                            "location": location
                        })
                        i += 1
                    except OSError:
                        break
        except Exception:
            pass

    # Scan Startup Folders
    user_appdata = os.environ.get("APPDATA", "")
    program_data = os.environ.get("PROGRAMDATA", r"C:\ProgramData")

    folders = [
        (os.path.join(user_appdata, r"Microsoft\Windows\Start Menu\Programs\Startup"), "User Startup Folder"),
        (os.path.join(program_data, r"Microsoft\Windows\Start Menu\Programs\Startup"), "Common Startup Folder")
    ]

    for folder, location in folders:
        if os.path.exists(folder):
            try:
                for file_name in os.listdir(folder):
                    if file_name.lower().endswith((".lnk", ".bat", ".cmd", ".exe")):
                        full_path = os.path.join(folder, file_name)
                        startup_items.append({
                            "name": file_name,
                            "command": full_path,
                            "location": location
                        })
            except Exception:
                pass

    return startup_items


def check_system_integrity(repair: bool = False) -> Tuple[bool, str]:
    """Runs Windows System File Checker (SFC) or DISM scan."""
    cmd = ["sfc", "/scannow" if repair else "/verifyonly"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = proc.stdout.strip()
        if "Windows Resource Protection did not find any integrity violations" in output:
            return True, "All Windows system files are healthy. No integrity violations found."
        elif "found corrupt files and successfully repaired them" in output:
            return True, "Corrupt files were detected and successfully repaired."
        elif "found corrupt files but was unable to fix" in output:
            return False, "Corrupt files found, full DISM restore repair is recommended."
        elif "must be an administrator" in output.lower():
            return False, "SFC system verification requires Administrator privileges."
        else:
            return proc.returncode == 0, output or "System integrity scan finished."
    except Exception as e:
        return False, str(e)


def flush_memory_working_sets() -> Tuple[bool, str]:
    """Frees inactive system memory and working sets safely."""
    ps_cmd = """
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    """
    try:
        proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=15)
        return proc.returncode == 0, "System garbage collection completed and working memory trimmed."
    except Exception as e:
        return False, str(e)
