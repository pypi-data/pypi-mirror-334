from .table_task import TableTask

class ColumnSummarizer(TableTask):
    def __init__(self):
        self.descriptions = [
            "Please look at the column below and provide a title for the column.",
            "Kindly refer to the column below and suggest a suicolumn title for it.",
            "I'd appreciate it if you could glance at the column and offer a title for it.",
            "Could you spare a moment to look at the column and give it an appropriate title?",
            "Your task is to review the column and come up with a title for it.",
            "Given the column below, could you provide a title that accurately represents its contents?",
            "Here's a column for your consideration; please suggest a title that fits its contents.",
            "I request that you provide a summary of the input column's content.",
            "Kindly give a concise overview of what the input column represents.",
            "Take a moment to summarize the key points of the input column.",
            "Your task is to give a summary of the input column's main information.",
            "Could you spare a moment to summarize the input column's key findings?",
            "I'd appreciate it if you could provide a summary of the input column after examining it.",
            "Given the input column, can you provide a summary that captures its main data?",
            "Here's an input column for your consideration; please offer a summary of its key aspects.",
            "After reviewing the input column, could you provide a brief summary of its main points?",
            "I'd like your input on this column – can you summarize its contents for me?",
            "Please take a look at the input column and provide a concise summary of its data.",
            "Your help is needed in summarizing the input column and its main information.",
            "Summarize the input column and its key details for easy understanding.",
            "Your task is to analyze the input column and provide a summary of its main aspects.",
            "Could you please glance at the input column and offer a summary that captures its essence?",
            "Please provide a summary for the input column after reviewing its contents.",
            "Your input is valued – kindly summarize the input column's data.",
            "Having looked at the input column, can you give a summary that reflects its main points?",
            "Here's an input column that needs summarizing; can you do that for me?",
            "After considering the input column, please provide a summary that best represents it.",
            "I request that you review the column below and give a brief summary of its contents.",
            "Kindly examine the column and provide a concise overview of what it represents.",
            "Take a moment to look at the column and summarize its key points.",
            "Your task is to glance at the column and provide a summary of its contents.",
            "Could you spare a moment to review the column and give a summary of its main information?",
            "I'd appreciate it if you could summarize the column's content after looking at it.",
            "Given the column below, can you provide a summary that captures its main data?",
            "Here's a column for your consideration; please offer a summary of its key findings.",
            "After examining the column, could you provide a brief summary of its main points?",
            "Please take a look at the column and provide a concise summary of its data.",
            "Your help is needed in summarizing the column below and its main information.",
            "Summarize the column and its key details for easy understanding.",
            "Your task is to analyze the column and provide a summary of its main aspects.",
            "Could you please glance at the column and offer a summary that captures its essence?",
            "Please provide a summary for the column after reviewing its contents.",
            "Having looked at the column, can you give a summary that reflects its main points?",
            "Here's a column that needs summarizing; can you do that for me?",
            "After considering the column, please provide a summary that best represents it.",
        ]
        
        self.structure = ("#Task Description: {}\n\n"
                          "#Input:\n"
                          "**Column:**\n{}\n\n"
                          "Return the final result as JSON in the format {{\"summary\": \"<summary of column>\"}}.\n\n"
                          "#Output:")
        
        self.property_type = 'summary'