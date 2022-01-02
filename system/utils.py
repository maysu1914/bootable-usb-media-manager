def string_to_dict(data, remove_last_line=False):
    lines = data.split('\n')[:-1] if remove_last_line else data.split('\n')
    filtered_lines = []
    for index, line in enumerate(lines):
        if ':' not in line:
            continue
        splitted = line.split(':')
        if not splitted[1]:
            for next_line in lines[index + 1:]:
                if ':' in next_line:
                    break
                else:
                    splitted[1] += next_line
        filtered_lines.append(splitted)
    return {line[0].strip(): line[1].strip() for line in filtered_lines}


def get_last_item_from_path(path):
    for item in reversed(path.split('\\')):
        if item:
            return item.replace('/', '')
    return
