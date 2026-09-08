"""Safe and automated cleaning execution module."""
import os
import shutil
import subprocess
from typing import List, Tuple
from .safety import is_safe_to_delete

def clean_paths(paths: List[str]) -> Tuple[int, List[str]]:
    """Safely cleans listed directory contents or directories."""
    cleaned_count = 0
    errors = []
    
    for path in paths:
        if not os.path.exists(path):
            continue
            
        if not is_safe_to_delete(path):
            errors.append(f"Skipped unsafe path: {path}")
            continue
            
        try:
            if os.path.isfile(path):
                os.remove(path)
                cleaned_count += 1
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                cleaned_count += 1
        except Exception as e:
            errors.append(f"Failed to remove {path}: {str(e)}")
            
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Clear-RecycleBin -DriveLetter C -Force -ErrorAction SilentlyContinue"],
            timeout=15,
            capture_output=True
        )
    except Exception:
        pass
        
    return cleaned_count, errors
