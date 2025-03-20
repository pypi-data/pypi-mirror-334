from .text_task import TextTask

class InsightsExtractor(TextTask):
    def __init__(self):
        self.descriptions = [
            "Given the following information about the columns of a table, provide a list of useful insights about the data. These can include possible visualizations, correlations between columns, etc."
            ]
        
        self.structure = (
            "#Task Description: {}\n\n"
            "#Input:\n{}\n\n"
            "Return the final result as JSON in the format {{\"insights\": <list_of_insights>}}.\n\n"
            "# Output:"
        )
        
    def create_prompt(self, profiles):
        description = self.descriptions[0]
        
        info = ''
        for col, properties in profiles.items():
            info += f'*{col}*:\n'
            for property, val in properties.items():
                if type(val) != list:
                    info += f'\t{property}: {val}\n'
                else:
                    info += f'\t{property}:\n'
                    for term in val:
                        info += "\t\t"+str(term)[1:-1].replace("'", "")+'\n'
        
        self.property_type = "insights"
        prompt = self.structure.format(description, info)
    
        return prompt
