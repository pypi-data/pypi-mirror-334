import pandas as pd
from .table_summarizer import TableSummarizer
from .column_summarizer import ColumnSummarizer
from .table_annotator import TableAnnotator
from .column_annotator import ColumnAnnotator
from .properties_merger import PropertiesMerger
from .temporal_extractor import TemporalExtractor
from .spatial_extractor import SpatialExtractor
from .properties_comparer import PropertiesComparer
from .insights_extractor import InsightsExtractor
from .properties_fuser import PropertiesFuser
from collections import Counter
import random

class TableSage:
    
    def __init__(self):
        pass
    
    def load_dataset(self, file, separator=',', encoding='utf-8', engine='python'):
        try:
            self.df = pd.read_csv(file, sep=separator, encoding=encoding, engine='python')
            # self.df = self.df[['NN', 'Adresa']]
        except Exception as e:
            self.df = None
            raise e
            
    def sample(self, df, sampling='random', sampling_number=5):
        if sampling == 'random':
            sample = df.head(sampling_number)
        return sample
    
    def create_profile(self):
        profiles = {}
        for col in self.df:
            profile = self.df[col].describe().to_dict()
            if self.df[col].dtype in ["float64", "int64"]:
                profiles[col] = profile
            elif self.df[col].dtype in ["object", "category"]:
                profile = {k:v for k,v in profile.items() if k in ['count', 'unique']}
                c = Counter(self.df[col].values)
                no = 5
                profile[f'top-{no}'] = [{'term': k, 'frequency': v} for k,v in c.most_common(no)]
                profiles[col] = profile
        return profiles
            
    ############### Table-Related Features ####################################
    
    def summarize_table(self, model, description_ids=0, sampling='random',
                        sampling_number=5, endpoint=None, token=None, verbose=False):
        ts = TableSummarizer()
        sampled_df = self.sample(self.df, sampling, sampling_number)
        responses = ts.run(sampled_df, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'table_summary', endpoint, token) #TODO: Merger should be different
        if verbose:
            result['responses'] = responses
        return result
        
    def summarize_column(self, column, model, description_ids=0, sampling='random',
                         sampling_number=5, endpoint=None, token=None, verbose=False):
        cs = ColumnSummarizer()
        if column not in self.df:
            raise ValueError('Column {} not in DataFrame.'.format(column))
        sampled_df = self.df[column].to_frame()
        sampled_df = self.sample(sampled_df, sampling, sampling_number)
        responses = cs.run(sampled_df, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'column_summary', endpoint, token) #TODO: Merger should be different
        if verbose:
            result['responses'] = responses
        return result
    
    def annotate_table(self, model, description_ids=0, sampling='random', sampling_number=5,
                        endpoint=None, token=None, verbose=False):
        ta = TableAnnotator()
        sampled_df = self.sample(self.df, sampling, sampling_number)
        responses = ta.run(sampled_df, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'table_type', endpoint, token) #TODO: Merger should be different
        if verbose:
            result['responses'] = responses
        return result
    
    def annotate_column(self, column, model, description_ids=0, sampling='random', 
                       sampling_number=5, endpoint=None, token=None, verbose=False):
        ca = ColumnAnnotator()
        if column not in self.df:
            raise ValueError('Column {} not in DataFrame.'.format(column))
        sampled_df = self.df[column].to_frame()
        sampled_df = self.sample(sampled_df, sampling, sampling_number)
        responses = ca.run(sampled_df, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'column_type', endpoint, token) #TODO: Merger should be different
        if verbose:
            result['responses'] = responses
        return result
    
    ############### Extraction-Related Features ###############################
    def extract_temporal(self, summary, model, description_ids=0, 
                         endpoint=None, token=None, verbose=False):
        if summary is None:
            raise ValueError('Summary cannot be None!')
        te = TemporalExtractor()
        responses = te.run(summary, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'temporal_span', endpoint, token)
        if verbose:
            result['responses'] = responses
        return result
    
    def extract_spatial(self, summary, model, description_ids=0, 
                        endpoint=None, token=None, verbose=False):
        if summary is None:
            raise ValueError('Summary cannot be None!')
        se = SpatialExtractor()
        responses = se.run(summary, model, description_ids, endpoint, token)
        result = self.merge_properties(responses, model, 'spatial_coverage', endpoint, token)
        if verbose:
            result['responses'] = responses
        return result    
    
    def extract_insights(self, properties, model, endpoint=None, token=None):
        profiles = self.create_profile()
        for col in properties:
            for k,v in properties[col].items():
                profiles[col][k] = v
        ie = InsightsExtractor()
        prompt = ie.create_prompt(profiles)
        response = ie.run_prompt(prompt, model, endpoint, token)
        return {'result': response}

    
    ############### Comparison-Related Features ###############################
    def compare_properties(self, properties, model, property_type='properties', endpoint=None, 
                         token=None):
        pc = PropertiesComparer()
        prompt = pc.create_prompt(properties, property_type)
        response = pc.run_prompt(prompt, model, endpoint, token)
        return {'result': response}
    
    ############### Fusion-Related Features ###################################
    
    def merge_properties(self, properties, model, property_type='properties', endpoint=None, 
                         token=None):
        pm = PropertiesMerger()
        prompt = pm.create_prompt(properties, property_type)
        response = pm.run_prompt(prompt, model, endpoint, token)
        return {'result': response}
 
    def fuse_properties(self, table_description, column_descriptions, insights, model, property_type='properties', endpoint=None, 
                         token=None):
        pf = PropertiesFuser()
        prompt = pf.create_prompt(table_description, column_descriptions, insights)
        response = pf.run_prompt(prompt, model, endpoint, token)
        return {'result': response}
    
    ############### Profile-Related Features ##################################
    
    def profile_dataset(self, model, table_prompt_ids=None, 
                        column_prompt_ids=None, endpoint=None, token=None,
                        official_table_description=None, 
                        official_column_descriptions=None,
                        no_prompts=3, verbose=False):

        if type(model) == str:
            model = [model]
        
        ################ Table Summarization ##################################
        print('Starting Table Summarization...')
        if table_prompt_ids is None:
            table_description_ids = random.sample(range(45), no_prompts)

        table_descriptions = []
        for m in model:
            responses = self.summarize_table(m, description_ids=table_description_ids,
                                             endpoint=endpoint, token=token)
            table_descriptions += [responses['result']]
            
        if official_table_description is not None:
            table_descriptions += [official_table_description]
                
        table_description = self.merge_properties(table_descriptions, model=m,
                                                  property_type='table_summary',
                                                  endpoint=endpoint, token=token)
        table_description = table_description['result']
        
        ################ Column Summarization #################################
        print('Starting Column Profiling...')
        column_info = {}
        column_info_descriptions = {}
        for col in self.df:
            print("\t", col)
            if column_prompt_ids is None:
                column_description_ids = random.sample(range(45), no_prompts)
    
            column_descriptions = []
            for m in model:
                responses = self.summarize_column(col, m, description_ids=column_description_ids,
                                                 endpoint=endpoint, token=token)
                column_descriptions += [responses['result']]
                
            if official_column_descriptions is not None and col in official_column_descriptions:
                column_descriptions += [official_column_descriptions[col]]
                    
            column_description = self.merge_properties(column_descriptions, model=m,
                                                      property_type='column_summary',
                                                      endpoint=endpoint, token=token)
            column_description = column_description['result']
            
            column_types = []
            for m in model:
                responses = self.annotate_column(col, m, description_ids=0,
                                                 endpoint=endpoint, token=token)
                column_types += [responses['result']]
                
            column_type = self.merge_properties(column_types, model=m,
                                                property_type='column_type',
                                                endpoint=endpoint, token=token)
            column_type = column_type['result']
            column_info[col] = {'type': column_type, 'summary': column_description}
            column_info_descriptions[col] = column_description
            
        ################# Insights Extraction #################################
        print('Starting Insights Extraction...')
        insights = self.extract_insights(column_info, m,
                                          endpoint=endpoint, token=token)
        insights = insights['result']
        
        ################# Properties Fusion ###################################
        print('Starting Properties Fusion...')
        profile = self.fuse_properties(table_description, column_info_descriptions,
                                       insights, m, endpoint=endpoint, token=token)
        profile = profile['result']
        
        result = {'result': profile}
        if verbose:
            result['table_description'] = table_description
            result['column_info'] = column_info
            result['insights'] = insights
        return result