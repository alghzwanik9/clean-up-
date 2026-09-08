"""WinStorageGuard CLI Application with Automation Scheduling"""
import sys
import argparse
from engine.analyzer import get_drive_usage, scan_user_bloat
from engine.cleaner import clean_paths
from engine.windows_update import reset_windows_update_cache
from engine.scheduler import install_scheduled_task, uninstall_scheduled_task, get_scheduled_task_status

def main():
    parser = argparse.ArgumentParser(description="WinStorageGuard - High performance storage analyzer and cleaner.")
    parser.add_argument("--analyze", action="store_true", help="Run comprehensive disk and bloat analysis.")
    parser.add_argument("--clean", action="store_true", help="Execute safe developer and app cache cleanup.")
    parser.add_argument("--reset-wu", action="store_true", help="Reset stuck Windows Update downloads and services.")
    parser.add_argument("--install-schedule", action="store_true", help="Install automated background cleaning schedule.")
    parser.add_argument("--remove-schedule", action="store_true", help="Remove automated background cleaning schedule.")
    parser.add_argument("--schedule-status", action="store_true", help="Check status of automated schedule.")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  WinStorageGuard - Windows Storage Optimizer for Developers")
    print("=" * 60)
    
    c_usage = get_drive_usage("C:")
    print(f"Drive C: Free Space: {c_usage['free_gb']} GB / {c_usage['total_gb']} GB ({c_usage['percent_free']}% Free)")
    
    if args.install_schedule:
        print("\n[+] Registering automated background task in Windows Task Scheduler...")
        ok, msg = install_scheduled_task()
        print(f"    {msg}")
        return
        
    if args.remove_schedule:
        print("\n[+] Removing automated background task...")
        ok, msg = uninstall_scheduled_task()
        print(f"    {msg}")
        return
        
    if args.schedule_status:
        status = get_scheduled_task_status()
        print(f"\n[+] Automation Status: {'ACTIVE' if status['installed'] else 'NOT CONFIGURED'}")
        print(f"    {status['details']}")
        return

    if args.reset_wu:
        print("\n[+] Resetting Windows Update staging cache...")
        success, msg = reset_windows_update_cache()
        print(f"    {msg}")
        return

    if args.analyze or not args.clean:
        print("\n[+] Scanning known bloat and developer cache locations...")
        bloat_items = scan_user_bloat()
        if not bloat_items:
            print("    No heavy caches found (> 1 MB).")
        else:
            print(f"    Found {len(bloat_items)} candidate locations:")
            total_mb = sum(item[1] for item in bloat_items)
            for path, size_mb in bloat_items[:15]:
                print(f"    - {path[:65]:<65} : {size_mb:>8.2f} MB")
            print(f"\n    Total Identifiable Cache: {total_mb:.2f} MB ({total_mb/1024:.2f} GB)")
            
    if args.clean:
        print("\n[!] Starting Safe Automated Cleanup...")
        bloat_items = scan_user_bloat()
        paths_to_clean = [item[0] for item in bloat_items]
        count, errors = clean_paths(paths_to_clean)
        print(f"    Cleaned {count} items.")
        if errors:
            print(f"    Encountered {len(errors)} non-critical notices.")
            
        new_c = get_drive_usage("C:")
        freed = round(new_c['free_gb'] - c_usage['free_gb'], 2)
        print(f"\n[+] Cleanup Complete! New Free Space on C: {new_c['free_gb']} GB (Freed ~{freed} GB)")

if __name__ == "__main__":
    main()
