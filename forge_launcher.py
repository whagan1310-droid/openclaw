import subprocess
import time
import os
import sys

# Apptivators Academy: The Forge Suite Launcher
# This script starts all 4 bots as independent processes.

BOTS = [
    {"name": "GoonsClawbot", "path": "bots/GoonsClawbot/goons_clawbot.py"},
    {"name": "S.A.M.P.I.RT", "path": "bots/S.A.M.P.I.RT/sampi_rt_bot.py"},
    {"name": "SyncFlux", "path": "bots/SyncFlux/sync_flux_bot.py"},
    {"name": "SonicForge", "path": "bots/SonicForge/sonic_forge_bot.py"},
]

def launch_all():
    processes = []
    print("⚔️ Apptivators Academy: Initiating Forge Launch Sequence ⚔️")
    print("-" * 60)

    for bot in BOTS:
        abs_path = os.path.join(os.path.dirname(__file__), bot["path"])
        if os.path.exists(abs_path):
            print(f"🚀 Launching {bot['name']}...")
            # Use sys.executable to ensure we use the same python interpreter
            proc = subprocess.Popen([sys.executable, abs_path])
            processes.append(proc)
            time.sleep(2) # Stagger start
        else:
            print(f"⚠️ Warning: {bot['name']} not found at {abs_path}")

    print("-" * 60)
    print("🔥 All systems green. The Forge is Online.")
    print("Ctrl+C to terminate the suite.")

    try:
        while True:
            # Check if processes are alive
            for i, proc in enumerate(processes):
                if proc.poll() is not None:
                    print(f"❌ Alert: {BOTS[i]['name']} has terminated! Re-launching...")
                    abs_path = os.path.join(os.path.dirname(__file__), BOTS[i]["path"])
                    processes[i] = subprocess.Popen([sys.executable, abs_path])
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛡️ Securing the Forge... Terminating all bots.")
        for proc in processes:
            proc.terminate()
        print("✅ Shutdown Complete.")

if __name__ == "__main__":
    launch_all()
