# Model Facts
Create a Model Facts label to improve the transparency of your model when communicating with end users. 
This label provides a framework to interrogate models for biases. 
It provides information required for comparability in a simple and flexible format. 

Last Updated: 
18 March, 2025

## Framework
<img src="https://github.com/jhzsquared/model_facts/blob/main/model_facts.png" alt = "Model Facts" width = 200 />

## Installation
It can be installed from PyPI using: 

```pip install modelfacts```

Note: the template notebooks are only available in the source distribution.

You can also clone this repository and install required packages through:

```
git clone https://github.com/jhzsquared/model_facts.git
pip install -r requirements.txt
```

## Usage
Model Facts is designed to be flexible, whether you have pre-formatted data and results and just want to fill out a template, or want to generate your own statistics.

### Template
1. Download the `model_facts_template.ipynb` notebook.
1. Create a csv file with the test data, the aligned demographic variables, predictions, baseline, and truth values.
1. Run the first code cell
1. Fill out the form
1. Profit! :)

Note: the template currently only supports metrics from `scikit-learn.metrics`, binary classification, and regression models. For more complex modeling problems, please reference the other workflows.

### DIY
The `demo/model_facts_titanic.ipynb` notebook provides a simple example of how you can use Model Facts labels on your own dataset with more flexibility through the `modelfacts.ModelFacts` class.

### Extra DIY
Use the `modelfacts.ModelFactsLabel` class and pass in your own pre-calculated statistics.

```
model_facts_data = (admin_data, accuracy_data, demographic_data)
mf_label = mfw.ModelFactsLabel(model_facts_data)
table = mf_label(application, warning, source, show=True)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Make sure to update tests as appropriate.

Reach out if you are interested in joining the team for continued development of this project

## Limitations
The automated calculation code currently only supports binary classification and regressions. 
Users can use their own calculations and the `modelfacts.ModelFactsLabel` to generate a label from their own statistics.

## License
Model Facts is licensed under the MIT license.
## Citation
This project was developed as a follow-up to the following paper. Please cite the following if you are using Model Facts labels:


Jessica Zhu, Michel Cukier, Joseph Richardson, Nutrition facts, drug facts, and model facts: putting AI ethics into practice in gun violence research, Journal of the American Medical Informatics Association, Volume 31, Issue 10, October 2024, Pages 2414–2421, https://doi.org/10.1093/jamia/ocae102

or 

```
@article{10.1093/jamia/ocae102,
    author = {Zhu, Jessica and Cukier, Michel and Richardson, Joseph, Jr},
    title = {Nutrition facts, drug facts, and model facts: putting AI ethics into practice in gun violence research},
    journal = {Journal of the American Medical Informatics Association},
    volume = {31},
    number = {10},
    pages = {2414-2421},
    year = {2024},
    month = {05},
    issn = {1527-974X},
    doi = {10.1093/jamia/ocae102},
    url = {https://doi.org/10.1093/jamia/ocae102},
    eprint = {https://academic.oup.com/jamia/article-pdf/31/10/2414/59206288/ocae102.pdf},
}
```