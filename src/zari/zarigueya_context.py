import os
import re
import utils
from mako.lookup import TemplateLookup
from os.path import join as pjoin

class ZarigueyaContext:
    def __init__(self, models_path: str, included_models: list, excluded_models: list, tmplts_path: str, out_path: str, profile_path: str, use_case_funcs: bool = True):
        self.tmplts_path = tmplts_path
        self.out_path = out_path
        # Current input and output relative paths
        self.current_tmplt_path = tmplts_path
        self.current_outpath = out_path

        # Include all models in the path by default
        if included_models is None:
            self.included_models = set()
            for model in os.listdir(models_path):
                model_path = pjoin(models_path, model)
                if os.path.isdir(model_path) and os.path.exists(pjoin(model_path, 'config.toml')):
                    self.included_models.add(model)
        else:
            self.included_models = set(included_models)
        
        if excluded_models is not None:
            self.included_models -= set(excluded_models)

        # Dict containing the models' configuration
        # each key is the config file name
        self.models = {}
        self._models_path = models_path
        self._update_models_dict()

        # The current model in a loop
        self.current_model = None
        # The current prop in a loop. A tuple where the first element is the
        # property list, and the second is the attribute in case each element
        # is expected to have them.
        self.current_prop = None
        
        # Load general toml config files
        self.gbl = utils.load_toml(models_path, 'gbl')
        self.conversions = utils.load_toml(profile_path)

        if use_case_funcs:
            self.lookup = TemplateLookup(
                tmplts_path,
                imports=[
                    'from caseconverter import camelcase as camelc',
                    'from caseconverter import pascalcase as pascalc',
                    'from caseconverter import snakecase as snakec',
                    'from caseconverter import titlecase as titlec',
                    'from caseconverter import macrocase as macroc',
                ])
        else:
            self.lookup = TemplateLookup()
 
    @property
    def models_path(self):
        return self._models_path
    
    @models_path.setter
    def models_path(self, value: str):
        self._models_path = value
        self._update_models_dict()
    
    def _update_models_dict(self):
        for model in self.included_models:
            model_path = pjoin(self.models_path, model)
            fname = pjoin(model_path, 'config.toml')
            if os.path.exists(fname):
                self.models[model] = utils.load_toml(fname)
            else:
                print(f"Can't find condig.toml for odel {model}.")

def load_default_context() -> ZarigueyaContext:
    models_path = 'tests/example_models'
    tmplts_path = 'templates/go_templ_datastar'
    profile_path = 'profiles/go_datastar'
    out_path = pjoin(models_path, 'output')

    return ZarigueyaContext(models_path, tmplts_path, out_path, profile_path)