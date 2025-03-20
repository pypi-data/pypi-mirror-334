from transformers import AutoModelForCausalLM, AutoTokenizer
from openai import OpenAI
import torch
import traceback
import re
import json

class BaseTask:
    def __init__(self):
        pass
    
    def run_prompts(self, prompts, model, endpoint=None, token=None):
        responses = []
        for nop, prompt in enumerate(prompts):
            response = self.run_prompt(prompt, model, endpoint, token)
            responses.append(response)
        return responses
    
    def run_prompt(self, prompt, model, endpoint=None, token=None):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        try:
            if endpoint is None: # HuggingFace alternative:
                device = torch.device("cuda:0") if torch.cuda.is_available() else "cpu"
                self.model = AutoModelForCausalLM.from_pretrained(
                    model, torch_dtype=torch.float16, device_map={"": 0}
                ).to(device)
                self.tokenizer = AutoTokenizer.from_pretrained(model)
                

                text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
                generated_ids = self.model.generate(**model_inputs, max_new_tokens=512)
                generated_ids = [
                    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
                ]
                response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
                
                del self.model
                del self.tokenizer
                torch.cuda.empty_cache()
                
            else: # OpenAI protocol
                client = OpenAI(base_url = endpoint, api_key=token)
                
                response = client.chat.completions.create(
                  model=model, messages=messages
                )
                response = response.choices[0].message.content
            
            response = self.clean_response(response)
            return response
        except Exception as e:
            traceback.print_exc()
            return None         
        
    def run_prompts(self, prompts, model, endpoint=None, token=None):
        responses = []
        for nop, prompt in enumerate(prompts):
            response = self.run_prompt(prompt, model, endpoint, token)
            responses.append(response)
        return responses        
        
    def clean_response(self, response):
        pattern = r'\{[\s\S]*\}'
        match = re.search(pattern, response, re.DOTALL)
        if match:   # 1-line JSON
            json_str = match.group(0)  # Get JSON content
            try:
                j = json.loads(json_str)  # Parse JSON
                return j[self.property_type]
            except json.JSONDecodeError as e:
                return None
        return None