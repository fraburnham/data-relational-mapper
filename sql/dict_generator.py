def verify_model_registered(registry, model):
    return model in registry


def verify_models_registered(registry, query):
    for model in query.keys():
        if not verify_model_registered(registry, model):
            return False

    return True
