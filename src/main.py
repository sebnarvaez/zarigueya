import os
from zari.model_generator import ModelGenerator
from zari.zarigueya_context import ZarigueyaContext

if __name__ == "__main__":
    #TODO: Debug loading models from ZarigueyaContext
    gen = ModelGenerator()
    args = gen.setup_cmd_parser()
    
    if args:
        ctx = gen.context_from_cmd(args)
        #ctx = load_default_context()

        if not os.path.exists(ctx.out_path):
            os.makedirs(ctx.out_path)
        
        gen.apply_templates(ctx)