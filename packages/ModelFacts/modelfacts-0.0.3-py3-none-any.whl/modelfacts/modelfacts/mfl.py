from great_tables import GT, loc, style, md
import pandas as pd
import numpy as np

class ModelFacts():
    '''Generate a Model Facts label from original data and predictions
    As published in: https://doi.org/10.1093/jamia/ocae102
    Given an input test dataframe and administrative details it will 
    split the data by demographic information to calculate relevant scores
    Users can then take these calculations to generate a formatted label

    Attributes:
        age_bins: the lower limit for grouping ages
        labels: the labels for the age bins
    '''
    age_bins = [0, 18, 25, 35, 50, 65, np.inf]
    labels = ['<18','18-24', '25-34', '35-49', '50-64', '64+']
    def __init__(self, df, true, pred, baseline, st_func, t_func, 
                 classification = True, pred_proba = None, baseline_proba = None,
                 st_proba = False, t_proba = False):
        '''Set key Model Facts details
        Parameters
        ----------
        df: pd.DataFrame
            The test dataset with true values, predictions and baseline
        true: str
            column name with true values
        pred: str
            column name with model predicted values
        baseline: str
            column name with baseline prediction values
        st_func: str
            name of the metric used for standard comparisons of this problem
            (only supports sklearn.metrics names)
        t_func: str
            name of the metric used to optimize the model
            (only supports sklearn.metrics names)
        classification: bool, optional
            True if it is a classification model. 
            False if a regression (continuous prediction) model
        pred_proba: str, optional
            Name of prediction probabilities 
            for calculating a score like AUC
        baseline_proba: str, optional
            Name of baseline prediction probabilities 
            for calculating a score like AUC
        st_proba: bool, optional
            If True, the score use the probability column
        t_proba: bool, optional
            If True, the score uses the probability column
        '''
        self.df = df
        self.true = true
        self.pred = pred
        self.baseline = baseline
        self.st_func = st_func
        self.t_func = t_func
        self.type = classification
        self.pred_proba = pred_proba
        self.baseline_proba = baseline_proba
        self.st_proba = st_proba
        self.t_proba = t_proba

    def __call__( self, demo_groups, age_col=None, 
             train_date = None, test_data_date = None,
             data_size = np.nan, data_split = "",
             st_kwargs = {}, t_kwargs = {}):
        '''Calculate Model Facts' demographic data and scores
        Parameters
        ----------
        demo_groups: list
            The list of demographic column names to consider (not including age)
        age_col: str, optional
            The name of the age column
        train_date: dt.datetime, optional
            When the model was trained
        test_data_date: dt.datetime, optional
            When the Test dataset is from
        data_size: float, optional
            Number of samples in train+test
        data_split: str, optional
            %Train/Test (e.g. 80/20)
        st_kwargs: dict, optional
            keyword arguments for the standard score 
        t_kwargs: dict, optional
            keyword arguments for training score
        
        Returns:
        -------
        model_facts_data: tuple of dataframes with processed statistics
            (administrative data, accuracy score data, demographic data)
        '''
        if self.type:
            model_type = "classification"
        else:
            model_type = "regression"
        admin = {
            'Model Type': model_type,
            'Model Train Date': train_date, 
            'Test Data Date': test_data_date, 
            'Dataset Size': data_size,
            '%Train/%Test': data_split }
        admin_data = pd.DataFrame.from_dict(admin, orient = 'index')
        acc_data = {}
        acc_data['Standard Score'] = self.calc_accuracy(self.st_func, 
                                                       self.st_proba,
                                                        **st_kwargs)
        acc_data['Training Score'] = self.calc_accuracy(self.t_func, 
                                                        self.t_proba,
                                                        **t_kwargs)
        acc_data = pd.DataFrame(acc_data).T
        demo_data = []
        demo_groups = [d for d in demo_groups if d!=age_col]
        for demo in demo_groups:
            demo_data.append(self.calc_demo(demo, age = False))
        if age_col:
            demo_data.append(self.calc_demo(age_col, age = True))
        demo_data = pd.concat(demo_data)
        model_facts_data = (admin_data, acc_data, demo_data)
        return model_facts_data
    
    def calc_accuracy(self, score_func, proba, **kwargs):
        '''Calculate Model Facts Accuracy section
        Obtain the core name, scores, and percent over baseline
        Parameters:
            score_func: function for metrics calculation, must take format f(true, pred, *kwargs)
            proba: bool, True if using a probability scoring function
            kwargs: dict, score specific keyword arguments
        Return:
            dict
        '''
        if proba:
            pred = self.pred_proba
            baseline = self.baseline_proba
        else:
            pred = self.pred
            baseline = self.baseline
        raw = score_func(self.df[self.true], self.df[pred], **kwargs)
        baseline = score_func(self.df[self.true], self.df[baseline], **kwargs)
        perc_over = 100*(raw-baseline)/baseline
        return {'Name': score_func.__name__, 'Raw Score': raw, '% Over Baseline': perc_over}

    def calc_demo(self, demo_col, age =  False, proba = False):
        '''Calculate Model Facts demographics section
        Per demographic group, obtain:
         - % samples in the test data
         - the 'accuracy' score within that group (per the predefined standard score metric)
         - the target class distribution in the test data
            - the % Target (if a classification model)
            or 
            - the mean, std (if a regression model)
                    
        Parameters:
            demo_col: str, name of 1 demographic column
            age: bool, True if demo_col is the age column
            proba: bool, True if using a probability based scoring function
        Returns:
            dataframe
        '''
        if proba:
            pred = self.pred_proba
        else:
            pred = self.pred
        if age:
            age_cut = pd.cut(self.df[demo_col], bins = self.age_bins, right = False, labels= self.labels)
            groups = self.df.groupby(age_cut, observed = True)
        else:
            groups = self.df.groupby(demo_col, observed = False)
        data = {}
        if self.type:
            data = groups[[demo_col, self.true, pred]].apply( lambda x: 
                    (x[demo_col].count()/len(self.df) * 100, # % in test data
                    self.st_func(x[self.true], x[pred]), # accuracy
                    x[self.true].sum()/x[self.true].count() * 100)) # % in target
            data = pd.DataFrame(data.tolist(), 
                    columns = ['% in Test Data', 'Standard Score', '% Target'], 
                    index = data.index)
        else:
            data = groups[[demo_col, self.true, pred]].apply( lambda x: 
                    (x[demo_col].count()/len(self.df)*100,  # % in test data
                    self.st_func(x[self.true], x[pred]), 
                    (x[self.true].mean(), x[self.true].std()))) # (target mean/std)
            data = pd.DataFrame(data.tolist(), 
                    columns = ['% in Test Data', 'Standard Score', 'Mean, Std'], 
                    index = data.index)
        data['grp'] = demo_col
        return data

    def make_label(self, model_facts_data, 
                   application = "", warning = "", source = "", show = True):
        '''Generate a formatted model facts label
        Parameters
        ----------
        model_facts_data: tuple of dataframes
            The data generated by calling ModelFacts 
            Can also pass in three self-created dataframes 
        application: str, optional 
            Brief text string describing the model's use case
            (e.g. Predicting X. The target class is Y)
        warning: str, optional
            Any known out of scope use cases, high risk biases, or blind spots 
            (e.g. from untested scenarios or missing data)
        source: str, optional
            Brief text string of where the data is from and who trained the model
            (e.g. Data from A. Model trained by B)
        show: bool, optional
            Whether to display the generated label
        Return:
            great_tables.GT table
        '''
        label = ModelFactsLabel(model_facts_data)
        return label(application = application, 
                     warning = warning, source = source, show = show)

