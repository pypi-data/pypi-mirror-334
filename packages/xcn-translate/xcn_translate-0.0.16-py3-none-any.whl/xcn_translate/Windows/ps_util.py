
import psutil

def process_list(keyword=None):
    processlist = []

    if keyword is None:
        for process in psutil.process_iter():
            if process.status() == 'running':
                processlist.append(process)
    else:
        for process in psutil.process_iter():
            if process.status() == 'running' and keyword.lower() in process.name().lower():
                processlist.append(process)

    return processlist

def list_cmdline_by_name(name, loggerd=print):
    loggerd(f">>list cmdline by name: {name}")
    ret = []
    try:
        plist = process_list(name)
        for p in plist:
            cl = p.cmdline()
            ret.append(cl.copy())
            loggerd(f"\t {cl}")
    except Exception as e:
        loggerd(f"Error: {e}")
    return ret

def find_process_by_cmdline(name, cmdlist, loggerd=print, ignorexec=False):
    loggerd(f">>find process by cmdline: {name}")

    try:
        plist = process_list(name)
        for p in plist:
            cl = p.cmdline()
            if ignorexec:
                cl = cl[1:] if len(cl)>1 else []
            if len(cl) == len(cmdlist):
                for i in range(len(cl)):
                    if cl[i] != cmdlist[i]:
                        break
                else:
                    return p
    except Exception as e:
        loggerd(f"Error: {e}")

    return None

class xPsUtil:
    def __init__(self):
        pass


if __name__ == "__main__":
    pList = process_list("python")
    for p in pList:
        cl = p.cmdline()
        print(cl)
    pass
