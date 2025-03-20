from .text_task import TextTask

class SpatialExtractor(TextTask):
    def __init__(self):
        self.descriptions = [
            "From the dataset description, extract the country associated with its content. If the country cannot be determined, respond with 'Unknown'",
        ]
        
        self.structure = ("#Task Description: {}\n"
                          "#Description: {}\n"
                          "Return the final result as JSON in the format {{\"spatial_coverage\": \"<spatial_coverage>\"}}.\n\n"
                          "#Output:")
        
        self.property_type = 'spatial_coverage'