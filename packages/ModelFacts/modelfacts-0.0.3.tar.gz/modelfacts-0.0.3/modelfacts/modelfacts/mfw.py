import ipywidgets as ipyw
from ipywidgets import Layout
import datetime as dt
import io
import pandas as pd
from sklearn import metrics

from .mfl import  ModelFacts

class ModelFactsWidget(ipyw.VBox):
    '''Generate a form to create a Model Facts label
    The widget only supports data from binary classification and regression models
    Data must be in csv format
    Provide input values from form to calculate statistics for the label
    '''

    def __init__(self):
        '''Define initial widgets
        Generates column selection widget only after test data is provided
        '''
        style = {'description_width': 'initial'}
        items_layout = Layout(flex='1 1 auto',
                      width='auto')     # override the default width of the button to 'auto' to let the button grow
        # input application of the model
        self.application = ipyw.Textarea(
            value='',
            placeholder='Predicting X. The target class is Y',
            description='What is the application of this model?',
            disabled=False,
            style = style,
            layout = items_layout
        )
        self.warning = ipyw.Textarea(
            value = '',
            placeholder = 'Any known out of scope use cases, high risk biases, or blind spots (eg, from untested scenarios or missing data).',
            description = 'What warnings should users be aware of?',
            disabled = False,
            style = style,
            layout = items_layout
        )
        self.source = ipyw.Textarea(
            value = '',
            placeholder = 'Data from A. Model trained by B.',
            description = 'Cite data and model source',
            disabled = False,
            style = style,
            layout = items_layout
        )
        # input model type 
        self.model_type = ipyw.Dropdown(
            options = [('classification', True), ('regression', False)],
            description ='What type of predictive model is this?',
            disabled=False,
            style = style,
            layout = items_layout
        )

        # input size/split (optional)
        self.data_size = ipyw.IntText(
            value=0,
            description='Number of samples in full dataset (e.g.train+test)',
            disabled=False,
            style = style,
            layout = items_layout
        )
        self.data_split = ipyw.FloatText(
            value=0,
            min = 0,
            max = 100,
            description='Percent of the data used for testing (0-100%)',
            disabled=False,
            style = style,
            layout = items_layout
        )

        # input dates
        self.train_date = ipyw.DatePicker(
            description='When was this model trained?',
            disabled=False,
            style = style,
            layout = items_layout,
            value = dt.datetime.now()
        )
        self.data_date = ipyw.DatePicker(
            description='When was the test data from?',
            disabled=False,
            style = style,
            layout = items_layout, 
            value = dt.datetime.now()
        )
    
        # input score names
        self.st_score = ipyw.Text(
            value = 'f1_score',
            placeholder = 'f1_score',
            description = 'Standard Score (Sklearn.metrics function name)',
            disabled = False,
            style = style,
            layout = items_layout
        )
        self.t_score = ipyw.Text(
            value = 'accuracy_score',
            placeholder = 'accuracy_score',
            description = 'Training Score Used (Sklearn.metrics function name)',
            disabled = False,
            style = style,
            layout = items_layout
        )

        # select if any of the scores are probability based
        self.score_proba = ipyw.RadioButtons(
            options = ['None', 'Standard Score', 'Training Score', 'Both'],
            description = 'Are any of the scores probability based?',
            disabled=False,
            style = style,
            layout = items_layout
        )

        # upload data
        self.test_data = ipyw.FileUpload(accept = '.csv', description = "Upload Test data")

        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid',
                            width='100%')

        self.widget_holder = ipyw.VBox(layout= box_layout)
        children = [
            self.application,
            self.warning,
            self.source,
            self.model_type,
            self.train_date,
            self.data_date,
            self.st_score,
            self.t_score,
            self.score_proba,
            self.data_size,
            self.data_split,
            self.test_data,
            self.widget_holder,
        ]
        self.test_data.observe(self._add_demo_cols_widgets, names=['value'])
        
        super().__init__(children=children)

    def _add_demo_cols_widgets(self, widg):
        '''Create demographic column selection widget
        '''
        style = {'description_width': 'initial'}
        items_layout = Layout(flex='1 1 auto',
                      width='auto')  
        test_data =  widg['new']
        print(test_data[0])
        self.test_df  = pd.read_csv(io.BytesIO(test_data[0].content))
        cols = list(self.test_df.columns)
        # Select which column has the demographics (after reading in the data)
        all_demo = ipyw.SelectMultiple(
            options = cols,
            description='Select all columns with demographic data (hold shift or ctrl)',
            disabled=False,
            style = style,
            layout = items_layout
        )
        age_demo = ipyw.Select(
            options = [None] + cols,
            description='Select the column with age data (Choose None if there is no age demographic data)',
            disabled=False,
            style = style,
            layout = items_layout
        )
        # instructions       
        complete = ipyw.Label(
            value = 'Run next cell when the form is filled out',
            style = dict(
                text_color = "Blue",
                font_weight = "Bold"))
        new_widgets = [all_demo, age_demo, complete]
        self.widget_holder.children = tuple(new_widgets)
    
    def create_label(self):
        '''Create a Model Facts label from widget input
        Returns: 
            Model Facts Table: great_tables.GT 
        '''
        # admin data
        application = self.application.value
        warning = self.warning.value
        source = self.source.value
        model_type = self.model_type.value
        train_date = self.train_date.value
        test_data_date = self.data_date.value
        data_size = self.data_size.value
        data_split = f'{100-self.data_split.value}/{self.data_split.value}'
        # define score used
        st_score = self.st_score.value
        st_score_func = getattr(metrics, st_score)
        t_score = self.t_score.value
        score_func = getattr(metrics, t_score)
        st_proba = False
        t_proba = False
        if self.score_proba.value == 'Both':
            st_proba = True
            t_proba = True
        elif self.score_proba.value == "Standard Score":
            st_proba = True
        elif self.score_proba.value =="Training Score":
            t_proba = True
        # get demographic columns
        demo_cols = self.widget_holder.children[0].value
        age_col = self.widget_holder.children[1].value
        demo_cols = [i for i in demo_cols if i!=age_col]
        model_facts = ModelFacts(self.test_df, 'true', 'pred', 'baseline',
                                 st_score_func, score_func, classification = model_type,
                                 pred_proba ="pred_proba", baseline_proba = "baseline_proba", 
                                 st_proba = st_proba, t_proba = t_proba)
        mf_titanic = model_facts(demo_cols, age_col = age_col,
            train_date = train_date, test_data_date = test_data_date,
            data_size = data_size, data_split = data_split)
        table = model_facts.make_label(mf_titanic, 
                                       application = application, 
                                       warning = warning, 
                                       source = source, show = True)
        return table
