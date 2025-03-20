import os
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description="Display the SLURM job monitor log file using watch."
    )
    parser.add_argument("node_shortname", help="Short name of the node (e.g., node306)")
    parser.add_argument("id", nargs="?", default="1", help="Monitor ID (default: 1)")
    args = parser.parse_args()

    # Use MONITOR_LOG_DIR if set; otherwise, default to ~/.monitoring
    log_dir = os.path.expanduser(os.environ.get("MONITOR_LOG_DIR", "~/.monitoring"))
    log_file = os.path.join(log_dir, f"cpu_memory_usage_{args.node_shortname}.cluster_{args.id}.log")

    if not os.path.exists(log_file):
        print(f"Log file {log_file} not found!")
        return

    command = ["watch", "-n", "1", "cat", log_file]
    try:
        subprocess.call(command)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()