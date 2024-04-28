from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LoadTarget:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target": ("target", {}),
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

    RETURN_TYPES = ("target_model",)

    FUNCTION = "load_models"

    #OUTPUT_NODE = False

    CATEGORY = "mergetool_llm"

    def load_model(self, model_name, device,dtype):
        torch_dtype = getattr(torch, dtype)
        weight = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            device_map=device,
            low_cpu_mem_usage=True
        )
        state_dict = weight.state_dict()
        return (weight, state_dict)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadTarget": LoadTarget
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "loding target model": "LoadTarget"
}
