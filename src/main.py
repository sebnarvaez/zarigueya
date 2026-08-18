import sys
sys.path.append('/home/sebasnr/Documents/projects/zarigueya/src/')
import os
from zari.model_generator import ModelGenerator
from zari.zarigueya_context import ZarigueyaContext

if __name__ == "__main__":
    #TODO: Debug loading models from ZarigueyaContext
    gen = ModelGenerator._from_toml_file('../projects/go_datastar_scaffold/proj_conf.toml')
    args = gen.setup_cmd_parser()
    
    if args:
        ctx = gen.context_from_cmd(args)
        #ctx = load_default_context()
        
        gen.apply_templates(ctx)