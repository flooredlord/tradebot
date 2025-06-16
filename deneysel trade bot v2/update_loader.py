import os
import shutil
from datetime import datetime

PATCH_DIR = 'update'
ARCHIVE_DIR = 'patched'

def apply_patches():
    if not os.path.exists(PATCH_DIR):
        print("🟡 No update folder found.")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    for filename in os.listdir(PATCH_DIR):
        if filename.startswith("patch_") and filename.endswith(".py"):
            target_file = filename.replace("patch_", "")
            patch_path = os.path.join(PATCH_DIR, filename)
            target_path = target_file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            print(f"🔧 Patching {target_file}...")

            try:
                # 1️⃣ Yedekle
                if os.path.exists(target_path):
                    shutil.copyfile(target_path, f"{target_path}.bak")
                    print(f"📦 Backup created: {target_path}.bak")

                # 2️⃣ Üzerine yaz
                shutil.copyfile(patch_path, target_path)
                print(f"✅ {target_file} updated successfully.")

                # 3️⃣ Arşivle patch dosyasını
                archived_name = f"{ARCHIVE_DIR}/{filename.replace('.py', '')}_{timestamp}.py"
                shutil.move(patch_path, archived_name)
                print(f"📁 Patch archived as: {archived_name}")

            except Exception as e:
                print(f"❌ Failed to patch {target_file}: {e}")