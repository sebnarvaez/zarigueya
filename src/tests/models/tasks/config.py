import sys
sys.path.append('/home/sebasnr/Documents/projects/zarigueya/src/')

from zari.zari_model import ZariModel, ZariProp
from faker import Faker

fake = Faker()

config = ZariModel(
    name = "contact",
    namep = "contacts",

    props = [
        ZariProp(
            name = "nombre",
            type = "string",
            optional = False,
            dummy_method = fake.sentence,
            dummy_args = {"nb_words": 6}
        ),
        ZariProp(
            name = "descripcion",
            type = "string",
            dummy_method = fake.text
        ),
        ZariProp(
            name = "hecho",
            type = "bool"
        )
    ]
)