import os
import re
import utils
from mako.lookup import TemplateLookup
from os.path import join as pjoin

class ZarigueyaContext:
    def __init__(self, tmplts_path: str, models_path: str, out_path: str, profile_path: str, use_case_funcs: bool = True):
        self.tmplts_path = tmplts_path
        self.out_path = out_path
        # Current input and output relative paths
        self.current_inpath = tmplts_path
        self.current_outpath = out_path

        self.models = []
        self._models_path = models_path
        self._update_models_list()

        # The current model in a loop
        self.current_model = None
        # The current prop in a loop. A tuple where the first element is the
        # property list, and the second is the attribute in case each element
        # is expected to have them.
        self.current_prop = None
        
        # Load general toml config files
        self.gbl = utils.load_toml(models_path, 'gbl')
        self.conversions = utils.load_toml(profile_path, 'conversions')

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
        self._update_models_list()
    
    def _update_models_list(self):
        for file in os.listdir(self._models_path):
            if file.endswith('.toml') and file != 'gbl.toml':
                self.models.append(utils.load_toml(self._models_path, file))
    

def load_default_context() -> ZarigueyaContext:
    tmplts_path = 'templates/go_templ_datastar'
    models_path = 'tests/example_models'
    profile_path = 'profiles/go_datastar'
    out_path = pjoin(models_path, 'output')

    return ZarigueyaContext(tmplts_path, models_path, out_path, profile_path)