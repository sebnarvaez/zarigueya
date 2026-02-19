import pytest
import unittest
import difflib
import utils
from model_generator import *
from zarigueya_context import ZarigueyaContext

@pytest.fixture
def zari_ctx() -> ZarigueyaContext:
    tmplts_path = 'tests/templates'
    models_path = 'tests/models'
    profile_path = 'tests/profile'
    out_path = pjoin(models_path, 'output')

    return ZarigueyaContext(tmplts_path, models_path, out_path, profile_path)

@pytest.fixture
def contacts_model() -> dict[str, any]:
    fpath = 'tests/models/contacts.toml'
    with open(fpath, 'r') as toml_file:
        return tomllib.loads(toml_file.read())

def test_get_filename(zari_ctx, contacts_model):
    # Change names to maintain compatibility with main source code
    ctx = zari_ctx
    mdetails = contacts_model
    # Init vars
    tmplt_params = {
        **mdetails, 
        'gbl': ctx.gbl,
        'conv': ctx.conversions
    }
    # Is .tmplt being removed?
    fname = 'example.tmplt.go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result.find('.tmplt') == -1, "output file name should not have '.tmplt' on it"

    # Is name intact if there's nothing to replace?
    fname = 'example.go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == fname, "output file name should not have been altered"

    # does the model name replace the empty square brackets?
    fname = '[].go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'{tmplt_params['name']}.go', "file with an empty [] should default to the model's name"
    
    # does a model's property get correctly replaced?
    fname = '[${namep}].go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'{contacts_model['namep']}.go', "file with an empty [] should default to the model's name"

    # does it work if the square brackets are preceded by other characters?
    fname = 'pre_[${namep}].go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'pre_{contacts_model['namep']}.go', "file with an empty [] should default to the model's name"

    # does it work if the square brackets are followed by other characters?
    fname = '[${namep}]_post.go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'{contacts_model['namep']}_post.go', "file with an empty [] should default to the model's name"

    # does it work if the square brackets are between other characters?
    fname = 'pre_[${namep}]_post.go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'pre_{contacts_model['namep']}_post.go', "file with an empty [] should default to the model's name"

    # does it work if the square brackets are empty AND between other characters?
    fname = 'pre_[]_post.go'
    rem = regex_model.search(fname)
    result = get_filename(rem, fname, tmplt_params)
    # Assert
    assert result == f'pre_{contacts_model['name']}_post.go', "file with an empty [] should default to the model's name"

    
def test_create_file_or_folder(tmp_path, zari_ctx):
    # Change names to maintain compatibility with main source code
    ctx = zari_ctx
    # Init vars
    infile_path = 'main.tmplt.go'
    expectedf_path = 'tests/models/expected_output/main.go'
    tmplt_params = {
        'models': ctx.models,
        'gbl': ctx.gbl,
        'conv': ctx.conversions
    }
    ctx.current_outpath = tmp_path.absolute()
    outfile_name = 'main.go'

    create_file_or_folder(ctx, infile_path, outfile_name, tmplt_params)

    with open(pjoin(ctx.current_outpath, outfile_name)) as gen_file, open(expectedf_path) as expec_file:
        generated = gen_file.readlines()
        expected = expec_file.readlines()
    
    diff = difflib.ndiff(expected, generated)
    changes: list[str] = []
    line_number = 1

    for line in diff:
        # elements starting with white space means the line is the same
        # in both files.
        if not line.startswith("  "):
            # elements starting with ?, then there are three elements refering
            # to the same line. The previous corresponds to the first file,
            # the ? shows the approx. location of the difference, and the next
            # to the second file 
            if line.startswith("? "):
                line_number -= 1

            changes.append(f"line {line_number:03d}: {line}")
            
            if line.startswith("? "):
                continue
        line_number += 1
    
    assert len(changes) == 0, f"""
Generated and expected files are not equal. Check the diff:
    -: Exclusive of expected file
    +: Exclusive of generated file
    ?: Marks the aprox. position of the difference in the line
  
{"".join(changes)}"""