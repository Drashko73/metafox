# MetaFOX Examples

This directory contains various examples showcasing the features of the MetaFOX component for automated machine learning (AutoML).

## TPOT AutoML API Example

This examples demonstrates the usage of the TPOT AutoML API.

### Creating an AutoML job

This example demonstrates the process of creating an AutoML job that is being stored inside of a Redis database in a form of **key:value** where key is an automatically generated id and value consists of parameters passed by the user regarding an AutoML job.

The request body is a JSON object that contains the following parameters:
* (optional) **job_name** - name of the job
* (required) **data_source** - URL of the dataset
* (required) **target_variable** - target variable
* (required) **problem_type** - type of the problem (classification or regression)
* (optional) **generations** - number of generations that the genetic algorithm will run
* (optional) **population_size** - size of the population
* (optional) **offspring_size** - size of the offspring
* (optional) **mutation_rate** - rate of mutation
* (optional) **crossover_rate** - rate of crossover
* (optional) **scoring** - scoring metric to be used for optimization
  * **For regression:** neg_mean_squared_log_error, neg_median_absolute_error, neg_mean_absolute_error, neg_mean_squared_error, r2
  * **For classification:** accuracy, balanced_accuracy, average_precision, f1, f1_macro, f1_micro, f1_samples, f1_weighted, neg_log_loss, precision, precision_macro, precision_micro, precision_samples, precision_weighted, recall, recall_macro, recall_micro, recall_samples, recall_weighted, jaccard, jaccard_macro, jaccard_micro, jaccard_samples, jaccard_weighted, roc_auc, roc_auc_ovr, roc_auc_ovo, roc_auc_ovr_weighted, roc_auc_ovo_weighted
* (optional) **cv** - number of cross-validation folds
* (optional) **subsample** - fraction of samples to be used for training
* (optional) **max_time_mins** - maximum time in minutes that the genetic algorithm will run
* (optional) **max_eval_time_mins** - maximum time in minutes that the genetic algorithm will run for a single evaluation
* (optional) **random_state** - seed for random number generator
* (optional) **config_dict** - dictionary containing configuration parameters for the genetic algorithm
  * Built-in options: TPOT light, TPOT MDR, TPOT sparse
  * Custom configuration: dictionary containing parameters for the genetic algorithm
  * None: default configuration
* (optional) **template** - template for the pipeline (**needs work**)
* (optional) **early_stop** - early stopping criteria - how many generations without improvement before stopping the genetic algorithm

The default values for the parameters are as follows:
| Parameter | Default Value |
| --- | --- |
| generations | 100 |
| population_size | 100 |
| offspring_size | 100 |
| mutation_rate | 0.9 |
| crossover_rate | 0.1 |
| scoring | None |
| cv | 5 |
| subsample | 1.0 |
| max_time_mins | None |
| max_eval_time_mins | 5 |
| random_state | None |
| config_dict | None |
| template | None |
| early_stop | None |

Request body example 1:
```bash
{
    "job_name": "Boston Housing Regression 1",
    "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
    "target_variable": "medv",
    "problem_type": "regression",
    "generations": 10,
    "population_size": 10,
    "offspring_size": 10,
    "mutation_rate": 0.9,
    "crossover_rate": 0.1,
    "scoring": "neg_mean_squared_error",
    "cv": 5,
    "subsample": 1.0,
    "max_time_mins": 5,
    "max_eval_time_mins": 5,
    "random_state": 42,
    "config_dict": "TPOT light",
    "template": null,
    "early_stop": 5
}
```
In this example, the user is creating an AutoML job for the Boston Housing dataset with the target variable **medv**. The user is running the genetic algorithm for 10 generations with a population size of 10 and offspring size of 10. The mutation rate is set to 0.9 and the crossover rate is set to 0.1. The scoring metric used for optimization is the negative mean squared error. The user is using 5-fold cross-validation and the entire dataset for training. The genetic algorithm will run for a maximum of 5 minutes and each evaluation will run for a maximum of 5 minutes. The seed for the random number generator is set to 42. **The user is using the TPOT light configuration for the genetic algorithm**. The user has set the early stopping criteria to 5 generations without improvement.

