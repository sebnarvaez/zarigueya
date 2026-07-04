from zari.zari_model import ZariModel, ZariProp

config = ZariModel(
    name = "contact",
    namep = "contacts",
    default_str_length = 50,
    
    props = [
        ZariProp(
            name = "nombres",
            type = "string",
            optional = False,
            dummy_method = "first_name"
        ),
        ZariProp(
            name = "apellidos",
            type = "string",
            dummy_method = "last_name",
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
            dummy_method = "numerify",
            dummy_args = {"string": "##########"}
        ),
        ZariProp(
            name = "telefonos",
            type = "string",
            long = 10,
            dummy_method = "numerify",
            dummy_args = {"string": "##########"}
        ),
        ZariProp(
            name = "direccion",
            type = "string",
            dummy_method = "address",
        ),
        ZariProp(
            name = "ciudad",
            type = "string",
            dummy_method = "city",
        ),
        ZariProp(
            name = "email",
            type = "string",
            dummy_method = "email",
        ),
        ZariProp(
            name = "webs",
            type = "string",
            dummy_method = "domain_name",
        ),
        ZariProp(
            name = "notas",
            type = "string",
            dummy_method = "sentence",
        ),
        ZariProp(
            name = "es_distribuidor",
            type = "bool",
            optional = false
        ),
        ZariProp(
            name = "es_cliente",
            type = "bool",
            optional = false
        )
    ]
)