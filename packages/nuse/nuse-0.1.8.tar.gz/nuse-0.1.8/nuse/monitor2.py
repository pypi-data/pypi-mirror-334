import psutil
import time
import os
import threading
import socket
import atexit
import uuid

stop_monitoring = threading.Event()
_monitor_thread = None  # internal monitor thread reference

_filter_cgroup = False
_cgroup_job_id = None

def generate_bar(usage, length=10):
    """Generate a simple text-based bar for the given usage percentage."""
    bars = int((usage / 100.0) * length)
    return '█' * bars + '-' * (length - bars)

def belongs_to_job(pid):
    if not _cgroup_job_id:
        return True
    cgroup_file = f"/proc/{pid}/cgroup"
    if not os.path.exists(cgroup_file):
        return False
    try:
        with open(cgroup_file, "r") as f:
            lines = f.read().splitlines()
        return any(_cgroup_job_id in line for line in lines)
    except Exception:
        return False

def format_cpu_usage(cpu_usage_list, cols=4):
    """
    Expects cpu_usage_list to be a list of tuples: (cpu_index, usage)
    and displays each entry showing the hardware core number.
    """
    lines = []
    rows = (len(cpu_usage_list) + cols - 1) // cols
    for row in range(rows):
        line = ""
        for col in range(cols):
            index = row + col * rows
            if index < len(cpu_usage_list):
                cpu_id, usage = cpu_usage_list[index]
                bar = generate_bar(usage)
                line += f"CPU {cpu_id:02}: {usage:5.1f}% {bar}    "
        lines.append(line)
    return "\n".join(lines)

def format_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'username']):
        try:
            info = proc.info
            if _filter_cgroup and not belongs_to_job(info['pid']):
                continue
            mem_mb = info['memory_info'].rss / (1024 ** 2)
            user = info.get('username', 'unknown')
            line = (f"{info['pid']}",
                    user,
                    f"{info['cpu_percent']:5.1f}%",
                    f"{info['memory_percent']:5.1f}%",
                    f"{mem_mb:8.2f} MB",
                    info['name'] if info['name'] else "unknown")
            processes.append(line)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def cpu_usage(proc_tuple):
        try:
            val = proc_tuple[2].replace('%', '').strip()
            return float(val)
        except (IndexError, ValueError):
            return 0.0

    processes_sorted = sorted(processes, key=cpu_usage, reverse=True)
    if not processes_sorted:
        return "No active processes or all below threshold.\n"

    # Add USER column to header
    header_fmt = "{pid:>8} | {user:>10} | {cpu:>6} | {mem:>6} | {mem_mb:>10} | {name:<20}"
    header_text = header_fmt.format(pid="PID", user="USER", cpu="CPU", mem="MEM", mem_mb="MEM (MB)", name="NAME")
    border = "-" * len(header_text)

    lines = [header_text, border]
    for pid, user, cpu, mem, mem_mb, name in processes_sorted:
        name = name if len(name) <= 20 else name[:20]
        line = header_fmt.format(pid=pid, user=user, cpu=cpu, mem=mem, mem_mb=mem_mb, name=name)
        lines.append(line)
    return "\n".join(lines)

def monitor_resources():
    current_dir = os.getcwd()
    current_dir = os.path.expanduser(os.environ.get("MONITOR_LOG_DIR", "~/.monitoring"))
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    hostname = socket.gethostname()
    # uuid_hash = str(uuid.uuid4())[:2]
    slurm_job_id = os.environ.get('SLURM_JOB_ID')
    log_file_path = os.path.join(current_dir, f"cpu_memory_usage_{hostname}_{slurm_job_id}.log")
    
    # Get allowed CPU indices (from CPU affinity)
    allowed_cpus = psutil.Process().cpu_affinity()
    allowed_cpus = sorted(allowed_cpus)
    
    # Check allocated memory using SLURM environment variable (in MB).
    allocated_mem_mb = os.environ.get("SLURM_MEM_PER_NODE")
    if allocated_mem_mb:
        try:
            allocated_mem_bytes = float(allocated_mem_mb) * (1024 ** 2)
            allocated_mem_gb = allocated_mem_bytes / (1024 ** 3)
        except Exception:
            allocated_mem_bytes = None
            allocated_mem_gb = None
    else:
        allocated_mem_bytes = None

    with open(log_file_path, "w") as f:
        while not stop_monitoring.is_set():
            f.seek(0)
            # Get full CPU percentages then create a (core,index,usage) list using allowed CPUs.
            full_cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
            allocated_cpu_usages = [(cpu, full_cpu_percents[cpu]) for cpu in allowed_cpus if cpu < len(full_cpu_percents)]
            f.write("CPU Usage (Allocated):\n")
            f.write(format_cpu_usage(allocated_cpu_usages, cols=4))
            
            # Compute memory usage as the sum of RSS from processes that belong to this job,
            # if allocated memory is provided. Otherwise fallback to global memory usage.
            if allocated_mem_bytes:
                job_mem = 0
                for proc in psutil.process_iter(['pid', 'memory_info']):
                    try:
                        if _filter_cgroup:
                            if not belongs_to_job(proc.pid):
                                continue
                        job_mem += proc.info['memory_info'].rss
                    except Exception:
                        pass
                percent_used = (job_mem / allocated_mem_bytes) * 100
                mem_usage_str = f"{percent_used:.1f}% used ({job_mem/(1024**3):.2f} GB out of {allocated_mem_gb:.2f} GB)"
            else:
                memory_info = psutil.virtual_memory()
                mem_usage_str = (f"{memory_info.percent:.1f}% used "
                                 f"({memory_info.used/(1024**3):.2f} GB out of {memory_info.total/(1024**3):.2f} GB)")
            
            f.write(f"\n\nMemory Usage (Allocated): {mem_usage_str}\n\n")
            f.write(format_processes())
            f.flush()
            f.truncate()
            time.sleep(1)

def _stop_monitoring():
    stop_monitoring.set()
    if _monitor_thread:
        _monitor_thread.join()

def start_monitoring(filter_cgroup=False, job_id=None):
    """
    Starts the monitor thread in the background and will automatically
    stop when the program exits. If filter_cgroup=True, only processes
    belonging to the SLURM job (determined via cgroup) will be shown.
    Additionally, CPU usage and memory usage will be filtered to show
    only the allocated resources.
    """
    global _monitor_thread, stop_monitoring, _filter_cgroup, _cgroup_job_id
    _filter_cgroup = filter_cgroup
    if filter_cgroup and not job_id:
        job_id = os.environ.get("SLURM_JOB_ID")
    _cgroup_job_id = job_id
    stop_monitoring.clear()
    _monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    _monitor_thread.start()
    atexit.register(_stop_monitoring)