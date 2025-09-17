from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType
import torch


class LLMLoader:
    def __init__(self, model_name:str, token:str=""):
        self.model_name = model_name
        self.token = token
        
    def simple_model(self):
        model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                use_auth_token=self.token,
                device_map="auto")
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.token)
        return model, tokenizer
    
    # QloRa 
    def qlora_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.token)
        tokenizer.pad_token = tokenizer.eos_token
        quant_config = BitsAndBytesConfig(load_in_4bit=True,
                                          bnb_4bit_use_double_quant=False,
                                          bnb_4bit_quant_type="nf4",
                                          bnb_4bit_compute_dtype=torch.bfloat16)
        model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                use_auth_token=self.token,
                quantization_config=quant_config,
                device_map="auto")
        target_modules = ["q_proj", "v_proj"]
        lora_config = LoraConfig(
                      task_type=TaskType.CAUSAL_LM,
                      r=16,
                      lora_alpha=32,
                      target_modules= target_modules,  
                      lora_dropout=0.1,  
                      bias="none")
        qlora_model = get_peft_model(model, lora_config)
        return qlora_model, tokenizer
    
class Loader:
    model_loader = {
        "simple": "simple_model",
        "qlora": "qlora_model"
        }
    # def __new__(cls, model_name:str, load_type:str, token=""):
    #     loader = "LLMLoader(model_name=model_name, token=token)." + Loader.model_loader.get(load_type, "simple_model") + "()"
    #     return eval(loader)
    
    def __new__(cls, model_name:str, load_type:str, token=""):
        llm_loader = LLMLoader(model_name=model_name, token=token)
        method_name = cls.model_loader.get(load_type, "simple_model")
        method = getattr(llm_loader, method_name)
        return method()
        
        