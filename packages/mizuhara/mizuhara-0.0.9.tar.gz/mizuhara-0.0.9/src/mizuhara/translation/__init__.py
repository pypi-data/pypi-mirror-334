import yaml


def translate(domain:str, key:str, language_code:str="en") -> str:
    """
    this function is charge of translate string, which is defined on yaml file in the same path, into another language_code.
    if you need customize, please create another yaml file on translation folder,
    and use this function to translate.

    :param domain: name or alternate path of yaml file.
    :param key: name of main key in yaml file.
    :param language_code: language that you want to translate to.
    :return: str
    """

    # read yaml file into dictionary.
    with open(f"translation/{domain.replace("_", "/")}.yml", mode="r", encoding="utf-8") as file:
        content = dict(yaml.safe_load(file))

    try:
        # return translated string
        return content.get(key.lower()).get(language_code)

    # if there is no key in yml file, return original string(key)
    except AttributeError:
        return key