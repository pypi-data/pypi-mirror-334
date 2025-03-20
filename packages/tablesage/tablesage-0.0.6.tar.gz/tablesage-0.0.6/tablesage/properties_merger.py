from .text_task import TextTask

class PropertiesMerger(TextTask):
    def __init__(self):
        self.descriptions = {
            "column_type": "Given the following column semantic types, provide a single table semantic type that combines and covers all of them.",
            "table_type": "Given the following table semantic types, provide a single table semantic type that combines and covers all of them.",
            "column_summary": "Given the following column summaries, provide a single column summary that combines and covers all of them.",
            "table_summary": "Given the following table summaries, provide a single table summary that combines and covers all of them.",
            "temporal_span": "Given the following temporal spans, provide a single temporal span that combines and covers all of them.", 
            "spatial_coverage": "Given the following spatial coverages, provide a single spatial coverage that combines and covers all of them.", 
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
            "Return the final result as JSON in the format {{\"{}\": \"<final result>\"}}.\n\n"
            "# Output:"
        )
        
    def create_prompt(self, properties, property_type):
        description = self.descriptions.get(property_type, "Provide a combined result for the given properties.")
        input_label = self.input_labels.get(property_type, "Properties")
        
        partials = "\n".join(f"{nop+1}. {property}" for nop, property in enumerate(properties) if property is not None)
    
        self.property_type = property_type
        prompt = self.structure.format(description, input_label, partials, property_type)
    
        return prompt
