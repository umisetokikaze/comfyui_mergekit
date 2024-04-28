

class SetLayer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "include": ("STRING", {
                    "default": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
                }),
                "exclude": ("STRING", {
                    "default": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
                }),

            },
        }

    RETURN_TYPES = ("include","exclude")

    FUNCTION = "get_parse"

    #OUTPUT_NODE = False

    CATEGORY = "mergetool_llm"

    def set_parse(self,exclude,include):
        return exclude,include

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SetLayer": SetLayer
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "str to parsed layers": "Set Layer"
}
