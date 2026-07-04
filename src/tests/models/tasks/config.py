from zari.zari_model import ZariModel, ZariProp

config = ZariModel(
    name = "contact",
    namep = "contacts",

    props = [
        ZariProp(
            name = "nombre",
            type = "string",
            optional = false,
            dummy_method = "sentence",
            dummy_args = {"nb_words": 6}
        ),
        ZariProp(
            name = "descripcion",
            type = "string",
            dummy_method = "text"
        ),
        ZariProp(
            name = "hecho",
            type = "bool"
        )
    ]
)