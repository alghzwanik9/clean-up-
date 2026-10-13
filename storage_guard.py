"""WinStorageGuard CLI Application with Performance Optimizer."""
import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from engine.analyzer import get_drive_usage, scan_user_bloat
from engine.cleaner import clean_paths
from engine.optimizer import (
    check_system_integrity,
    flush_memory_working_sets,
    flush_network_caches,
    get_startup_programs,
    optimize_storage_drive,
)
from engine.scheduler import (
    get_scheduled_task_status,
    install_scheduled_task,
    uninstall_scheduled_task,
)
from engine.windows_update import reset_windows_update_cache


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns command line arguments parser."""
    parser = argparse.ArgumentParser(
        description=(
            "WinStorageGuard - Storage & System Performance Optimizer."
        )
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run comprehensive disk and bloat analysis.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Execute safe developer and app cache cleanup.",
    )
    parser.add_argument(
        "--reset-wu",
        action="store_true",
        help="Reset stuck Windows Update downloads and services.",
    )
    parser.add_argument(
        "--install-schedule",
        action="store_true",
        help="Install automated background cleaning schedule.",
    )
    parser.add_argument(
        "--remove-schedule",
        action="store_true",
        help="Remove automated background cleaning schedule.",
    )
    parser.add_argument(
        "--schedule-status",
        action="store_true",
        help="Check status of automated schedule.",
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run system optimization pipeline (TRIM, DNS, RAM).",
    )
    parser.add_argument(
        "--trim",
        action="store_true",
        help="Execute SSD TRIM and Volume optimization on drive C:.",
    )
    parser.add_argument(
        "--flush-dns",
        action="store_true",
        help="Flush DNS resolver and network routing caches.",
    )
    parser.add_argument(
        "--startup",
        action="store_true",
        help="Scan and analyze boot-time startup applications.",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Verify Windows system file integrity via SFC.",
    )
    return parser


def handle_startup_scan() -> None:
    """Displays boot-time startup applications."""
    print("\n[+] Scanning Startup Applications...")
    items = get_startup_programs()
    if not items:
        print("    No startup items found in monitored registries/folders.")
        return

    print(f"    Found {len(items)} startup programs registered:")
    for item in items:
        cmd_display = item["command"]
        if len(cmd_display) > 60:
            cmd_display = cmd_display[:57] + "..."
        loc = item["location"][:22]
        name = item["name"][:25]
        print(f"    [{loc:<22}] {name:<25} : {cmd_display}")


def main():
    """Main CLI entrypoint for WinStorageGuard."""
    parser = build_parser()
    args = parser.parse_args()

    print("=" * 65)
    print("  WinStorageGuard - Storage & System Performance Optimizer")
    print("=" * 65)

    c_usage = get_drive_usage("C:")
    free_gb = c_usage["free_gb"]
    total_gb = c_usage["total_gb"]
    pct = c_usage["percent_free"]
    print(f"Drive C: Free Space: {free_gb} GB / {total_gb} GB ({pct}% Free)")

    if args.install_schedule:
        print("\n[+] Registering automated background task...")
        _, msg = install_scheduled_task()
        print(f"    {msg}")
        return

    if args.remove_schedule:
        print("\n[+] Removing automated background task...")
        _, msg = uninstall_scheduled_task()
        print(f"    {msg}")
        return

    if args.schedule_status:
        status = get_scheduled_task_status()
        state = "ACTIVE" if status["installed"] else "NOT CONFIGURED"
        print(f"\n[+] Automation Status: {state}")
        print(f"    {status['details']}")
        return

    if args.reset_wu:
        print("\n[+] Resetting Windows Update staging cache...")
        _, msg = reset_windows_update_cache()
        print(f"    {msg}")
        return

    if args.trim:
        print("\n[+] Running SSD TRIM and Volume Optimization...")
        _, msg = optimize_storage_drive("C")
        print(f"    {msg}")
        return

    if args.flush_dns:
        print("\n[+] Flushing DNS and Network Caches...")
        _, logs = flush_network_caches()
        for log in logs:
            print(f"    - {log}")
        return

    if args.startup:
        handle_startup_scan()
        return

    if args.health:
        print("\n[+] Running Windows System File Integrity Check (SFC)...")
        print("    (This may take a minute)...")
        _, msg = check_system_integrity(repair=False)
        print(f"    Result: {msg}")
        return

    if args.optimize:
        print("\n[!] Running Full System Optimization Pipeline...")
        print("\n1. SSD TRIM & Drive Optimization:")
        _, msg_trim = optimize_storage_drive("C")
        print(f"   {msg_trim}")

        print("\n2. Network & DNS Cache Flush:")
        _, net_logs = flush_network_caches()
        for log in net_logs:
            print(f"   - {log}")

        print("\n3. RAM Working Sets Trim:")
        _, msg_mem = flush_memory_working_sets()
        print(f"   - {msg_mem}")

        print("\n[+] System Optimization Completed.")
        return

    # Storage Analysis & Safe Cleanup Handling
    bloat_items = None
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
            total_gb = total_mb / 1024
            print(f"\n    Total Cache: {total_mb:.2f} MB ({total_gb:.2f} GB)")

    if args.clean:
        print("\n[!] Starting Safe Automated Cleanup...")
        if bloat_items is None:
            bloat_items = scan_user_bloat()
        paths_to_clean = [item[0] for item in bloat_items]
        count, errors = clean_paths(paths_to_clean)
        print(f"    Cleaned {count} items.")
        if errors:
            print(f"    Encountered {len(errors)} non-critical notices.")

        new_c = get_drive_usage("C:")
        freed = round(new_c["free_gb"] - c_usage["free_gb"], 2)
        print(
            f"\n[+] Cleanup Complete! New Free Space on C: "
            f"{new_c['free_gb']} GB (Freed ~{freed} GB)"
        )


if __name__ == "__main__":
    main()
