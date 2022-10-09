import os
import sys
import json

try:
    import stashapi.log as log
    from stashapi.tools import human_bytes
    from stashapi.stashapp import StashInterface
except ModuleNotFoundError:
    print("You need to install the stashapp-tools (stashapi) python module. (CLI: pip install stashapp-tools)", file=sys.stderr)

# plugins don't start in the right directory, let's switch to the local directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if not os.path.exists("config.py"):
    with open("bulkimportdefaults.py", 'r') as default:
        config_lines = default.readlines()
    with open("config.py", 'w') as firstrun:
        firstrun.write("from bulkimportdefaults import *\n")
        for line in config_lines:
            if not line.startswith("##"):
                firstrun.write(f"#{line}")

import config

def configfile_edit(configfile, name: str, state: str):
    found = 0
    with open(configfile, 'r') as file:
        config_lines = file.readlines()
    with open(configfile, 'w') as file_w:
        for line in config_lines:
            if name == line.split("=")[0].strip():
                file_w.write(f"{name} = {state}\n")
                found += 1
            elif "#" + name == line.split("=")[0].strip():
                file_w.write(f"{name} = {state}\n")
                found += 1
            else:
                file_w.write(line)
        if not found:
            file_w.write(f"#\n{name} = {state}\n")
            found = 1
    return found

def exit_plugin(msg=None, err=None):
    if msg is None and err is None:
        msg = "plugin ended"
    output_json = {"output": msg, "error": err}
    print(json.dumps(output_json))
    sys.exit()

def importstudios():
    with open("studios.txt", 'r') as file:
        config_lines = file.readlines()
    for studioname in config_lines:
        log.debug(studioname)
        if studioname:
           studio = {}
           studio["name"] = studioname
           result = stash.find_studio(studio, create=True)
           log.debug(result)
    return

def main():
    global stash
    json_input = json.loads(sys.stdin.read())
    FRAGMENT_SERVER = json_input["server_connection"]
    stash = StashInterface(FRAGMENT_SERVER)
    PLUGIN_ARGS = False
    HOOKCONTEXT = False

    try:
        PLUGIN_ARGS = json_input['args']["mode"]
    except:
        pass

    if PLUGIN_ARGS:
        log.debug("--Starting Plugin 'Bulk Import'--")
        if "importstudios" in PLUGIN_ARGS:
            log.info("Importing Studio list in bulk")
            importstudios()
        exit_plugin("Bulk Import plugin finished")

    exit_plugin()

main()