class ModelFactsLabel():
    '''Format a Model Facts Label from data
    Use the great_tables package and preprocessed data to generate a label
    Displays necessary transparency information in a clean, organized fashion
    Example::

        model_facts_data = (admin_data, accuracy_data, demographic_data)
        mf_label = ModelFactsLabel(model_facts_data)
        table = mf_label(application, warning, source, show=True)
        
    '''
    def __init__(self, model_facts_data):
        '''Initiate data needed for Model Facts label
        Parameters
        ----------
        model_facts_data: tuple of dataframes
            The data generated by calling ModelFacts 
            Can also pass in three self-created dataframes as a tuple
            (Admin data, accuracy data, demographic data)
        '''
        self.admin = model_facts_data[0].copy()
        self.acc = model_facts_data[1].copy()
        self.demo = model_facts_data[2].copy()

    def __call__(self, application = "", warning = "", source = "", show = True):
        '''Create a formatted model facts label
        Parameters
        ----------
        application: str, optional 
            Brief text string describing the model's use case
            (e.g. Predicting X. The target class is Y)
        warning: str, optional
            Any known out of scope use cases, high risk biases, or blind spots 
            (e.g. from untested scenarios or missing data)
        source: str, optional
            Brief text string of where the data is from and who trained the model
            (e.g. Data from A. Model trained by B)
        show: bool, optional
            Whether to display the generated label
        Return:
            great_tables.GT table
        '''
        acc_data = self.acc.copy()
        acc_index = acc_data.index
        acc_data.loc[' '] = acc_data.columns
        acc_data['grp'] = 'Accuracy'
        acc_data.rename(columns = {'Name':0, 'Raw Score':1, '% Over Baseline':2}, inplace=True)
        acc_data = acc_data.reindex([' ']+list(acc_index))

        demo_data = self.demo.copy()
        demo_index = demo_data.index
        notna_index = demo_data[~demo_data['Standard Score'].isna()].index
        demo_data.loc['Demographics'] = demo_data.columns
        demo_data.rename(columns={'% in Test Data':0, 'Standard Score':1, '% Target':2, 'Mean, Std': 2}, inplace= True)
        demo_data = demo_data.reindex(['Demographics']+list(demo_index))

        data = pd.concat([self.admin, acc_data, demo_data])
        data.rename(columns = {col: str(col) for col in data.columns}, inplace= True)
        data.fillna('', inplace=True)
        data['index'] = data.index
        data.loc['Demographics', 'grp'] = ' '

        # clean up text data
        if application == "":
            application = "Undefined model application"
        if warning == "":
            warning = "Unknown model warnings"
        else:
            warning = f"Warnings: {warning}"
        if source == "":
            source = "Unknown data and model source"
        instructions = "How to use Model Facts: " \
        "The first section, &quot;Application&quot; through &quot;Test Data Date&quot;" \
        " is to check that this model is relevant and timely for your goals. " \
        "Use the accuracy &quot;Standard Score&quot; to compare it to other models. " \
        "Use the demographic breakdown to check for biases in protected attributes " \
        "(eg, if one race is underrepresented in the &quot;% Test Data&quot; " \
        "or &quot;% Target&quot; or has a large difference in accuracy " \
        "compared to the overall model&#39;s &quot;Standard Score&quot;)."
        table = (
            GT(data, rowname_col="index", groupname_col="grp")
            .tab_header(title="Model Facts", subtitle = f"Application: {application}")
            .tab_style(
                style=[
                    style.text(color="black", weight="bold"),
                    style.fill(color="lightgray")
                ],
                locations=loc.body(rows=[" ", 'Demographics'])
            )
            .tab_style(
                style=[
                    style.text(color="Black", weight="bold"),
                ],
                locations=loc.row_groups()
            )
            .tab_source_note(md(f'<span style="color:red">**{warning}**</span>'))
            .tab_source_note(source)
            .tab_source_note(md(f'<small>{instructions}</small>'))
            .cols_label({'0':'', '1': '', '2':''})
            .fmt_number(rows = list(acc_index), columns = [1,2], n_sigfig = 3)
            .fmt_number(rows = list(notna_index), columns = [1], n_sigfig = 3)
            .fmt_number(rows = list(demo_index), columns = [0, 2], n_sigfig = 3)
            .fmt_date(rows = ['Model Train Date', 'Test Data Date'], columns = 0, date_style = 'day_month_year')
        )
        if show:
            table.show()
        return table
