import os
import re
import importlib.util
from zari import utils
from mako.lookup import TemplateLookup
from os.path import join as pjoin

class ZarigueyaContext:
    def __init__(self, models_path: str, project_config: ProjectConfig, included_models: list, excluded_models: list):
        self.update_models_path(models_path, included_models, excluded_models)

        # Current input and output relative paths
        self.current_tmplt_path = project_config.root
        self.current_outpath = project_config.out_root

        # The current model in a loop
        self.current_model = None
        # The current prop in a loop. A tuple where the first element is the
        # property list, and the second is the attribute in case each element
        # is expected to have them.
        self.current_prop = None
        
        # Load general toml config files
        self.gbl = utils.load_toml(models_path, 'gbl')
        self.conversions = utils.load_toml(project_config.profile_path)

        if project_config.use_case_funcs:
            self.lookup = TemplateLookup(
                project_config.root,
                imports=[
                    'from caseconverter import camelcase as camelc',
                    'from caseconverter import pascalcase as pascalc',
                    'from caseconverter import snakecase as snakec',
                    'from caseconverter import titlecase as titlec',
                    'from caseconverter import macrocase as macroc',
                ])
        else:
            self.lookup = TemplateLookup()
 
    def update_models_path(self, models_path: str, included_models: list, excluded_models: list):
        self._models_path = models_path
        self._update_included_models()
        self._update_models_list()

    def _update_included_models(self, included_models: list = None, excluded_models: list = None) -> list:
        if included_models is not None and excluded_models is not None:
            raise AttributeError(f"Can't set both included and excluded models.")
        # Include all models in the path by default
        if included_models is None:
            self.included_models = set()
            for model in os.listdir(self._models_path):
                model_path = pjoin(self._models_path, model)
                if os.path.isdir(model_path) and os.path.exists(pjoin(model_path, 'config.py')):
                    self.included_models.add(model)
        else:
            self.included_models = set(included_models)
        
        if excluded_models is not None:
            self.included_models -= set(excluded_models)
    
    def _update_models_list(self):
        self.models = []
        for model in self.included_models:
            model_path = pjoin(self._models_path, model)
            fpath = pjoin(model_path, 'config.py')
            
            spec = importlib.util.spec_from_file_location(model, fpath)
            if spec is None:
                raise ImportError(f" Error: Could not find a spec for model {model}")

            model_module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(model_module)
            except Exception as e:
                raise ImportError(f" Error executing module for model {model}: {e}")
            self.models.append(model_module.config)

def load_default_context() -> ZarigueyaContext:
    models_path = 'tests/example_models'
    tmplts_path = 'templates/go_templ_datastar'
    profile_path = 'profiles/go_datastar'
    out_path = pjoin(models_path, 'output')

    return ZarigueyaContext(models_path, tmplts_path, out_path, profile_path)