from .base_task import BaseTask

class TextTask(BaseTask):
    def __init__(self):
        pass

    def create_prompt(self, summary, description_ids=0):
        descriptions = self.descriptions
        structure = self.structure
        
        if type(description_ids) == int:
            description_ids = [description_ids]

        prompts = []            
        for description_id in description_ids:
            if type(description_id) == str: #direct description
                description = description_id
            elif type(description_id) == int:
                if description_id >= len(descriptions):
                    raise ValueError("ID not in available templates, please provide a value between 0 and {}.".format(len(descriptions)))
                description = descriptions[description_id]
            else:
                raise ValueError("Wrong type of descriptions")
            prompt = structure.format(description, summary)
            prompts.append(prompt)
        return prompts
    
    def run(self, summary, model, description_ids=0, endpoint=None, token=None):
        prompts = self.create_prompt(summary, description_ids)
        responses = self.run_prompts(prompts, model, endpoint, token)
        return responses    