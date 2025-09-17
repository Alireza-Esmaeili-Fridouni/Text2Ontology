def prompt_filler(promt_template, instruction, text, sentence, tokenizer):
    prompt = promt_template.format(text=text, sentence=sentence)
    txt = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]
    message = tokenizer.apply_chat_template(
           txt,
           tokenize = False,
           add_generation_prompt=True 
        )
    return message  
        