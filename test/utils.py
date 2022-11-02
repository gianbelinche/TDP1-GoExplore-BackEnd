import copy


def generate_invalid(correct, invalid):
    result = []
    for key in correct.keys():
        for invalid_value in invalid[key]:
            cp = copy.deepcopy(correct)
            if invalid_value is None:
                del cp[key]
            else:
                cp[key] = invalid_value
            result.append(cp)
    return result
