import os
import sys
import subprocess

def check_safe_directory():
    current_dir = os.getcwd().lower()
    if "downloads" in current_dir or "compressed" in current_dir:
        print("ERROR: You are running this script from inside a Downloads or Compressed folder!")
        print("Please move your project folder to a clean path (like C:\\ProsperoMgr) and run it from there.")
        sys.exit(1)

def run_git_sync():
    check_safe_directory()
    
    choice = input("Do you want to wipe all past commit history? (y/n): ").strip().lower()
    commit_message = input("Please enter the commit message: ").strip()
    
    if not commit_message:
        print("Commit message cannot be empty!")
        return

    try:
        if choice == 'y':
            print("Wiping history and creating a fresh main branch...")
            # پاک کردن پوشه .git قبلی و ساخت دوباره آن به صورت تمیز
            subprocess.run(["rmdir", "/s", "/q", ".git"], shell=True, check=False)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/DavSpencer/ProsperoMAN.git"], check=True)
            subprocess.run(["git", "checkout", "-b", "main"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("Force pushing fresh history to GitHub...")
            subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
            print("\nDone! History was wiped and remote files replaced on main.")

        else:
            print("Preserving history. Preparing to update remote files...")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=False)
            print("Force pushing local files to overwrite remote differences...")
            subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
            print("\nDone! Local files replaced remote files, and history was preserved.")

    except subprocess.CalledProcessError as e:
        print(f"\nError executing Git commands: {e}")

if __name__ == "__main__":
    run_git_sync()