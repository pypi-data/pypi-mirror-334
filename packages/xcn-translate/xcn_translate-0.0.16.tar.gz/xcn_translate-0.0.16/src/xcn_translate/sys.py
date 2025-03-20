
def get_platform(self):
    import platform
    system_name = platform.system().lower()
    if 'linux' in system_name:
        return 'linux64'
    elif 'darwin' in system_name:
        return 'mac-arm64' if platform.processor() == 'arm' else 'mac-x64'
    elif 'win' in system_name:
        return 'win64' if platform.architecture()[0] == '64bit' else 'win32'
    else:
        raise ValueError(f"Unsupported platform: {system_name}")

def update_sys_path_with__file(file_o):
    import sys
    from pathlib import Path
    folder_path = None
    if file_o:
        folder_path = str(Path(file_o).absolute().parent)
        if folder_path not in sys.path:
            sys.path.append(folder_path)
    return folder_path
