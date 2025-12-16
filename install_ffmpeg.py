import os
import sys
import subprocess
import urllib.request
import urllib.error
import zipfile
import shutil
import platform
import winreg
from pathlib import Path

# Configuration
FFMPEG_FILENAME = "ffmpeg-master-latest-win64-gpl.zip"
GITHUB_URL = f"https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/{FFMPEG_FILENAME}"
MIRROR_PREFIX = "https://mirror.ghproxy.com/"
INSTALL_DIR = Path.home() / "ffmpeg_portable"

def print_color(text, color="white"):
    """Simple color printing for Windows terminal"""
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    # Enable VT100 emulation if on Windows 10+ (usually enabled by default in modern terminals)
    sys.stdout.write(f"{colors.get(color, '')}{text}{colors['reset']}\n")

def check_ffmpeg_installed():
    """Check if ffmpeg is available in PATH"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def add_to_user_path(new_path):
    """Add a directory to the User PATH environment variable permanently via Registry"""
    new_path = str(new_path)
    key_path = r"Environment"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""
        
        if new_path.lower() in current_path.lower():
            print_color(f"Path already configured: {new_path}", "yellow")
            return

        # Append new path
        updated_path = current_path
        if updated_path and not updated_path.endswith(";"):
            updated_path += ";"
        updated_path += new_path

        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, updated_path)
        print_color(f"Success: Added {new_path} to User PATH", "green")
        print_color("Note: You need to restart your terminal/IDE for changes to take effect.", "yellow")
        
    except Exception as e:
        print_color(f"Error modifying PATH in registry: {e}", "red")
    finally:
        try:
            winreg.CloseKey(key)
        except:
            pass

def download_file(url, dest_path):
    """Download file with progress indicator"""
    print_color(f"Downloading from: {url}", "cyan")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            total_size = int(response.info().get('Content-Length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    f.write(buffer)
                    if total_size > 0:
                        percent = downloaded * 100 / total_size
                        sys.stdout.write(f"\rProgress: {percent:.1f}%")
                        sys.stdout.flush()
            print() # Newline
        return True
    except Exception as e:
        print_color(f"\nDownload error: {e}", "red")
        return False

def install_manual(use_mirror=False):
    """Download and extract FFmpeg manually"""
    url = f"{MIRROR_PREFIX}{GITHUB_URL}" if use_mirror else GITHUB_URL
    temp_zip = Path(os.environ["TEMP"]) / FFMPEG_FILENAME
    
    if not download_file(url, temp_zip):
        return False

    print_color("Extracting files...", "cyan")
    try:
        if INSTALL_DIR.exists():
            shutil.rmtree(INSTALL_DIR)
        INSTALL_DIR.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
        
        # Find the bin folder containing ffmpeg.exe
        bin_path = None
        for path in INSTALL_DIR.rglob("ffmpeg.exe"):
            bin_path = path.parent
            break
            
        if bin_path:
            print_color(f"Binary found at: {bin_path}", "green")
            add_to_user_path(bin_path)
            
            # Clean up zip
            try:
                os.remove(temp_zip)
            except:
                pass
            return True
        else:
            print_color("Error: Could not find ffmpeg.exe in extracted files.", "red")
            return False
            
    except Exception as e:
        print_color(f"Extraction error: {e}", "red")
        return False

def install_via_winget():
    """Try to install using Windows Package Manager"""
    print_color("Attempting installation via Winget...", "cyan")
    try:
        # Check if winget exists
        subprocess.run(["winget", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Install
        result = subprocess.run(
            ["winget", "install", "Gyan.FFmpeg", "--accept-source-agreements", "--accept-package-agreements"], 
            check=False
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    print_color("Winget installation skipped or failed.", "yellow")
    return False

def main():
    os.system('') # Init ANSI colors for Windows
    print_color("=== FFmpeg Auto-Installer (Python Version) ===", "green")

    if platform.system() != "Windows":
        print_color("This script is designed for Windows.", "red")
        return

    if check_ffmpeg_installed():
        print_color("FFmpeg is already installed!", "green")
        return

    # Method 1: Winget
    if install_via_winget():
        print_color("Installation via Winget successful!", "green")
        print_color("Please restart your terminal.", "yellow")
        return

    # Method 2: Direct Download
    print_color("Falling back to manual download...", "yellow")
    if install_manual(use_mirror=False):
        print_color("Installation successful!", "green")
        return

    # Method 3: Mirror Download
    print_color("Direct download failed. Trying domestic mirror...", "yellow")
    if install_manual(use_mirror=True):
        print_color("Installation successful via mirror!", "green")
    else:
        print_color("All installation methods failed.", "red")

if __name__ == "__main__":
    main()

