import os
from pathlib import Path

class DefineSaveName:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "save_dir": ("STRING", {
                    "multiline": False,
                    "default": "model_name"
                }),
                "model_dict": ("model_dict", {
                }),
                "target": ("target", {
                }),
            },
        }
    RETURN_TYPES = ("save_name",)
    CATEGORY = "mergetool_llm"
    FUNCTION = "define_savename"
    def define_savename(self, save_dir, model_dict,target):
        def get_savename(path):
            path_path = Path(path)
            path_parts = path_path.parts
            if path_parts[0] == "/" or ":\\" in path_parts[0]:
                path_parts = path_parts[1:]
            return "-".join(path_parts)
        left = get_savename(model_dict["left"])
        right = get_savename(model_dict["right"])
        model_name =  f"{left}_{right}"
        if target is not None:
            target_name = get_savename(target)
            save_name = os.path.join(save_dir, target_name, model_name)
        else:
            save_name = os.path.join(save_dir, "vector", model_name)
        return save_name


NODE_CLASS_MAPPINGS = {
    "DefineSaveName": DefineSaveName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DefineSaveName": "create save name"
}
