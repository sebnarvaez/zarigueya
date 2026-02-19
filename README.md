# Zarigueya

General-purpose scaffolding for your app.

## Requisites

- [Mako](https://www.makotemplates.org/) - The templating engine.
- [Case Converter](https://pypi.org/project/case-converter/) - Utilites to transform word cases.
- [Faker](https://faker.readthedocs.io/en/master/) - Generate fake data.

## Usage

1. Create at least one file containing a model's details, which is a [TOML file](https://toml.io/en/latest) with the following structure:

```toml
name = # Model name in singular.
modelp = # Model name in plural.

[[props]] # A list of objects, each of which containing:

name = # Name of the property
type = # bundled types are: ["int", "float", "bool", "string"]. Additional types can be defined in conversions.toml
optional = # true|false (default: true). Whether the property is mandatory or optional.
dummy_data = # true|false (default: true). Set to false if you don't want to generate fake data for this specific property, even with the app's dummy_data flag set to true.

dummy_method = # (default: ""). What kind of dummy data should be generated. Must be a valid Faker method, check the Faker docs (https://faker.readthedocs.io/en/master/) to see which methods are available.
dummy_args = # (default: {}). Map of arguments for the Faker method.
valid_values = # (default: []). A list of valid values for this property. If empty no restrictions are assumed. If dummy_data generation is ON and this option is set,Faker's random_element will be used to generate the data.
default_value = # Value to use if left in blank,

[options] # The list of general options for the model. May be omitted if the defaults are fine for you.

gen_sql = # true|false (default: true). Whether to generate sql code.
dummy_data = # true|false (default: true). Whether to generate dummy data. Uses the **dummy_value** field of the property if available.
default_str_length = # (default: 100). Default length for the string type

[data] # A list containing the Initial data for the model. Each element must specify each property from the [[properties]] list exactly once.
```

2. Run `model_generator.py` with the corresponding arguments:

```
positional arguments:
  model_details         The path containing the TOML files with the models' details. There shall be one file per model, plus an optional gbl.toml file with global configuration parameters.

options:
  -h, --help            show this help message and exit
  -o, --outpath OUTPATH
                        Path of the file where the generated output will be saved in.Defaults to model_details/output.
  -t, --templates_path TEMPLATES_PATH
                        Path of the model templates. Defaults to templates/. Note that the provided template should support whatever other options you choose.
  -e, --exclude_files   Template files that will be excluded.
  -d, --gen_data        Whether to generate dummy data. Uses the dummy tag of the field properties.
  -v, --verbose         Print replaced strings in the template
```
