# MetaFOX

Advanced automated machine learning (AutoML) component, which will significantly simplify the initial model creation within NEMO META-OS by automating the process of model selection, feature engineering, and hyperparameter tuning. MetaFOX uses the power of automation in machine learning to streamline model development, enhance quality of the models, and democratize AI accessibility. It significantly simplifies the initial model creation for **federated learning (FL)** and **transfer learning (TL)** by automating the process of **model selection**, **feature engineering**, and **hyperparameter tuning**.

* **Model Selection**: MetaFOX evaluates numerous machine learning models to find the best starting architecture for the specific problem. It can efficiently sift through many combinations of model types (e.g., linear models, tree-based models, neural networks) to identify a promising starting point for federated learning, or in the case of TL, the most appropriate pre-trained model. It can assess which pre-trained models perform best on tasks like the target task and select the most suitable one.
* **Feature Engineering**: MetaFOX automatically detects the best transformations and interactions of features that could benefit the model. FL involves disparate data sources, and AutoML can help ensure that the features used in the initial model are robust and generalizable across different datasets. Although transfer learning often relies on features learned from the source task, AutoML can help in identifying and constructing additional features from the target dataset that can be beneficial when added to the model.
* **Hyperparameter Optimization**: AutoML tools optimize hyperparameters much more efficiently than manual experimentation. In the case of FL, it can help ensure that the initial model is as performant as possible before it is sent out to nodes for local training. In the case of TL, AutoML will automatically tune hyperparameters for the transfer learning process, which can be crucial since the optimal settings for the source task may not be ideal for the target task.
* **Architecture Adjustments**: In TL, MetaFOX can determine the best architecture adjustments needed when adapting the pre-trained model to the new task, such as adding or removing layers, or adjusting the size of layers to suit the new data and task.

## Table of Contents
- [Getting Started](#getting-started)
- [Installing Prerequisites](#installing-prerequisites)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)

## Installing Prerequisites <a name="installing-prerequisites"></a>

Before running MetaFOX, you need to install the following prerequisites:

1. Docker: MetaFOX relies on Docker to run RabbitMQ and Redis containers. You can install Docker by following the official installation guide for your operating system.

2. RabbitMQ: RabbitMQ is a message broker that MetaFOX uses for task queuing and communication between components. To install RabbitMQ using Docker, execute the following command:

    ```
    docker run -d --name rabbitmq -p 5672:5672 rabbitmq
    ```

    This command will pull the RabbitMQ Docker image and start a container named "rabbitmq" with port 5672 exposed.

3. Redis: Redis is an in-memory data store that MetaFOX uses for caching and storing intermediate results. To install Redis using Docker, execute the following command:

    ```
    docker run -d --name redis -p 6379:6379 redis
    ```

    This command will pull the Redis Docker image and start a container named "redis" with port 6379 exposed.

Once you have installed Docker, RabbitMQ, and Redis, you can start them by executing the respective Docker commands mentioned above. Make sure to wait for the containers to start before proceeding with the next steps.

[Back to Table of Contents](#table-of-contents)

## Getting Started <a name="getting-started"></a>

To start off, follow these steps:

1. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```

2. Start the Celery worker by running the following command from the **src** directory:
    ```
    celery -A metafox.worker.metafox_celery worker --loglevel=info
    ```

3. Start the FastAPI endpoint by running the following command from the **src** directory:
    ```
    python3 -m metafox.app.app
    ```

Optional: Start Flower for monitoring Celery workers by running the following command from the **src** directory:
```
celery -A metafox.worker.metafox_celery flower --port=5555
```

Once the app and the necessary components are running, you can access the FastAPI endpoint at `http://localhost:8000` and monitor the Celery workers using Flower at `http://localhost:5555`.

Make sure to configure any necessary environment variables or settings before starting the app.

[Back to Table of Contents](#table-of-contents)


## API Documentation <a name="api-documentation"></a>

After starting the FastAPI endpoint, you can access the API documentation by navigating to `http://localhost:8000/metafox/docs`. This endpoint provides a comprehensive overview of all the available API routes, request/response schemas, and example requests.

The API documentation is generated automatically based on the defined endpoints and their corresponding request/response models. It allows developers to easily explore and understand the functionality of the MetaFOX API without having to refer to the source code.

The documentation provides detailed information about each endpoint, including the HTTP methods supported, the expected request payloads, and the structure of the response data. It also includes interactive features such as the ability to make test requests directly from the documentation page.

To access the API documentation, simply open a web browser and enter the URL `http://localhost:8000/metafox/docs` after starting the FastAPI endpoint.

[Back to Table of Contents](#table-of-contents)

## Environment Variables <a name="environment-variables"></a>

MetaFOX uses environment variables for configuration. To set up the necessary environment variables, create a `.env` file in the root directory of the project. Here is an example of how the `.env` file should be structured:

```
API_NAME=MetaFOX
API_VERSION=1.0.0
API_HOST=localhost
API_PORT=8000
API_PREFIX=/metafox
API_DOCS_URL=/metafox/docs
API_REDOC_URL=/metafox/redoc


BROKER_URL=pyamqp://guest@localhost:5672//
RESULT_BACKEND=redis://localhost:6379/0
TASK_SERIALIZER=json
RESULT_SERIALIZER=json
WORKER_CONCURRENCY=12

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

Make sure to replace the values with your own configuration settings. The `.env` file should not be committed to version control to keep sensitive information secure.

[Back to Table of Contents](#table-of-contents)