Request body example 2:
```bash
{
    "job_name": "Boston Housing Regression 2",
    "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
    "target_variable": "medv",
    "problem_type": "regression",
    "generations": 100,
    "population_size": 100,
    "offspring_size": 100,
    "mutation_rate": 0.9,
    "crossover_rate": 0.1,
    "scoring": "neg_mean_squared_error",
    "cv": 5,
    "subsample": 1.0,
    "max_time_mins": 5,
    "max_eval_time_mins": 5,
    "random_state": 42,
    "config_dict": null,
    "template": null,
    "early_stop": 5
}
```
In this example the user is creating an AutoML job for the Boston Housing dataset with the target variable **medv**. The user is running the genetic algorithm for 100 generations with a population size of 100 and offspring size of 100. The mutation rate is set to 0.9 and the crossover rate is set to 0.1. The scoring metric used for optimization is the negative mean squared error. The user is using 5-fold cross-validation and the entire dataset for training. The genetic algorithm will run for a maximum of 5 minutes and each evaluation will run for a maximum of 5 minutes. The seed for the random number generator is set to 42. **The user is using the default configuration for the genetic algorithm**. The user has set the early stopping criteria to 5 generations without improvement.

Request body example 3:
```bash
{
    "job_name": "Boston Housing Regression 3",
    "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
    "target_variable": "medv",
    "problem_type": "regression",
    "generations": 100,
    "population_size": 100,
    "offspring_size": 100,
    "mutation_rate": 0.9,
    "crossover_rate": 0.1,
    "scoring": "neg_mean_squared_error",
    "cv": 5,
    "subsample": 1.0,
    "max_time_mins": 5,
    "max_eval_time_mins": 5,
    "random_state": 42,
    "config_dict": "{'sklearn.linear_model.ElasticNetCV':{'l1_ratio': np.arange(0.0, 1.01, 0.05), 'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]}}",
    "template": null,
    "early_stop": 5
}
```
In this example the user is creating an AutoML job for the Boston Housing dataset with the target variable **medv**. The user is running the genetic algorithm for 100 generations with a population size of 100 and offspring size of 100. The mutation rate is set to 0.9 and the crossover rate is set to 0.1. The scoring metric used for optimization is the negative mean squared error. The user is using 5-fold cross-validation and the entire dataset for training. The genetic algorithm will run for a maximum of 5 minutes and each evaluation will run for a maximum of 5 minutes. The seed for the random number generator is set to 42. **The user is using a custom configuration for the genetic algorithm**. The user has set the early stopping criteria to 5 generations without improvement.

Request example body 4:
```bash
{
    "job_name": "Boston Housing Regression 4",
    "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
    "target_variable": "medv",
    "problem_type": "regression",
    "generations": 100,
    "population_size": 100,
    "offspring_size": 100,
    "mutation_rate": 0.9,
    "crossover_rate": 0.1,
    "scoring": "neg_mean_squared_error",
    "cv": 5,
    "subsample": 1.0,
    "max_time_mins": 5,
    "max_eval_time_mins": 5,
    "random_state": 42,
    "config_dict": null,
    "template": "Regressor",
    "early_stop": 5
}
```
In this example the user is creating an AutoML job for the Boston Housing dataset with the target variable **medv**. The user is running the genetic algorithm for 100 generations with a population size of 100 and offspring size of 100. The mutation rate is set to 0.9 and the crossover rate is set to 0.1. The scoring metric used for optimization is the negative mean squared error. The user is using 5-fold cross-validation and the entire dataset for training. The genetic algorithm will run for a maximum of 5 minutes and each evaluation will run for a maximum of 5 minutes. The seed for the random number generator is set to 42. The user is using the default configuration for the genetic algorithm. The user has set the early stopping criteria to 5 generations without improvement. **The user is using a template for the pipeline restricting TPOT to use only regressors**.

The response body is a JSON object that contains the following parameters:
* **message** - message indicating the status of the job
* **automl_job_id** - id of the job

Example response:
```bash
{
  "message": "AutoML job created.",
  "automl_job_id": "8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310"
}
```

### Starting an AutoML job

Description: After successfully storing the job details, based on the generated id, user can start submitted job.

Request body:
```bash
# This request body is likely going to be different, please use the id returned as a response of a previous action.
8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310
```
As a request body, user should provide the id of the job that was created in the previous step. In this case, the id is **8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310**.

The response should contain the message indicating the status of the job.
```bash
AutoML job started.
```


### Checking job status

Description: Based on a provided automl job id, user can check status of a job.

