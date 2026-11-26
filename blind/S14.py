import subprocess

def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False