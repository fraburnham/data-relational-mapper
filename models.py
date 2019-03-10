from functools import singledispatch

# this fn may not belong in here
def __query_engine_factory(models):
    return lambda query_map: print(query_map)


@singledispatch
def register_models(models):
    raise Exception("query_engine_factory not implemented for {}".format(type(models)))


@register_models.register(list)
def register_models_list(models):
    model_dict = {}
    for model in models:
        # this seems like there must be a better, more pythonic way
        model_dict = {**model_dict, **model}


@register_models.register(dict)
def register_models_dict(models):
    return __query_engine_factory(models)
