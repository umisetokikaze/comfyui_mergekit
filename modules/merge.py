
import tqdm
skip_layernorm = True

def Add(v, k, base_state_dict, sub_state_dict, velocity):
    return ((base_state_dict[k] + sub_state_dict[k]).to(v) * velocity)

def Sub(v, k, base_state_dict, sub_state_dict, velocity):
    return ((base_state_dict[k] - sub_state_dict[k]).to(v) * velocity)

def Mul(v, k, base_state_dict, sub_state_dict, velocity):
    return ((base_state_dict[k] * sub_state_dict[k]).to(v) * velocity)

def Div(v, k, base_state_dict, sub_state_dict, velocity):
    return ((base_state_dict[k] / sub_state_dict[k]).to(v) * velocity)

def Mix(v, k, base_state_dict, sub_state_dict, velocity):
    return (base_state_dict[k]*(1.0 - velocity) + sub_state_dict[k]*velocity).to(v)

def parse_layers(layers_str):
        if layers_str is None:
            return None
        return layers_str.split(',')

def merge(target_model,left_model,right_model, velocity, skip_layers, operation, include_layers, exclude_layers,savename):
    target_weight, target_state_dict = target_model
    right_weight, left_state_dict = left_model
    right_weight, right_state_dict = right_model
    target = target_state_dict
    if target_state_dict is None:
        target = left_state_dict
    operation_dict = {
        "add": Add,
        "sub": Sub,
        "mul": Mul,
        "div": Div,
        "mix": Mix,
    }
    included_layers = []
    excluded_layers = []
    with tqdm(target.keys()) as pbar:
        for k in pbar:
            if (k in skip_layers) or (skip_layernorm and "layernorm" in k):
                excluded_layers.append(k)
                continue
            if include_layers is not None:
                for j in include_layers:
                    if j not in k:
                        excluded_layers.append(k)
                        continue
            if exclude_layers is not None:
                for j in exclude_layers:
                    if j in k:
                        excluded_layers.append(k)
                        continue
            included_layers.append(k)
            v = target[k]
            pbar.set_description(k)
            if target_state_dict is not None:
                v.copy_(v + operation_dict[operation](v, k, left_state_dict, right_state_dict, velocity))
            else:
                v.copy_(operation_dict[operation](v, k, left_state_dict, right_state_dict, velocity))

    print("Included Layers:")
    print(included_layers)
    print("Excluded Layers:")
    print(excluded_layers)

    target_model.save_pretrained(savename)


class Merge:
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
                "skip_layers": ("skip_layers", {
                }),
                "velocity": ("velocity", {
                }),
                "calc": ("STRING", {
                    "default": "add"
                }),
                "inc": ("include", {
                    "default": ""
                }),
                "exc": ("exclude", {
                    "default": ""
                }),
                "save_name": ("save_name", {
                    "default": ""
                }),

            },
        }

    RETURN_TYPES = ()

    FUNCTION = "set_models"

    OUTPUT_NODE = True

    CATEGORY = "mergetool_llm"

    def set_models(self, target_model,left_model, right_model,skip_layers,velocity,calc,inc,exc,save_name):
        inc = parse_layers(inc)
        exc = parse_layers(exc)
        merge(target_model,left_model, right_model, velocity, skip_layers, calc, inc, exc,save_name)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Merge": Merge
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Merge": "run merge"
}
