

class GetSkip:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_model": ("target_model", {
                }),
                "left_model": ("left_model", {
                }),
                "right_model": ("right_model", {
                }),
                },

        }

    RETURN_TYPES = ("skip_layers",)

    FUNCTION = "get_skip_layers"

    #OUTPUT_NODE = False

    CATEGORY = "mergetool_llm"


    def get_skip_layers(self, target_model, left_model, right_model):
        target_state_dict = target_model.state_dict()
        right_weight, left_state_dict = left_model
        right_weight, right_state_dict = right_model
        # それぞれのstate_dictからキーとテンソルのサイズを取得し、比較する。もしも合致しないものがあればそれだけを表示する。
        skip_layers = []
        target = target_state_dict
        if target_state_dict is None:
            target = left_state_dict
        for target_key in target.keys():
            # if base_state_dict[target_key].size() != target_state_dict[target_key].size() \
            #     or sub_state_dict[target_key].size() != target_state_dict[target_key].size():
            if target_key not in right_state_dict.keys():
                print(f" left key not found: {target_key}, skip...")
                skip_layers.append(target_key)
                continue
            if left_state_dict[target_key].size() != right_state_dict[target_key].size() \
                or (target_state_dict is not None and left_state_dict[target_key].size() != target_state_dict[target_key].size()):
                print(f"\n ------------------------------------")
                print(f" mismatch size: {target_key}")
                print(f" tensor size")
                if target_state_dict is not None:
                    print(f"  target: {target_state_dict[target_key].size()}")
                print(f"  left  : {left_state_dict[target_key].size()}")
                print(f"  right   : {right_state_dict[target_key].size()}")
                skip_layers.append(target_key)

        if len(skip_layers) == 0:
            print()
            print(" match all layer tensor size")
        else:
            print(skip_layers)
        return [skip_layers]

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "get_skip": GetSkip
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "get skip layers": "get skip"
}