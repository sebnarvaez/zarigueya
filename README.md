# Zarigueya

General-purpose scaffolding for your app.

## Requisites

- [Mako](https://www.makotemplates.org/) - The templating engine.
- [Case Converter](https://pypi.org/project/case-converter/) - Utilites to transform word cases.
- [Faker](https://faker.readthedocs.io/en/master/) - Generate fake data.

## Usage

Zarigueya is built around data models, which is the source of all the information that will be used to fill the templates. Models are tied to a SQL Table, and are represented as folders containing:

- A `config.toml` file with the following structure (Know more about [TOML files](https://toml.io/en/latest)):

```toml
name = # Model name in singular.
namep = # Model name in plural.

# Optional parameters:
sql_engine = postgres|sqlite # (default: postgres)
gen_sql = true|false # (default: true). Whether to generate sql code.
dummy_data = true|false # (default: true). Whether to generate dummy data. Uses the **dummy_value** field of the property if available.
default_str_length = # (default: 100). Default length for the string type

[[props]] # One entry for each property of the model. Only fields with no default value are mandatory.

name = # Name of the property.
display_name = # Human readable name of the property.
type = # The SQL data type.
length = # The length in characters for text, or precision for numeric types.
precision = # Only applies for numeric types.
default_value = # (default: NULL) Value to use if left in blank.
optional = y|n # (default: y). Whether the property is mandatory or optional.
dummy_data = y|n # (default: y). Set to n to prevent generating fake data for this specific property, even if set to y in the general config.toml options.
dummy_method = # (default: ""). What kind of dummy data should be generated. Must be a valid Faker method, check the Faker docs (https://faker.readthedocs.io/en/master/) to see which methods are available.
dummy_args = # (default: {}). Map of arguments for the Faker method.
valid_values = # (default: []). A list of valid values for this property. If empty, no restrictions are assumed. If dummy_data generation is ON and this option is set, Faker's random_element will be used to generate the data.

```

- An optional `data.csv` file containing the initial data for the model. The first row is expected to have the colum names (field `name` from [[props]] in `config.toml`)

Once you've defined your models, run `model_generator.py` with the corresponding arguments:

```
positional arguments:
  model_details         The path containing the model definitions. There shall be one folder per model, plus an optional gbl.toml file with global configuration parameters.

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
