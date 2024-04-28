import os

class DumpLayers:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "state_dict": ("state_dict", {
                }),},
        }

    def dump_layers(self, model_state_dict, savename):
        os.makedirs(os.path.dirname(savename), exist_ok=True)
        layer_names = list(model_state_dict.keys())
        with open(f"{savename}_layers.txt", "w") as f:
            f.write("\n".join(layer_names))
        print(f"Layer names dumped to {savename}_layers.txt")
        print("Layer names:")
        print("\n".join(layer_names))

    OUTPUT_NODE = False

    RETURN_TYPES = ()

    FUNCTION = "dump_layers"
    CATEGORY = "mergetool_llm"

NODE_CLASS_MAPPINGS = {
    "SetModels": DumpLayers
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "create models list": "SetModels"
}
