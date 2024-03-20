# BIKE SHARING DATASET: building a clean and structure Machine Learning project


## Overview
The main goal of this project is to build a clean and well structured machine learning project using (and learning) DevOps and MLOps best practices. An deep exploratory data analysis and a performant machine learning model are a secondary goal, highly neglected at this stage.

**The project is not perfect nor complete. Feedbacks are more than welcome! :)**

I split the all project in two parts having the following goals:
- To create an user interface using streamlit allowing analyst to easily explore the Bike sharing dataset

- To create the first building blocks (that I will call ML toolkit) allowing:
    1) Machine learning models and pipelines building and training
    2) Model evaluation
    3) Features engineering and model selection




## The Dataset

The dataset is a set of shared bicycle records. 
Here is a brief description of the data:
- **datetime** ->​ date and time of the statement
- **season​** -> 1 = winter, 2 = spring, 3 = summer, 4 = fall
- **holiday** ​–> indicates whether the day is a school holiday
- **workingday** ->​ indicates whether the day is worked (neither weekend nor vacation)
- **weather​** -> 1: clear to cloudy, 2: fog, 3: light rain or snow, 4: heavy showers or snows
- **temp** ​–> temperature in degrees Celsius
- **atemp** ​–> felt temperature in degrees Celsius
- **humidity​** –> humidity level
- **windspeed** ​–> wind speed
- **casual​** -> number of rentals from non-subscribers
- **registered** ​–> number of rentals from subscribed users
- **count** ​–> total number of bike rentals


## The key components

- **streamlit**: folder containing the file related to the streamlit application 
    - **plot.py**: define the class that will be used in the main file
    - **main.py**: define the class that will produce the app
- **src**: folder containing files to load and process data, to build, train and evaluate models
    - **data preprocessing.py**: file to preprocess data
    - **models.py**: file to build models and pipelines
    - **evaluate.py**: file to evaluate th model

## Remarks and next steps
It can be interesting to learn and explore what it can be done by using MLflow in order to optimize the pipeline, the iteration on differet models and preprocesing steps, the hyperparametes tuning and the model selection process
- **Streamlit app**
    - Define App **tests** to ensure it behaves as we want
    - Create a GitHub Action allowing to **automatically update the App**
    - Add data analysis **fonctionalities**
- **ML toolkit**
    - Define **unit tests**
    - The cleaning fonction can be developed to better ensure data quality.
    - Add to the feature_engineering class a method adding temporal feature to data: we did not introduce features allowing to account for temporal relationship. However, we can observe that the average number of users increases with time and this feature cannot be neglected
    - From the insights we get by performing a deeper exploratory data analyse there may some interesting methods to add to the feature_engineering class and the get_preprocessor pipeline can be optimized  
    - Add other models that can be worthly to test
    - Add an **hyperparameter tuning fonctionnality**
    - Add an automatically **model selection fonctionnality**
    - Add a **monitoring functionality**

