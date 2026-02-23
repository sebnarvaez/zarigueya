#!/bin/python3
import os
import tomllib
import re
import argparse
import utils
import shutil
from zarigueya_context import ZarigueyaContext
from zarigueya_context import load_default_context
from mako.template import Template
from mako import exceptions
from os.path import join as pjoin

# Variable references com in the style ${var}
regex_var_str = r"\${.+}"
# Lists (of models or their properties) are referenced as []
regex_model = re.compile(fr"\[(|{regex_var_str})\]")
regex_props = re.compile(fr"\[\[(|{regex_var_str})\]\]")

"""
Returns the name of the file or folder, replacing the corresponding
variables on the template's name
"""
def get_filename(rem: re.Match, t_fname: str, tmplt_params: dict) -> str:
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
def setup_cmd_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='Zarigueya', description='General-purpose scaffolding for your app.')

    parser.add_argument('models_details', action='store',
                        help="The path containing the TOML files for the models' details. " +
                            "There shall be one file per model, plus an optional " +
                            "gbl.toml file with global configuration parameters.")

    parser.add_argument('-o', '--outpath', default='models_details/output/',
                        help="Path of the file where the generated output will be saved in." +
                            "Defaults to model_details/output.")

    parser.add_argument('-t', '--templates_path',
                        help="Path of the model templates. Defaults to templates/. " + 
                            "Note that the provided template should support whatever other " +
                            "options you choose.")

    parser.add_argument('-e', '--exclude_files', action='store_true',
                        help="Template files that will be excluded.")
                    
    parser.add_argument('-d', '--gen_data', action='store_true',
                        help="Whether to generate dummy data. Uses the dummy tag of the " +
                            "field properties.")

    parser.add_argument('-p', '--profile', default='profiles/go_datastar',
                        help="Folder containing the conversions.toml file, in which the " +
                            " equivalent of datatypes for each used language is defined.")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Print replaced strings in the template")

    parser.add_argument('--no-case-funcs', action='store_true',
                        help="Don't import the default helper functions in template files; Related to case conversion.")

    return parser.parse_args()

"""
Create a Zarigueya Context from the command line arguments.
"""
def context_from_cmd(args: argparse.Namespace) -> ZarigueyaContext:
    
    tmplts_path = args.templates_path
    # If no template is provided, use the default
    if tmplts_path == None:
        tmplts_path = pjoin(os.path.dirname(os.path.realpath(__file__)), "templates")

    model_data = {}

    models_path = args.models_details
    out_path = args.outpath
    profile_path = args.profile
    use_case_funcs = not args.no_case_funcs

    if out_path == None:
        out_path = pjoin(input_path, 'output')

    return ZarigueyaContext(tmplts_path, models_path, out_path, profile_path, use_case_funcs)

"""
Find templates and process them.
@param ctx: holds current state of the structure.
"""
def apply_templates(ctx: ZarigueyaContext):
    # The template parameters is a dict containing the current model's
    # parameters, the global parameters (gbl), and the type conversions (conv).
    tmplts_params = {}
    # Helps deciding what to do with the file
    file_ready = False
    
    for infile_name in os.listdir(ctx.current_inpath):
        # infile_name is the name of the file/folder.
        # infile_path is its full path.
        infile_path = pjoin(ctx.current_inpath, infile_name)
        # Non-template files are just copied
        if '.tmplt' not in infile_name:
            shutil.copy2(
                infile_path,
                ctx.current_outpath)
            continue
        
        # Process files/folders that apply to all properties
        rem = regex_props.search(infile_name)
        if rem:
            if ctx.current_model is None:
                raise AttributeError(f"{infile_path}: double square-brackets notation ([[${{property}}]]) is for properties of a model, and thus is reserved for files/folders with a parent folder using single square-brackets notation ([${{model}}]).")
            
            if ctx.current_prop is not None:
                raise NotImplementedError("Nested properties are not currently supported")

            # Property definition. Can be either dierctly a list (1 element),
            # or an attribute of a list property (2 elements)
            prop_def = rem.group().split('.')
            if len(prop_def) < 1 or len(prop_def) > 2:
                raise AttributeError(f"{infile_path}: property definitions must contain one or two elements (separated by a period), found {len(prop_def)}: {prop_def}")
            
            prop_list = ctx.current_model[prop_def[0]]
            attr = prop_def[1] if len(prop_def == 2) else ''

            ctx.current_prop = (prop_list, attr)

            for prop in prop_list:
                if attr != '':
                    prop = prop[attr]

                outfile_name = infile_name[:rem.start()] + prop + infile_name[rem.end():]

                create_file_or_folder(ctx, infile_path, outfile_name, tmplt_params)
                
            ctx.current_prop = None
            file_ready = True

        # Process files/folders that apply to all models
        rem = regex_model.search(infile_name)
        if rem and not file_ready:
            if ctx.current_prop is not None:
                raise AttributeError(f"{infile_path}: A parent folder has the properties' double-square brackets [[]] notation, which isn't allowed for models file/folders (single square-bracket []).")

            for model in ctx.models:
                mdetails = utils.load_toml(ctx.models_path, model)
                ctx.current_model = mdetails
                tmplt_params = {
                    **mdetails, 
                    'gbl': ctx.gbl,
                    'conv': ctx.conversions
                }
                outfile_name = get_filename(rem, infile_name, tmplt_params)
                
                create_file_or_folder(ctx, infile_name, outfile_name, tmplt_params)
                file_ready = True
        
        if not file_ready:
            tmplt_params = {
                'models': ctx.models, 
                'gbl': ctx.gbl,
                'conv': ctx.conversions
            }
            outfile_name = get_filename(rem, infile_name, tmplt_params)
            
            create_file_or_folder(ctx, infile_name, outfile_name, tmplt_params)
            
def create_file_or_folder(ctx: ZarigueyaContext, infile_path: str, outfile_name: str, tmplt_params: dict):
    outfile_path = pjoin(ctx.current_outpath, outfile_name)
    infile_full_path = pjoin(ctx.tmplts_path, infile_path)

    if os.path.isfile(infile_full_path):
        with open(outfile_path, 'w') as f:
            mytemplate = ctx.lookup.get_template(infile_path)
            try:
                f.write(mytemplate.render(**tmplt_params))
            except:
                print(exceptions.text_error_template().render())
    else:
        os.makedirs(outfile_path)
        ctx.current_inpath = infile_path
        ctx.current_outpath = pjoin(ctx.current_outpath, outfile_name)
        apply_templates(ctx)

if __name__ == "__main__":

    args = setup_cmd_parser()
    ctx = context_from_cmd(args)
    #ctx = load_default_context()

    if not os.path.exists(ctx.out_path):
        os.makedirs(ctx.out_path)
    
    apply_templates(ctx)
