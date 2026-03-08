import os
import sys
from goons_clawbot import _push_file_to_github, DEPLOY_FILES, BUILD_PLAN_DIR

def run_manual_deploy():
    print("🚀 Starting manual deployment of build plan...")
    results = []
    for filename in DEPLOY_FILES:
        local_path = os.path.join(BUILD_PLAN_DIR, filename)
        if not os.path.exists(local_path):
            print(f"⏭️ Skipping {filename} (not found)")
            continue
        
        print(f"📦 Pushing {filename}...")
        result = _push_file_to_github(
            local_path, filename, f"Initial Deploy: {filename}"
        )
        if result["ok"]:
            print(f"✅ {filename} pushed.")
        else:
            print(f"❌ {filename} failed (HTTP {result['status']})")

    print("\n🏁 Deployment attempt complete.")

if __name__ == "__main__":
    run_manual_deploy()