Request body:
```bash
# This request body is likely going to be different, please use the automl job id returned as a response of a method that created the job.
8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310
```

As a request body, user should provide the id of the job that was created in the previous step and, optionally, the number of lines to be displayed in the response. In this case, the id is **8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310**.

The response should contain the message indicating the status of the job and the number of lines requested.
```bash
{
  "status": "SUCCESS",
  "logs": "Optimization Progress:  80%|████████  | 320/400 [04:39<01:38,  1.23s/pipeline]\nOptimization Progress:  82%|████████▏ | 328/400 [04:48<01:25,  1.18s/pipeline]\nOptimization Progress:  84%|████████▍ | 336/400 [05:03<01:32,  1.44s/pipeline]\n                                                                              \n\nOptimization Progress:  86%|████████▌ | 343/400 [05:03<01:22,  1.44s/pipeline]\n                                                                              \n5.25 minutes have elapsed. TPOT will close down.\nTPOT closed during evaluation in one generation.\nWARNING: TPOT may not provide a good pipeline if TPOT is stopped/interrupted in a early generation.\n\nOptimization Progress:  86%|████████▌ | 343/400 [05:03<01:22,  1.44s/pipeline]\n                                                                              \n\nOptimization Progress:  86%|████████▌ | 343/400 [05:03<01:22,  1.44s/pipeline]\n                                                                              \nTPOT closed prematurely. Will use the current best pipeline.\n\nOptimization Progress:  86%|████████▌ | 343/400 [05:03<01:22,  1.44s/pipeline]\n                                                                              "
}
```

### Stopping an AutoML job

Upon starting an AutoML job, user can stop the job by providing the automl job id. The job will be stopped and the user will receive a message indicating the the job has been stopped.

### Retirieving job details

Upon creation of an AutoML job, user can retrieve the details of the job by providing the automl job id. The details of the job will be returned to the user in a form of a JSON object.

```bash
{
  "automl_job_id": "60b00cea-e2cd-42cc-9551-e08763d90cd5_20240902002542",
  "details": {
    "job_name": "Boston Housing Regression 3",
    "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
    "target_variable": "medv",
    "problem_type": "regression",
    "generations": 100,
    "population_size": 100,
    "offspring_size": 100,
    "mutation_rate": 0.9,
    "crossover_rate": 0.1,
    "scoring": "neg_mean_squared_error",
    "cv": 5,
    "subsample": 1,
    "max_time_mins": 5,
    "max_eval_time_mins": 5,
    "random_state": 42,
    "config_dict": "{'sklearn.linear_model.ElasticNetCV':{'l1_ratio': np.arange(0.0, 1.01, 0.05), 'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]}}",
    "template": null,
    "early_stop": 5,
    "automl_library": "tpot"
  }
}
```

### Storing the best pipeline using BentoML

Upon completion of the AutoML job, user can store the best pipeline using BentoML by providing the automl job id. The best pipeline will be stored in a form of a BentoML file that can be used for deployment.
After the best pipeline is stored, the user will receive a message indicating the status of the job.

Response body:
```bash
Model saved.
```

### Retrieving the best pipeline using BentoML

After storing the best pipeline using BentoML, user can retrieve the best pipeline by providing the automl job id. The best pipeline will be retrieved and returned to the user in a form of a BentoML file.

Response headers:
```bash
 content-disposition: attachment; filename=8059d964-4a7e-4e5f-8921-a954dac3ec8b_20240902003310.bentomodel 
 content-length: 322912 
 content-type: application/octet-stream 
 date: Mon,02 Sep 2024 00:44:05 GMT 
 server: uvicorn 
```

Downloaded file can then be used for making predictions.

### Making predictions using the best pipeline

```python
import bentoml
import warnings
import pandas as pd

from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# Ignore warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('https://raw.githubusercontent.com/Drashko73/datasets/main/boston_housing/housing.csv')
features, target = data.drop('medv', axis=1), data['medv']

try:
    model = bentoml.models.import_model(
        path='path/to/downloaded/file/'   # Path to the downloaded file
    )
    
    runner = model.to_runner()
    runner.init_local()

    predictions = runner.predict.run(features)
    
except Exception as e:
    print(f'Error: {e}')
    # Exception could occur if the model has already been loaded
    # In that case, the model is stored on path /home/user/bentoml/models
    # In this case, refer to the official BentoML documentation for loading the model
```