from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
def load_model(model_name, device,dtype):
    torch_dtype = getattr(torch, dtype)
    model = AutoModelForCausalLM.from_pretrained(
        model,
        torch_dtype=torch_dtype,
        device_map=device,
        low_cpu_mem_usage=True
    )
    state_dict = model.state_dict()
    return model, state_dict

class SetTokenizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target": ("target", {
                }),
                "save_name": ("save_name", {
                }),
            },
        }
    FUNCTION = "set_tokenizer"
    RETURN_TYPES = ()
    OUTPUT_NODE = True

    CATEGORY = "mergetool_llm"
    def set_tokenizer(self, target,save_name):
        tokenizer = AutoTokenizer.from_pretrained(target)
        tokenizer.save_pretrained(save_name)
        print("tokenizer save done")

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SetTokenizer": SetTokenizer
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "load and save tokenizer": "SetTokenizer"
}
