from .table_task import TableTask
import json

class TableAnnotator(TableTask):
    def __init__(self, file="tablesage/semantic_types.json"):
        self.descriptions = [
            "Please look at the input table and determine the semantic type that best describes the table as a whole. The semantic type should reflect the main concept represented by all the columns together. Please only choose one semantic type from the candidate list, and remember that the type you choose has to accurately describe the entire table. If no candidate type can suitably describe the table, please return 'None'. Please only choose one type from the candidate list below, and *do not* create new types.",
        ]

        with open(file) as f:
            types = json.load(f)        
        types = '\n'.join(types)
        self.structure = ("#Task Description: {}\n\n"
                          "#Input:\n"
                          "**Table:**\n{}\n"
                          f"**Candidate table types:**\n{types}\n\n"
                          "Return the final result as JSON in the format {{\"chosen_semantic_type\": \"<an entry from the candidate list or None>\"}}.\n\n"
                          "#Output:")
        
        self.property_type = 'chosen_semantic_type'