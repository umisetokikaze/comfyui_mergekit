
class SetModels:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "left": ("STRING", {
                    "multiline": False, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Hello World!"
                }),

                "right": ("STRING", {
                    "default": "path/to/model"
                }),

                "base": ("STRING", {
                    "default": "path/to/model",
                }),

                "velocity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "velocity"}),

            },
        }

    RETURN_TYPES = ("model_dict", "target",)

    FUNCTION = "set_models"

    #OUTPUT_NODE = False

    CATEGORY = "mergetool_llm"

    def set_models(self, left, right, base,velocity):
        model_dict = {"left":left,"right":right,"velocity":velocity}
        return model_dict, base


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SetModels": SetModels
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "create models list": "Set models"
}
