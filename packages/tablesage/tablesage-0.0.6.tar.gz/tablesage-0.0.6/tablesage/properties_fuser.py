from .text_task import TextTask

class PropertiesFuser(TextTask):
    def __init__(self):
        self.descriptions = [
            "Given the following information that describe a table, i.e. table description, column descriptions and insights, construct a more comprehensive and detailed description about the table. Make sure to merge key elements, expand on areas that can provide more clarity, and avoid redundancy. Do not repeat any information verbatim in the output."
            ]
        
        self.structure = (
            "#Task Description: {}\n\n"
            "#Input:\n"
            "##Table Description:\n{}\n"
            "##Column Descriptions:\n{}\n"
            "##Insights:\n{}\n"
            "Return the final result as JSON in the format {{\"description\": <description>}}.\n\n"
            "# Output:"
        )
        
    def create_prompt(self, table_description, column_descriptions, insights):
        description = self.descriptions[0]
        
        column_str = ''
        for noc, (col, desc) in enumerate(column_descriptions.items()):
            column_str += f'{noc+1}. {col}: {desc}\n'
            
        insights_str = ''
        if insights is None:
            insights = []
        for noc, ins in enumerate(insights):
            insights_str += f'{noc+1}. {ins}\n'
        
        self.property_type = "description"
        prompt = self.structure.format(description, table_description,
                                       column_str, insights_str)
    
        return prompt