from zari.zari_model import ZariModel, ZariProp
from faker import Faker

fake = Faker()

config = ZariModel(
    name = "contact",
    namep = "contacts",
    default_str_length = 50,
    
    props = [
        ZariProp(
            name = "nombres",
            type = "string",
            optional = False,
            dummy_method = fake.first_name
        ),
        ZariProp(
            name = "apellidos",
            type = "string",
            dummy_method = fake.last_name,
        ),
        ZariProp(
            name = "tipo_id",
            type = "string",
            optional = False,
            valid_values = ["CC", "NIT", "TI", "CE"]
        ),
        ZariProp(
            name = "num_id",
            type = "string",
            optional = "n",
            long = 10,
            dummy_method = fake.numerify,
            dummy_args = {"string": "##########"}
        ),
        ZariProp(
            name = "telefonos",
            type = "string",
            long = 10,
            dummy_method = fake.numerify,
            dummy_args = {"string": "##########"}
        ),
        ZariProp(
            name = "direccion",
            type = "string",
            dummy_method = fake.address,
        ),
        ZariProp(
            name = "ciudad",
            type = "string",
            dummy_method = fake.city,
        ),
        ZariProp(
            name = "email",
            type = "string",
            dummy_method = fake.email,
        ),
        ZariProp(
            name = "webs",
            type = "string",
            dummy_method = fake.domain_name,
        ),
        ZariProp(
            name = "notas",
            type = "string",
            dummy_method = fake.sentence,
        ),
        ZariProp(
            name = "es_distribuidor",
            type = "bool",
            optional = False
        ),
        ZariProp(
            name = "es_cliente",
            type = "bool",
            optional = False
        )
    ]
)