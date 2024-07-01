# MetaFOX

Advanced automated machine learning (AutoML) component, which will significantly simplify the initial model creation within NEMO META-OS by automating the process of model selection, feature engineering, and hyperparameter tuning. MetaFOX uses the power of automation in machine learning to streamline model development, enhance quality of the models, and democratize AI accessibility. It significantly simplifies the initial model creation for **federated learning (FL)** and **transfer learning (TL)** by automating the process of **model selection**, **feature engineering**, and **hyperparameter 
tuning**.

* **Model Selection**: MetaFOX evaluates numerous machine learning models to find the best starting architecture for the specific problem. It can efficiently sift through many combinations of model types (e.g., linear models, tree-based models, neural networks) to identify a promising starting point for federated learning, or in the case of TL, the most appropriate pre-trained model. It can assess which pre-trained models perform best on tasks like the target task and select the most suitable one.
* **Feature Engineering**: MetaFOX automatically detects the best transformations and interactions of features that could benefit the model. FL involves disparate data sources, and AutoML can help ensure that the features used in the initial model are robust and generalizable across different datasets. Although transfer learning often relies on features learned from the source task, AutoML can help in identifying and constructing additional features from the target dataset that can be beneficial when added to the model.
* **Hyperparameter Optimization**: AutoML tools optimize hyperparameters much more efficiently than manual experimentation. In the case of FL, it can help ensure that the initial model is as performant as possible before it is sent out to nodes for local training. In the case of TL, AutoML will automatically tune hyperparameters for the transfer learning process, which can be crucial since the optimal settings for the source task may not be ideal for the target task.
* **Architecture Adjustments**: In TL, MetaFOX can determine the best architecture adjustments needed when adapting the pre-trained model to the new task, such as adding or removing layers, or adjusting the size of layers to suit the new data and task.

## Getting Started

To start off, follow these steps:

1. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```

2. Start the Celery worker by running the following command from the **src** directory:
    ```
    celery -A metafox.metafox_celery worker --loglevel=info
    ```

3. Start the FastAPI endpoint by running the following command from the **src** directory:
    ```
    uvicorn metafox.metafox_api:app --reload
    ```

Optional: Start Flower for monitoring Celery workers by running the following command from the **src** directory:
    ```
    celery -A metafox.metafox_celery flower --port=5555
    ```

Once the app and the necessary components are running, you can access the FastAPI endpoint at `http://localhost:8000` and monitor the Celery workers using Flower at `http://localhost:5555`.

Make sure to configure any necessary environment variables or settings before starting the app.