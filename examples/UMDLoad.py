if __name__ == "__main__":
    import sys
    sys.path.append('../')
    from Model import ServersModel, get_model_from_json
    import json
    model = get_model_from_json('data.json')
    print('model data has been read')
    print(model.get_descriptors())
    print('that\'s it')
