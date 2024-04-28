from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
def load_model(model_name, device,dtype):
    torch_dtype = getattr(torch, dtype)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch_dtype,
        device_map=device,
        low_cpu_mem_usage=True
    )
    state_dict = model.state_dict()
    return model, state_dict

class LoadLR:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_dict": ("model_dict", {
                }),
                "device": ("STRING", {
                    "multiline": False,
                    "default": "cpu"
                }),
                "dtype": ("STRING", {
                    "multiline": False,
                    "default": "bfloat16"
                }),
            },
        }

    RETURN_TYPES = ("left_model","right_model","velocity",)

    FUNCTION = "load_left_right_models"

    #OUTPUT_NODE = False

    CATEGORY = "mergetool_llm"
    def load_left_right_models(self, model_dict,device,dtype):
        velocity = model_dict["velocity"]
        left_weight, left_state_dict = load_model(model_dict["left"], device,dtype)
        right_weight, right_state_dict = load_model(model_dict["right"], device,dtype)
        # del base_weight, sub_weight
        print("all loaded")
        return (left_weight, left_state_dict), (right_weight, right_state_dict), velocity


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadLR": LoadLR
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "loding llm model": "LoadLR"
}
