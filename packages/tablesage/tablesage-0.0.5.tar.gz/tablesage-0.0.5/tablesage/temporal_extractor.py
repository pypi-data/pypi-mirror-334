from .text_task import TextTask

class TemporalExtractor(TextTask):
    def __init__(self):
        self.descriptions = [
            "From the dataset description, extract the temporal span (start and end years) of its content. If the range cannot be determined, respond with 'Unknown'. Format the range as 'XXXX-XXXX'.",
        ]
        
        self.structure = ("#Task Description: {}\n"
                          "#Description: {}\n"
                          "Return the final result as JSON in the format {{\"temporal_span\": \"<temporal_span>\"}}.\n\n"
                          "#Output:")
        
        self.property_type = 'temporal_span'