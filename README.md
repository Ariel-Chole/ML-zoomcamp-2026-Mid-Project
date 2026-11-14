# Life Expectancy Prediction

A machine-learning regression project that predicts a country's life
expectancy (in years) from country-level demographic, health, and
economic indicators. The project covers EDA, data preparation, 
model comparison, training, prediction, and Docker-based
packaging.

## 1. Problem Statement

Life expectancy is an important indicator of population health and
living conditions. It is related to factors such as healthcare,
education, economic conditions, and lifestyle.

This project uses historical country-level data to estimate life
expectancy and explore how health, demographic, and economic indicators
are associated with it.

-   **Prediction target:** `life_expectancy`
-   **Problem type:** Supervised regression
-   **Main evaluation metric:** Root Mean Squared Error (RMSE)

RMSE measures the difference between actual and predicted values. A
lower RMSE indicates more accurate predictions, while larger errors
receive greater weight.

This project is intended for educational and analytical use. Its
predictions should not be used as the only basis for public-health
policy or individual medical decisions.

## 2. Dataset

The project uses the **Life Expectancy (WHO)** dataset from Kaggle.

**Dataset source:** [Life Expectancy (WHO) --
Kaggle](https://www.kaggle.com/datasets/kumarajarshi/life-expectancy-who)

The local dataset file is named `Life Expectancy Data.csv`.

-   Initial dataset size: **2,938 rows and 22 columns**
-   Rows with a missing target value removed: **10**
-   Rows remaining for modeling: **2,928**
-   Target variable: `life_expectancy`

The input features include country, development status, year, adult
mortality, infant and under-five deaths, alcohol consumption, healthcare
expenditure, vaccination coverage, measles, BMI, HIV/AIDS, GDP,
population, thinness, income composition of resources, and schooling.

The dataset is already provided in the project file but you should inspect the original file for any updates and terms.

## 3. Exploratory Data Analysis and Data Preparation

The main exploration and modeling work is documented in `project.ipynb`.

The notebook includes:

1.  Loading the CSV dataset and inspecting its structure.
2.  Checking column types and missing values.
3.  Standardizing column names by stripping spaces, converting names to
    lowercase, and replacing spaces with underscores.
4.  Removing rows with missing `life_expectancy` target values.
5.  Comparing missing-value handling methods by using RMSE of each method.
6.  Encoding categorical variables into numerical features using
    `DictVectorizer`. To use 'DictVectorizer', our samples need to be in Dicts format.
7.  Examining feature correlations with the target.
8. Visualize the highest correlations features.

### Missing-value comparison

The notebook compares filling missing input values with zero and filling
them with the feature mean, using a baseline Linear Regression model.

  Missing-value method                  Validation RMSE
  ----------------------------------- -----------------
  Fill missing values with `0`                    6.364
  Fill missing values with the mean               6.391

Zero filling is selected because it gives the lowest validation RMSE
when compare.

### Feature correlation

Some of the stronger correlations with life expectancy reported in the
notebook are:

  Feature                             Correlation
  --------------------------------- -------------
  Income composition of resources          +0.582
  BMI                                      +0.578
  Schooling                                +0.556
  HIV/AIDS                                 -0.571
  Adult mortality                          -0.695

Correlation describes an association in this dataset. It does not prove
that a feature causes a change in life expectancy.

## 4. Modeling and Evaluation

Four regression models are compared using validation RMSE:

1.  Linear Regression
2.  Decision Tree Regressor
3.  Random Forest Regressor
4.  XGBoost Regressor

The Decision Tree, Random Forest, and XGBoost models are tuned using
selected hyperparameters. The model with the lowest validation RMSE is
selected.

### Validation results

  Model                             Validation RMSE
  ------------------------------- -----------------
  Linear Regression                          6.3643
  Tuned Decision Tree Regressor              2.5903
  Tuned Random Forest Regressor              2.0080
  Tuned XGBoost Regressor                **1.9870**

XGBoost is selected because it achieves the lowest validation RMSE among
the four models.

### Selected XGBoost parameters

-   `eta`: `0.1`
-   `max_depth`: `6`
-   `min_child_weight`: `1`
-   `objective`: `reg:squarederror`
-   Number of boosting rounds: `251`

### Cross-validation and test evaluation

Five-fold cross-validation on the training portion reports:

-   **Mean RMSE:** 1.844
-   **Standard deviation:** 0.114

The final evaluation on the held-out test dataset reports:

-   **Test RMSE:** 1.6482

These are the results already recorded in the `` project.ipynb `` notebook. Re-running
training may produce different values if the data, preprocessing, split,
random seeds, or package versions differ. The notebook results should be
distinguished from results independently reproduced by the deployment
training script.

## 5. Project Structure

The following structure reflects the files visible in the project
folder:

``` text
mid_project/
├── .venv/                          # Local Python virtual environment
├── .vscode/                        # VS Code settings
├── src/                            # Application source code
├── .python-version                 # Proper Python version 
├── Dockerfile                      # Dockerfile to build image and container
├── Life Expectancy Data.csv        # Dataset
├── life_expectancy_predict.py      # Prediction script
├── life_expectancy_train.py        # Model training script
├── life-expectancy-model.bin       # Saved model artifact
├── person.json                     # Sample Customer Data
├── project.ipynb                   # Main Project notebook
├── pyproject.toml                  # Project and dependency configuration
├── README.md                       # Project documentation
├── test.ipynb                      # Test Notebook
├── test.py                         # Test script
└── uv.lock                         # Locked dependency versions
```

The `.venv/` directory is a local environment and will generally not
be committed to Git. The `src/` directory contains application code used
by the project.

## 6. Installation and Local Execution

The project uses `uv` for Python dependency management through
`pyproject.toml` and `uv.lock`.

Make sure Python and `uv` are installed.

### Install dependencies

Run the following commands to create virtual environment and install required dependencies:

``` bash
uv sync --locked
```

The `--locked` option installs dependencies using the versions recorded
in `uv.lock` and checks that the lock file is consistent with the
project configuration.

### Train the model

**Notice:** You don't need to re-train the model.

The project includes `life_expectancy_train.py` for the
training workflow. Run the project training entry point:

``` bash
uv run python life_expectancy_train.py
```

The training workflow uses the project dataset and produces the saved
model artifact used for prediction. The model artifact `life-expectancy-model.bin` already exists in the project folder.

### Generate a prediction

After the model artifact is available, run:

``` bash
uv run python life_expectancy_predict.py
```

The prediction script loads the saved model and generates a prediction
using the input data configured by the project. `person.json` is
included as a JSON sample data for testing.

## 7. Web Service

The project uses Flask to provide a web service for life expectancy prediction. The application loads the trained XGBoost model and the fitted DictVectorizer from the saved model pipeline (life-expectancy-model.bin).

The service listens on port 9696 and provides the following prediction endpoint:

HTTP Method: POST

Endpoint: /life_expectancy

Purpose: Receives input data in JSON format and returns the predicted life expectancy.

### Making a Prediction

First, make sure the Flask application is running. To run the Flask application:
```bash
python3 life_expectancy_predict.py
gunicorn --bind=0.0.0.0:9696 life_expectancy_predict:app
```

Open another terminal and you can check the app health using the following commands:
```bash 
curl localhost:9696/health
or 
curl 0.0.0.0:9696/health
```

You can send a prediction request using the following command:

``` bash
curl -X POST http://localhost:9696/life_expectancy \
  -H "Content-Type: application/json" \
  -d @person.json
```

The person.json file contains the input features required by the model. The request should follow the JSON structure expected by the application's preprocessing pipeline.

### Example Response

{
  "Predicted Life_expectancy": 58.6354
}

Note: The prediction value above is just for your reference.

You can also use these `test.py` and `test.ipynb` files for other testing ways.

The application processes the received data using the fitted DictVectorizer, passes the transformed features to the XGBoost model, and returns the predicted life expectancy in years.

## 8. Dockerization

Docker is used to package the application and its required dependencies
so that it can run in a consistent environment. The project includes a
`Dockerfile`.

Build the image from the project root using the project's image name and
tag:

``` bash
docker build -t mid_project:2026_mid .
```

Run the container and publish port `9696`:

``` bash
docker run --rm -p 9696:9696 mid_project:2026_mid
```

The `--rm` option removes the container as soon as it stops. The port mapping
makes the service available through port `9696` on the host machine.

You can then send a prediction request to:

``` text
http://localhost:9696//life_expectancy
```
The project also includes `test.py` and `test.ipynb` for testing.
After building the container, open another terminal and run 
``` bash
python3 test.py
``` 
OR 
Just Run the `test.ipynb` as you like.

## 9. Cloud Deployment

I use Python Anywhere for Cloud Deployment. 

## 10. Learning in Public (14 public learning links)


## 11. Time & Effort

I spend more than 30 hours on this project. 

* About 3 hours searching the dataset
* About 5 hours EDA and data preparation
* About 15 hours Model Building and parameter tunling 
* About 3 hours Flask app building
* About 2 hours Docker packaging
* About 2 hours Cloud Deployment