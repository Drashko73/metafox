import pandas as pd
from tpot import TPOTRegressor

class TRegressor:
    """
        A wrapper for the TPOTRegressor class from the TPOT library.
    """
        
    # generations = 100                     -> 100 generations
    # population_size = 100                 -> 100 individuals in the population
    # offspring_size = None                 -> Use the same number of individuals as the population
    # mutation_rate = 0.9                   -> 90% of the population will be mutated
    # crossover_rate = 0.1                  -> Randomly select 10% of the population to mate
    # scoring = 'neg_mean_squared_error'    -> Use the negative mean squared error as the scoring metric
    # cv = 5                                -> 5-fold cross validation
    # subsample = 1.0                       -> Use all of the training data
    # n_jobs = 1                            -> Use one core for training
    # max_time_mins = None                  -> No time limit
    # max_eval_time_mins = 5                -> Spend 5 minutes evaluating a single pipeline
    # random_state = None                   -> Use a random seed
    # config_dict = None                    -> Use the default configuration
    # template = None                       -> Use a built-in template
    # warm_start = False                    -> Don't use warm-start
    # memory = None                         -> Don't use a cache
    # use_dask = False                      -> Don't use Dask
    # periodic_checkpoint_folder = None     -> Don't save checkpoints
    # early_stop = None                     -> Don't use early stopping
    # verbosity = 0                         -> Don't print progress
    # disable_update_check = False          -> Check for updates
    
    def __init__(self, config:dict = None) -> None:
        if config is None:
            config = {
                'generations': 100,
                'population_size': 100,
                'offspring_size': None,
                'mutation_rate': 0.9,
                'crossover_rate': 0.1,
                'scoring': 'neg_mean_squared_error',
                'cv': 5,
                'subsample': 1.0,
                'n_jobs': 1,
                'max_time_mins': None,
                'max_eval_time_mins': 5,
                'random_state': None,
                'config_dict': None,
                'template': None,
                'warm_start': False,
                'memory': None,
                'use_dask': False,
                'periodic_checkpoint_folder': "../checkpoints/tpot_regressor_checkpoints",
                'early_stop': None,
                'verbosity': 0,
                'disable_update_check': False
            }
        else:
            if not self.validate_config(config):
                raise ValueError("Invalid configuration parameter.")
            
        # If the periodic_checkpoint_folder is not None, set the path to the checkpoints folder
        if config.get('periodic_checkpoint_folder') is not None:
            config['periodic_checkpoint_folder'] = "../checkpoints/tpot_regressor_checkpoints"
        
        self.config = config                    # Store the configuration dictionary
        print(f"Configuration: {self.config}")
        
    def validate_config(self, config: dict) -> bool:
        """Validate the configuration dictionary.

        Args:
            config (dict): A dictionary containing the configuration parameters.

        Returns:
            bool: True if all keys in the config dictionary are valid, False otherwise.
        """
        valid_keys = {
            'generations',
            'population_size',
            'offspring_size',
            'mutation_rate',
            'crossover_rate',
            'scoring',
            'cv',
            'subsample',
            'n_jobs',
            'max_time_mins',
            'max_eval_time_mins',
            'random_state',
            'config_dict',
            'template',
            'warm_start',
            'memory',
            'use_dask',
            'periodic_checkpoint_folder',
            'early_stop',
            'verbosity',
            'disable_update_check'
        }
        return set(config.keys()).issubset(valid_keys)
    
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Fit the TPOT regressor to the training data.

        Args:
            X_train (pd.DataFrame): The training data.
            y_train (pd.Series): The target values.
        """
        self.tpot = TPOTRegressor(
            generations=self.config['generations'],
            population_size=self.config['population_size'],
            offspring_size=self.config['offspring_size'],
            mutation_rate=self.config['mutation_rate'],
            crossover_rate=self.config['crossover_rate'],
            scoring=self.config['scoring'],
            cv=self.config['cv'],
            subsample=self.config['subsample'],
            n_jobs=self.config['n_jobs'],
            max_time_mins=self.config['max_time_mins'],
            max_eval_time_mins=self.config['max_eval_time_mins'],
            random_state=self.config['random_state'],
            config_dict=self.config['config_dict'],
            template=self.config['template'],
            warm_start=self.config['warm_start'],
            memory=self.config['memory'],
            use_dask=self.config['use_dask'],
            periodic_checkpoint_folder=self.config['periodic_checkpoint_folder'],
            early_stop=self.config['early_stop'],
            verbosity=self.config['verbosity'],
            disable_update_check=self.config['disable_update_check']
        )
        self.tpot.fit(X_train, y_train)
        
    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        """Generate predictions using the trained TPOT regressor.

        Args:
            X_test (pd.DataFrame): The test data.

        Returns:
            pd.Series: The predicted target values.
        """
        
        assert hasattr(self, 'tpot'), "The model has not been trained."
        return self.tpot.predict(X_test)
    
    def export(self, filename: str) -> None:
        """Export the trained pipeline as a Python script.

        Args:
            filename (str): The name of the Python file to create.
        """
        
        assert hasattr(self, 'tpot'), "The model has not been trained."
        self.tpot.export(filename)
        
    def get_pipeline(self) -> str:
        """Get the optimized pipeline as a string.

        Returns:
            str: The optimized pipeline as a string.
        """
        
        assert hasattr(self, 'tpot'), "The model has not been trained."
        return self.tpot.fitted_pipeline_