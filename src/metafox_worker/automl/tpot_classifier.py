from tpot import TPOTClassifier

class TPOTClassifierWrapper:
    def __init__(self, generations=100, population_size=100,
                offspring_size=None, mutation_rate=0.9,
                crossover_rate=0.1,
                scoring='accuracy', cv=5,
                subsample=1.0, n_jobs=1,
                max_time_mins=None, max_eval_time_mins=5,
                random_state=None, config_dict=None,
                template=None,
                warm_start=False,
                memory=None,
                use_dask=False,
                periodic_checkpoint_folder=None,
                early_stop=None,
                verbosity=0,
                disable_update_check=False,
                log_file=None
        ):
        self.model = TPOTClassifier(
            generations=generations,
            population_size=population_size,
            offspring_size=offspring_size,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            scoring=scoring,
            cv=cv,
            subsample=subsample,
            n_jobs=n_jobs,
            max_time_mins=max_time_mins,
            max_eval_time_mins=max_eval_time_mins,
            random_state=random_state,
            config_dict=config_dict,
            template=template,
            warm_start=warm_start,
            memory=memory,
            use_dask=use_dask,
            periodic_checkpoint_folder=periodic_checkpoint_folder,
            early_stop=early_stop,
            verbosity=verbosity,
            disable_update_check=disable_update_check,
            log_file=log_file
        )
        
    def fit(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def get_model(self):
        return self.model
    
    def export_model(self, filename):
        self.model.export(filename)
        
    def get_pipeline(self):
        return self.model.fitted_pipeline_
    
    def get_model_params(self) -> dict:
        return self.model.clean_pipeline_string(self.model.fitted_pipeline_)