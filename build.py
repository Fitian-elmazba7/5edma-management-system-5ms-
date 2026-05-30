import os
import sys
import shutil
import subprocess

def build():
    # Configuration
    entry_point = "main.py"
    app_name = "ChurchAttendanceSystem"
    icon_path = os.path.join("icons", "app_icon.ico") # Ensure this exists or omit
    
    # List of data files/folders to include
    # Format: (source, destination_in_exe)
    add_data = [
        ("assets", "assets"),
        ("fonts", "fonts"),
        # icons might be empty but we include the folder just in case
        ("icons", "icons"),
    ]

    # Clean up previous builds
    print("Cleaning up previous build artifacts...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    if os.path.exists(f"{app_name}.spec"):
        os.remove(f"{app_name}.spec")

    # Construct PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--windowed", # No console window
        "--onefile",   # Single executable
        f"--name={app_name}",
    ]

    # Add data files
    for src, dest in add_data:
        if os.path.exists(src):
            # On Windows, PyInstaller uses semicolon ; as separator
            cmd.append(f"--add-data={src}{os.pathsep}{dest}")
    
    # Add icon if it exists
    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")

    # Add entry point
    cmd.append(entry_point)

    print(f"Running command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild successful!")
        print(f"Executable can be found in the 'dist' folder as {app_name}.exe")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
