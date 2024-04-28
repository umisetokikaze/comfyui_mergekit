from asyncio import log
import sys, os
from pathlib import Path
import importlib
import traceback

here = Path(__file__).parent.resolve()
sys.path.insert(0, str(Path(here, "src").resolve()))
for pkg_name in ["controlnet_aux", "custom_mmpkg"]:
    sys.path.append(str(Path(here, "src", pkg_name).resolve()))


def load_nodes():
    shorted_errors = []
    full_error_messages = []
    node_class_mappings = {}
    node_display_name_mappings = {}

    for filename in (here / "modules").iterdir():
        module_name = filename.stem
        if module_name.startswith('.'): continue #Skip hidden files created by the OS (e.g. [.DS_Store](https://en.wikipedia.org/wiki/.DS_Store))
        try:
            module = importlib.import_module(
                f".modules.{module_name}", package=__package__
            )
            node_class_mappings.update(getattr(module, "NODE_CLASS_MAPPINGS"))
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                node_display_name_mappings.update(getattr(module, "NODE_DISPLAY_NAME_MAPPINGS"))

            log.debug(f"Imported {module_name} nodes")

        except AttributeError:
            pass  # wip nodes
        except Exception:
            error_message = traceback.format_exc()
            full_error_messages.append(error_message)
            error_message = error_message.splitlines()[-1]
            shorted_errors.append(
                f"Failed to import module {module_name} because {error_message}"
            )
    return node_class_mappings, node_display_name_mappings

NODE_MAPPINGS, DISPLAY_NAME_MAPPINGS = load_nodes()

NODE_CLASS_MAPPINGS = {**NODE_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**DISPLAY_NAME_MAPPINGS}