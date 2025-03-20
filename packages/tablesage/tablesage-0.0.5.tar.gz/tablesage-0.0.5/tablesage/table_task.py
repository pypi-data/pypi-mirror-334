from .base_task import BaseTask

class TableTask(BaseTask):
    def __init__(self):
        pass
    
    def serialize_table(self, df):
        header = '|' + '|'.join(df.columns) + '|'
        separator = '|' + '|'.join('---' for _ in df.columns) + '|'
        content = '\n'.join('|' + '|'.join(str(val).strip() for val in row) + '|' for row in df.fillna('').values)
        return f"{header}\n{separator}\n{content}"

    def create_prompt(self, df, description_ids=0):
        descriptions = self.descriptions
        structure = self.structure
        
        df_str = self.serialize_table(df)

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
            prompt = structure.format(description, df_str)
            prompts.append(prompt)
        return prompts
        
    def run(self, df, model, description_ids=0, endpoint=None, token=None):
        prompts = self.create_prompt(df, description_ids)
        responses = self.run_prompts(prompts, model, endpoint, token)
        return responses
