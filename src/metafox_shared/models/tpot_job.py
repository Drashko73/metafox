from pydantic import Field, field_validator
from typing import Union, Dict, Annotated, Optional
from metafox_shared.models.automl_job import AutoMLJob
from metafox_shared.constants.string_constants import *
from metafox_shared.constants.tpot_constants import TPOT
from metafox_shared.constants.default_value_constants import *

available_config_dicts = [None, 'TPOT light', 'TPOT MDR', 'TPOT sparse']

class TPOTAutoMLJob(AutoMLJob):
    generations: Annotated[Optional[int], Field(
        default=DEFAULT_GENERATIONS,
        description="Number of generations to run the optimization process"
    )]
    population_size: Annotated[Optional[int], Field(
        default=DEFAULT_POPULATION_SIZE,
        description="Size of the population"
    )]
    offspring_size: Annotated[Optional[int], Field(
        default=DEFAULT_OFFSPRING_SIZE,
        description="Size of the offspring"
    )]
    mutation_rate: Annotated[Optional[float], Field(
        default=DEFAULT_MUTATION_RATE,
        description="Mutation rate"
    )]
    crossover_rate: Annotated[Optional[float], Field(
        default=DEFAULT_CROSSOVER_RATE,
        description="Crossover rate"
    )]
    scoring: Annotated[Optional[str], Field(
        default=DEFAULT_SCORING,
        description="Scoring function"
    )]
    cv: Annotated[Optional[int], Field(
        default=DEFAULT_CV,
        description="Number of cross-validation folds"
    )]
    subsample: Annotated[Optional[float], Field(
        default=DEFAULT_SUBSAMPLE,
        description="Subsample ratio"
    )]
    max_time_mins: Annotated[Optional[int], Field(
        default=DEFAULT_MAX_TIME_MINS,
        description="Maximum time in minutes"
    )]
    max_eval_time_mins: Annotated[Optional[int], Field(
        default=DEFAULT_MAX_EVAL_TIME_MINS,
        description="Maximum evaluation time in minutes"
    )]
    random_state: Annotated[Optional[int], Field(
        default=DEFAULT_RANDOM_STATE,
        description="Random state"
    )]
    config_dict: Annotated[Optional[Union[Dict, str]], Field(
        default=DEFAULT_CONFIG_DICT,
        description="Configuration dictionary"
    )]
    template: Annotated[Optional[str], Field(
        default=DEFAULT_TEMPLATE,
        description="Template"
    )]
    early_stop: Annotated[Optional[int], Field(
        default=DEFAULT_EARLY_STOP,
        description="Early stopping criteria"
    )]
    
    def custom_model_dump(self) -> Dict:
        return {
            DATA_SOURCE: self.data_source,
            TARGET_VARIABLE: self.target_variable,
            PROBLEM_TYPE: self.problem_type,
            GENERATIONS: self.generations,
            POPULATION_SIZE: self.population_size,
            OFFSPRING_SIZE: self.offspring_size,
            MUTATION_RATE: self.mutation_rate,
            CROSSOVER_RATE: self.crossover_rate,
            SCORING: self.scoring,
            CV: self.cv,
            SUBSAMPLE: self.subsample,
            MAX_TIME_MINS: self.max_time_mins,
            MAX_EVAL_TIME_MINS: self.max_eval_time_mins,
            RANDOM_STATE: self.random_state,
            CONFIG_DICT: self.config_dict,
            TEMPLATE: self.template,
            EARLY_STOP: self.early_stop,
            AUTOML_LIBRARY: TPOT
        }
        
    def __str__(self) -> str:
        return str(self.custom_model_dump())
    
    # Field validators
    @field_validator('config_dict')
    def check_config_dict(cls, value):
        if value is None:
            return value
        
        if value not in available_config_dicts and isinstance(value, str):
            return value
        
        if value not in available_config_dicts:
            raise ValueError('Config dict must be one of the available config dicts')
        
        return value