
def is_within_slice(index, pointer, substrate):
    """
    Principal evaluative (boolean) function behind the if loop of the rm function.


    Iterates through the pointer and calls parse_slice function if there is a colon
    Check if the index is within a slice range specified in pointer
    """

    start, stop, step = parse_slice(pointer, substrate)
    if start is None:
        start = 0
    if stop is None:
        stop = len(container['events'])

    indices = range(start, stop, step)
    if index in indices:
        return True
    else:
        return False

def is_first_colon(string):
    if re.match(r'^:', string):
        return True
    return False

def count_character(string, character):
    count = len(re.findall(character, string))
    return count

def parse_slice(slice_str, substrate):
    """
    Parse, or interpret, a slice string and return start, stop, and step values
    function is now dependent on is_first_colon function, which is a boolean return function,
    which using regex module 're' returns a true or false boolean value.

    pass the container['events'] as the substrate parameter, and
    pass the pointer argument as the slice_str parameter.

    if statements are based on the conception that if a re.match doesn't complete
    itself the returned value will be None. see 'if m is None:'.
    """

    if is_first_colon(slice_str):
        if count_character(slice_str, ':') == 3:
            m = re.match(r':(\d+)?:(\d+)?:(\d+)?', slice_str)
            start = 0
            stop = int(m.group(1)) if m.group(1) else None
            step = int(m.group(2)) if m.group(2) else 1
        elif count_character(slice_str, ':') == 2:
            m = re.match(r':(\d+)?:(\d+)?', slice_str)
            start = 0
            stop = int(m.group(1)) if m.group(1) else None
            step = int(m.group(2)) if m.group(2) else 1
        elif count_character(slice_str, ':') == 1:
            m = re.match(r':(\d+)', slice_str)
            start = 0
            stop = int(m.group(1)) if m.group(1) is not None else None
            step = 1
        elif count_character(slice_str, ':') == 0:
            m = re.match(r'(\d+)', slice_str)
            start, stop = int(m.group(1)), None
            step = 1
        return start, stop, step
    else:
        if count_character(slice_str, ':') == 3:
            m = re.match(r'(\d+)?:(\d+)?:(\d+)?', slice_str)
            start = int(m.group(1)) if m.group(1) else None
            stop = int(m.group(2)) if m.group(2) else m.group(1)
            step = int(m.group(3)) if m.group(3) else 1
        elif count_character(slice_str, ':') == 2:
            m = re.match(r'(\d+)?:(\d+)?', slice_str)
            start = int(m.group(1)) if m.group(1) else None
            stop = int(m.group(2)) if m.group(2) else m.group(1)
            step = int(m.group(3)) if m.group(3) else 1
        elif count_character(slice_str, ':') == 1 and re.match(r':$', slice_str):
            m = re.match(r'(\d+)?', slice_str)
            start = int(m.group(1)) if m.group(1) else None
            stop = len(container['events'])
            step = 1
        elif count_character(slice_str, ':') == 0:
            m = re.match(r'(\d+)', slice_str)
            start, stop = int(m.group(1)), None
            step = 1
        return start, stop, step
