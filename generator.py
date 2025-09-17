from llm_loader import Loader

class Onto_generator:
    
    def __init__(self, model_name:str, load_type='qlora', token=""):
        self.model, self.tokenizer = Loader(model_name=model_name, load_type=load_type, token=token)
        
    def onto_generate(self, input_text):
        encoded_data = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
                **encoded_data,
                max_new_tokens=512
            )
        generated_ids = [
                output_ids[len(input_ids):] 
                for input_ids, output_ids in zip(encoded_data["input_ids"], generated_ids)
            ]
        decoded_data = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return decoded_data 