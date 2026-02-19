import pytest
import utils

def test_load_toml(contacts_model):
    # Init vars
    fpath = 'tests/example_models/contacts.toml'
    with open(fpath, 'r') as toml_file:
        loaded_file = tomllib.loads(toml_file.read())

    # Is the file being correctly loaded?
    # Process
    result = utils.load_toml(fpath)
    # Assert
    assert result == loaded_file, 'Loaded files should be identical'

    # Does it work without the extension?
    # Process
    fpath = fpath[:-len('.toml')]
    result = utils.load_toml(fpath)
    # Assert
    assert result == loaded_file, 'File should be loadad even without the extension'