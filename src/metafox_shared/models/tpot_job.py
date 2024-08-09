from pydantic import Field
from typing import Union, Dict, Annotated, Optional
from metafox_shared.models.automl_job import AutoMLJob

class TPOTAutoMLJob(AutoMLJob):
    generations: Annotated[Optional[int], Field(
        default=100,
        description="Number of generations to run the optimization process"
    )]
    population_size: Annotated[Optional[int], Field(
        default=100,
        description="Size of the population"
    )]
    offspring_size: Annotated[Optional[int], Field(
        default=None,
        description="Size of the offspring"
    )]
    mutation_rate: Annotated[Optional[float], Field(
        default=0.9,
        description="Mutation rate"
    )]
    crossover_rate: Annotated[Optional[float], Field(
        default=0.1,
        description="Crossover rate"
    )]
    scoring: Annotated[Optional[str], Field(
        default=None,
        description="Scoring function"
    )]
    cv: Annotated[Optional[int], Field(
        default=5,
        description="Number of cross-validation folds"
    )]
    subsample: Annotated[Optional[float], Field(
        default=1.0,
        description="Subsample ratio"
    )]
    max_time_mins: Annotated[Optional[int], Field(
        default=None,
        description="Maximum time in minutes"
    )]
    max_eval_time_mins: Annotated[Optional[int], Field(
        default=5,
        description="Maximum evaluation time in minutes"
    )]
    random_state: Annotated[Optional[int], Field(
        default=None,
        description="Random state"
    )]
    config_dict: Annotated[Optional[Union[Dict, str]], Field(
        default=None,
        description="Configuration dictionary"
    )]
    template: Annotated[Optional[str], Field(
        default=None,
        description="Template"
    )]
    early_stop: Annotated[Optional[int], Field(
        default=None,
        description="Early stopping criteria"
    )]
    
    def custom_model_dump(self) -> Dict:
        return {
            "job_name": self.job_name,
            "data_source": self.data_source,
            "target_variable": self.target_variable,
            "problem_type": self.problem_type,
            "generations": self.generations,
            "population_size": self.population_size,
            "offspring_size": self.offspring_size,
            "mutation_rate": self.mutation_rate,
            "crossover_rate": self.crossover_rate,
            "scoring": self.scoring,
            "cv": self.cv,
            "subsample": self.subsample,
            "max_time_mins": self.max_time_mins,
            "max_eval_time_mins": self.max_eval_time_mins,
            "random_state": self.random_state,
            "config_dict": self.config_dict,
            "template": self.template,
            "early_stop": self.early_stop,
            "automl_library": "tpot"
        }
        
    def __str__(self) -> str:
        return str(self.custom_model_dump())