from .text_task import TextTask

class PropertiesComparer(TextTask):
    def __init__(self):
        self.descriptions = {
            "column_type": "Given the following column semantic types, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
            "table_type": "Given the following table semantic types, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
            "column_summary": "Given the following column summaries, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
            "table_summary": "Given the following table summaries, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
            "temporal_span": "Given the following temporal spans, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
            "spatial_coverage": "Given the following spatial coverages, provide a list of comparisons that also reports the advantanges and disadvantages of each one.",
        }

        self.input_labels = {
            "column_type": "Semantic Types",
            "table_type": "Semantic Types",
            "column_summary": "Summaries",
            "table_summary": "Summaries",
            "temporal_span": "Temporal Span", 
            "spatial_coverage": "Spatial Coverage", 
        }

        self.structure = (
            "#Task Description: {}\n\n"
            "#Input:\n**{}:**\n{}\n\n"
            "Return the final result as JSON in the format {{\"comparisons\": <list_of_comparisons>}}.\n\n"
            "# Output:"
        )
        
    def create_prompt(self, properties, property_type):
        description = self.descriptions.get(property_type, "Provide a list of comparisons for the given properties.")
        input_label = self.input_labels.get(property_type, "Properties")
        
        partials = "\n".join(f"{nop+1}. {property}" for nop, property in enumerate(properties) if property is not None)
    
        self.property_type = "comparisons"
        prompt = self.structure.format(description, input_label, partials, property_type)
    
        return prompt
