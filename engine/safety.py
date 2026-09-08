"""Safety enforcement layer to prevent accidental data loss."""
import os

PROTECTED_PATHS = [
    "C:\\Windows\\System32",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\Default",
    "D:\\DEV",
    "D:\\",
]

def is_safe_to_delete(target_path: str) -> bool:
    """Verifies that a target path is not a critical system root or source repository."""
    if not target_path or len(target_path.strip()) < 4:
        return False
    
    norm_target = os.path.normcase(os.path.abspath(target_path))
    
    if norm_target in ["c:\\", "d:\\", "c:", "d:"]:
        return False
        
    for p in PROTECTED_PATHS:
        norm_p = os.path.normcase(os.path.abspath(p))
        if norm_target == norm_p:
            return False
            
    return True
