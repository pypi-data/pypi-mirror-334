from .table_task import TableTask
import json

class ColumnAnnotator(TableTask):
    def __init__(self, file="tablesage/semantic_types.json"):
        self.descriptions = [
            "Please look at the input column and determine the semantic type that can describe *every single* instance the input column. Please only choose one semantic type from the candidate list, and remember that the type you choose has to accurately describe every single entity in the column. If no candidate column type can suitably describe every single instance in the column, please return 'None'. Please only choose one type from the candidate list below, and *do not* create new types.",
        ]

        with open(file) as f:
            types = json.load(f)        
        types = '\n'.join(types)
        self.structure = ("#Task Description: {}\n\n"
                          "#Input:\n**Column:**\n{}\n"
                          f"**Candidate column types:**\n{types}\n\n"
                          "Return the final result as JSON in the format {{\"chosen_semantic_type\": \"<an entry from the candidate list or None>\"}}.\n\n"
                          "#Output:")
        
        self.property_type = 'chosen_semantic_type'