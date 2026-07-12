#!/bin/python3
import csv
import os
import tomllib
import re
import argparse
import shutil
from functools import partial
from zari import utils
from zari.zarigueya_context import ZarigueyaContext
from zari.zarigueya_context import load_default_context
from mako.template import Template
from mako import exceptions
from os.path import join as pjoin

class ModelGenerator():
    # Variable references com in the style ${var}
    regex_var_str = r"\${.+}"
    # Lists (of models or their properties) are referenced as []
    regex_model = re.compile(fr"\[(|{regex_var_str})\]")
    regex_props = re.compile(fr"\[\[(|{regex_var_str})\]\]")

    """
    Returns the name of the file or folder, replacing the corresponding
    variables on the template's name
    """
    def get_filename(self, rem: re.Match, t_fname: str, tmplt_params: dict) -> str:
        # For template files, strip out the .tmplt extension
        t_fname = t_fname.replace('.tmplt', '')
        # Clear the square brackets that sourround the model or property (if any)
        if rem:
            middle_str = rem.group()[1:-1]
            if middle_str == '':
                middle_str = tmplt_params['name']
            t_fname = t_fname[:rem.start()] + middle_str + t_fname[rem.end():]

        t = Template(t_fname)
        return t.render(**tmplt_params)

    """
    Setup the command line argumments and help.
    """
    def setup_cmd_parser(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(prog='Zarigueya', description='General-purpose scaffolding for your app.')

        parser.add_argument('models_path', action='store',
                            help="The path containing the models' details. " +
                                "There shall be one folder per model, containing a config.toml and " + 
                                "an optional data.toml. Additionally, there can be a " +
                                "gbl.toml file at the root with global configuration parameters.")

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-i', '--include', nargs='*',
                            help="Models to include. By default, all models in the models_path " +
                                "are included. Can't be used combined with --exclude")

        group.add_argument('-e', '--exclude', nargs='*',
                            help="Models to exclude. By default, all models in the models_path " +
                                "are included. Can't be used combined with --include")

        # Mutually exclusive group finished
        parser.add_argument('-p', '--profile', required=True,
                            help="Folder containing the conversions.toml file, in which the " +
                                "equivalent of datatypes for each used language is defined.")

        parser.add_argument('-t', '--templates_path', required=True,
                            help="Path of the model templates. Note that the provided template " +
                                "should support whatever other options you choose.")
                                
        parser.add_argument('-o', '--outpath', default='output/',
                            help="Path of the root folder for the generated files." +
                                "Defaults to output/.")

        parser.add_argument('-s', '--skip_templates', action='store_true',
                            help="Template files to be skipped.")
                        
        parser.add_argument('-g', '--gen_data', action='store_true',
                            help="Whether to generate dummy data. Uses the dummy tag of the " +
                                "field properties.")


        parser.add_argument('-v', '--verbose', action='store_true',
                            help="Print replaced strings in the template")

        parser.add_argument('--no-case-funcs', action='store_true',
                            help="Don't import the default helper functions in template files related to case conversion.")
        
        return parser.parse_args()

    """
    Create a Zarigueya Context from the command line arguments.
    """
    def context_from_cmd(self, args: argparse.Namespace) -> ZarigueyaContext:
        
        models_path = args.models_path

        if not os.path.exists(models_path) or not os.path.isdir(models_path):
            print("models_path does not exist or is not a valid folder.")
            exit()

        tmplts_path = args.templates_path
        included_models = args.include
        excluded_models = args.exclude
                     
        out_path = args.outpath
        if out_path is None:
            out_path = pjoin(input_path, 'output')

        profile_path = args.profile
        use_case_funcs = not args.no_case_funcs

        return ZarigueyaContext(models_path, included_models, excluded_models, tmplts_path, out_path, profile_path, use_case_funcs)

    def get_seed_data(self, models_path, model_name):
        seed_file_path = pjoin(models_path, model_name, 'data.csv')
        if os.path.exists(seed_file_path):
            with open(seed_file_path, newline='') as seeds_file:
                return list(csv.DictReader(seeds_file))
        else:
            return None

    """
    Find templates and process them.
    @param ctx: holds current state of the structure.
    """
    def apply_templates(self, ctx: ZarigueyaContext):
        # The template parameters is a dict containing the current model's
        # parameters, its related data (data --if any), the global parameters (gbl),
        # and the type conversions (conv).
        tmplt_params = {}
        # Flag to prevent processing the same file twice if it matches multiple regex
        file_ready = False
        
        for tmplt_name in os.listdir(ctx.current_tmplt_path):
            # tmplt_name is the name of the file/folder.
            # tmplt_path is its full path.
            tmplt_path = pjoin(ctx.current_tmplt_path, tmplt_name)
            # Non-template files are just copied
            if os.path.isfile(tmplt_path) and '.tmplt' not in tmplt_name:
                shutil.copy2(
                    tmplt_path,
                    ctx.current_outpath)
                continue
            
            # Process files/folders that apply to all properties
            rem = regex_props.search(tmplt_name)
            if rem:
                if ctx.current_model is None:
                    raise AttributeError(f"{tmplt_path}: double square-brackets notation ([[${{property}}]]) is for properties of a model, and thus is reserved for files/folders with a parent folder using single square-brackets notation ([${{model}}]).")
                
                if ctx.current_prop is not None:
                    raise NotImplementedError("Nested properties are not currently supported")

                # Property definition. Can be either dierctly a list (1 element),
                # or an attribute of a list property (2 elements)
                prop_def = rem.group().split('.')
                if len(prop_def) < 1 or len(prop_def) > 2:
                    raise AttributeError(f"{tmplt_path}: property definitions must contain one or two elements (separated by a period), found {len(prop_def)}: {prop_def}")
                
                prop_list = ctx.current_model[prop_def[0]]
                attr = prop_def[1] if len(prop_def == 2) else ''

                ctx.current_prop = (prop_list, attr)

                for prop in prop_list:
                    if attr != '':
                        prop = prop[attr]

                    outfile_name = tmplt_name[:rem.start()] + prop + tmplt_name[rem.end():]

                    create_file_or_folder(ctx, tmplt_path, outfile_name, tmplt_params)
                    
                ctx.current_prop = None
                file_ready = True

            # Process files/folders that apply to all models
            rem = regex_model.search(tmplt_name)
            if rem and not file_ready:
                if ctx.current_prop is not None:
                    raise AttributeError(f"{tmplt_path}: A parent folder has the properties' double-square brackets [[]] notation, which isn't allowed for models file/folders (single square-bracket []).")

                for model in ctx.models:
                    mdetails = ctx.models[model]
                    ctx.current_model = model
                    tmplt_params = {
                        **mdetails, 
                        'seed_data': get_seed_data(ctx.models_path, model),
                        'gbl': ctx.gbl,
                        'conv': ctx.conversions
                    }
                    outfile_name = get_filename(rem, tmplt_name, tmplt_params)
                    
                    create_file_or_folder(ctx, tmplt_name, outfile_name, tmplt_params)
                    file_ready = True
            
            if not file_ready:
                tmplt_params = {
                    'models': ctx.models,
                    'seed_data': partial(get_seed_data, ctx.models_path),
                    'gbl': ctx.gbl,
                    'conv': ctx.conversions
                }
                outfile_name = get_filename(rem, tmplt_name, tmplt_params)
                
                create_file_or_folder(ctx, tmplt_name, outfile_name, tmplt_params)
                
    def create_file_or_folder(self, ctx: ZarigueyaContext, tmplt_path: str, outfile_name: str, tmplt_params: dict):
        outfile_path = pjoin(ctx.current_outpath, outfile_name)
        tmplt_full_path = pjoin(ctx.tmplts_path, tmplt_path)

        if os.path.isfile(tmplt_full_path):
            with open(outfile_path, 'w') as f:
                mytemplate = ctx.lookup.get_template(tmplt_path)
                try:
                    f.write(mytemplate.render(**tmplt_params))
                except:
                    print(exceptions.text_error_template().render())
        else:
            os.makedirs(outfile_path)
            ctx.current_tmplt_path = tmplt_path
            ctx.current_outpath = pjoin(ctx.current_outpath, outfile_name)
            apply_templates(ctx)

