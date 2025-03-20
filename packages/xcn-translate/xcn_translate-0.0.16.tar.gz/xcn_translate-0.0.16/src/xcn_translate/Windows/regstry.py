import winreg

hkey_cur_user = winreg.HKEY_CURRENT_USER

def winreg_cur_user_QueryValueEx(key, sub):
    try:
        with winreg.OpenKey(hkey_cur_user, key) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, sub)
            print("Value:", value)
            return value
    except FileNotFoundError:
        print("Registry key not found.")
    except Exception as e:
        print("Error:", e)
    return None

def winreg_cur_user_SetValueEx(key, sub, value):
    try:
        with winreg.OpenKey(hkey_cur_user, key, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, sub, 0, winreg.REG_SZ, value)
            print("Value set successfully.")
            return True
    except FileNotFoundError:
        print("Registry key not found.")
    except Exception as e:
        print("Error:", e)
    return False


class WinRegCurUser(object):
    def __init__(self, key=None):
        self.hkey_cur_user = winreg.HKEY_CURRENT_USER
        self.key_folder = key

    def check_and_create_key_folder(self, key=None):
        _kfolder = key if key else self.key_folder
        if _kfolder is not None:
            rkey = None
            try:
                rkey = winreg.OpenKey(self.hkey_cur_user, _kfolder, 0, winreg.KEY_READ)
                print(f"[win reg] check Key salready exists.")
            except FileNotFoundError:
                rkey = winreg.CreateKey(self.hkey_cur_user, _kfolder)
                print(f"[win reg] Key {_kfolder} created.")
            finally:
                if 'rkey' in locals():
                    winreg.CloseKey(rkey)
                    return True
        return False

    def remove_all_value(self, key=None):
        _kfolder = key if key else self.key_folder
        if self.check_and_create_key_folder(_kfolder):
            try:
                with winreg.OpenKey(self.hkey_cur_user, _kfolder, 0, winreg.KEY_ALL_ACCESS) as registry_key:
                    # Enumerate and delete each value
                    while True:
                        try:
                            # Enumerate the next value
                            value_name, _, _ = winreg.EnumValue(registry_key, 0)
                            # Delete the value
                            winreg.DeleteValue(registry_key, value_name)
                        except OSError:
                            # No more values, break the loop
                            break
                    return True
            except FileNotFoundError:
                print(f"Subkey {_kfolder} not found.")
            except PermissionError:
                print(f"Insufficient permissions to modify subkey {_kfolder}.")

        return False

    def query_value(self, sub, key=None):
        _kfolder = key if key else self.key_folder
        if self.check_and_create_key_folder(_kfolder):
            try:
                with winreg.OpenKey(self.hkey_cur_user, _kfolder) as reg_key:
                    value, _ = winreg.QueryValueEx(reg_key, sub)
                    print("[win reg] Query Value:", value)
                    return value
            except FileNotFoundError:
                print("[win reg][Query] Registry key not found.")
            except Exception as e:
                print("[win reg][Query] Error:", e)

        return None

    def set_value(self, sub, value, key=None):
        _kfolder = key if key else self.key_folder
        if self.check_and_create_key_folder(_kfolder):
            try:
                with winreg.OpenKey(self.hkey_cur_user, _kfolder, 0, winreg.KEY_WRITE) as reg_key:
                    winreg.SetValueEx(reg_key, sub, 0, winreg.REG_SZ, value)
                    print("[win req][set] operation successfully.")
                    return True
            except FileNotFoundError:
                print("[win reg][set] Registry key not found.")
            except Exception as e:
                print("[win reg][set] Error:", e)
            return False






