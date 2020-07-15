__data = list()


def LogEveLoading():
    return __data


def log(event_name):
    __data.append(event_name)
