def get_method_name(method):
    if method == 'b':
        return 'blackened'
    elif method == 'p':
        return 'pixelised'
    elif method == 'gb':
        return 'blurred'
    elif method == 'gn':
        return 'noised'
    else:
        raise ValueError('Invalid anonymisation method.')

def cast_strength(method, strength):
    if method == 'b':
        return float(strength)
    elif method == 'p':
        return int(strength)
    elif method == 'gb':
        return float(strength)
    elif method == 'gn':
        return float(strength)
    else:
        raise ValueError('Invalid anonymisation method.')