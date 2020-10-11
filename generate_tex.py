from yaml import load, FullLoader

with open('data.yml', 'r') as f:
    data = load(f, Loader=FullLoader)


def safe(d, key):
    """Safely return value of the dict or empty string."""
    if key in d:
        return d[key]
    else:
        return ''


def print_personal_info(personal_info):
    lines = []
    if 'photo' in personal_info:
        lines.append('\\photoR{2.8cm}{' + personal_info['photo'] + '}')
    lines.append('\\personalinfo{\n')
    for key in personal_info:
        if key == 'photo':
            continue
        line = '  \\'
        line += key
        line += '{'
        line += safe(personal_info, key)
        line += '}\n'
        lines.append(line)
    lines.append('}\n')
    return lines


def print_list(items):
    """Return TeX lines of an itemize element."""
    lines = []
    lines.append('\\begin{itemize}\n')
    for item in items:
        lines.append('\\item ' + item + '\n')
    lines.append('\\end{itemize}\n')
    return lines


def print_event(event):
    """Return TeX lines for an event."""
    lines = []
    event = event['event']
    lines.append('\\cvevent{')
    lines[0] += safe(event, 'title') + '}{'
    lines[0] += safe(event, 'org') + '}{'
    lines[0] += safe(event, 'time') + '}{'
    lines[0] += safe(event, 'location') + '}\n'
    description = safe(event, 'description')
    if type(description) is str:
        lines.append(description + '\n')
    elif type(description) is list:
        lines += print_list(description)
    return lines


def print_quote(quote):
    """Return TeX lines for a quote."""
    lines = []
    lines.append('\\begin{quote}\n')
    lines.append(f"``{quote}''\n")
    lines.append('\\end{quote}\n')
    return lines


def print_achievement(achievement):
    """Return TeX lines for an achievement."""
    achievement = achievement['achievement']
    lines = ['\\cvachievement{']
    lines[0] += safe(achievement, 'icon') + '}{'
    lines[0] += safe(achievement, 'title') + '}{'
    lines[0] += safe(achievement, 'description') + '}\n'
    return lines


def print_badges(badges):
    """Return TeX lines for a list of badges."""
    lines = []
    for badge in badges:
        if badge == 'dividertag':
            lines.append('\n\\divider\\smallskip\n\n')
        elif badge == 'br':
            lines.append('\\\\')
        else:
            lines.append('\\cvtag{' + badge + '}\n')
    return lines


def print_scale(skill, points):
    """Return TeX lines for a skill scale."""
    lines = ['\\cvskill{']
    lines[0] += skill
    lines[0] += '}{'
    lines[0] += str(points)
    lines[0] += '}\n'
    return lines


def print_referee(referee):
    """Return TeX lines for a referee's information."""
    referee = referee['referee']
    lines = ['\\cvref{']
    lines[0] += safe(referee, 'name') + '}{'
    lines[0] += safe(referee, 'institute') + '}{'
    lines[0] += safe(referee, 'email') + '}{'
    addresses = safe(referee, 'addresses')
    if type(addresses) is str:
        lines[0] += addresses + '}\n'
    else:
        lines[0] += '\\\\'.join(addresses) + '}\n'
    return lines


def print_section(section):
    """Return TeX lines for a section."""
    section_type = list(section.keys())[0]
    section_body = section[section_type]
    section_heading = (section_body['heading']
                       if 'heading' in section_body
                       else section_type)
    section_items = (section_body['items']
                     if 'items' in section_body
                     else None)

    printers = {
        'events': print_event,
        # 'quote': print_quote,
        'achievements': print_achievement,
        # 'badges': print_badges,
        # 'scales': print_scale,
        'referees': print_referee
    }

    lines = []
    lines.append('\n\\cvsection{' + section_heading + '}\n')
    if section_type in printers:
        printer = printers[section_type]
        for i, item in enumerate(section_items):
            lines += printer(item)
            if i < len(section_items) - 1:
                lines.append('\n\\divider\n\n')
    elif section_type == 'quote':
        lines += print_quote(section_body['quote'])
    elif section_type == 'badges':
        lines += print_badges(section_items)
    elif section_type == 'scales':
        for i, item in enumerate(section_items):
            lines += print_scale(item, section_items[item])
            if i < len(section_items) - 1:
                lines.append('\n\\divider\n\n')
    return lines


def write_columns(column, column_name):
    """Write a column into a file."""
    with open(f'{column_name}.tex', 'w') as f:
        for section in column:
            f.writelines(print_section(section))


def write_colors(colorscheme):
    lines = ['\\ProvidesPackage{customized-colorschema}']
    colornames = {}
    for name in colorscheme:
        color = colorscheme[name]
        if color[0] != '#':
            colornames[name] = color
            continue
        else:
            color = color[1:]
            colorname = name + 'Color'
            colornames[name] = colorname
        line = '\\definecolor{'
        line += colorname + '}{HTML}{'
        line += color + '}\n'
        lines.append(line)

    for name in colornames:
        line = '\\colorlet{'
        line += name + '}{'
        line += colornames[name] + '}\n'
        lines.append(line)
    with open('customized-colorschema.sty', 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    with open('personal-info.tex', 'w') as f:
        f.writelines(print_personal_info(data['personalinfo']))
    write_columns(data['column-1'], 'column-1')
    write_columns(data['column-2'], 'column-2')
    write_colors(data['colorscheme'])
