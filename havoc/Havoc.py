import os
import sys
import ctypes
import winreg
import shutil

# Check for admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Please run this installer as Administrator.")
    sys.exit(1)

# Paths
install_folder = r"C:\Program Files\Havoc"
script_path = os.path.join(install_folder, "havoc_handler.py")

# Python interpreter path (current interpreter)
python_exe = sys.executable

# The handler Python script content
handler_script = '''import sys
import webbrowser

def main():
    if len(sys.argv) < 2:
        print("No URL provided.")
        return

    input_url = sys.argv[1]
    prefix = "havoc://"

    if not input_url.startswith(prefix):
        print("Invalid protocol.")
        return

    path = input_url[len(prefix):]
    final_url = f"https://www.altarweb.com/havoc/{path}index.html"
    webbrowser.open(final_url)

if __name__ == "__main__":
    main()
'''

# Create install folder
os.makedirs(install_folder, exist_ok=True)

# Write the handler script file
with open(script_path, "w", encoding="utf-8") as f:
    f.write(handler_script)

# Registry setup
key_path = r"havoc"
command = f'"{python_exe}" "{script_path}" "%1"'

try:
    # Create key: HKEY_CLASSES_ROOT\havoc
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, "URL:Havoc Protocol")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

        # Create shell\open\command subkey
        with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
            winreg.SetValueEx(cmd_key, None, 0, winreg.REG_SZ, command)

    print("Havoc protocol handler installed successfully!")
    print('Test with Win+R -> havoc://ridge.go')
except PermissionError:
    print("Failed to write to registry. Please make sure you run this script as Administrator.")
except Exception as e:
    print(f"An error occurred: {e}")
