debug = False

lines = []
markers = []

def get_input():
    return input('>>> success? ').strip()
user_input = get_input

def input_continue():
    return input('press t to re-run(states of the command blocks would be kept, such as auto)')
if_continue = input_continue

def out(text,line=None):
    print(text)
output = out

def run(pcc_lines):
    parse_lines(pcc_lines)
    print(len(lines))
    print(len(markers))
    cont = True
    while cont:
        last_success = False
        for i in lines:
            if debug:
                output(i.str(last_success))
            last_success = i.run(last_success)
        cont = if_continue() == 't'
    for i in markers:
        if not i.has_run:
            print('line: %d' % i.line_num)
    for i in lines:
        if not i.has_run:
            print('line: %d' % i.line_num)
def find_marker(name,tag=None):
    if debug:
        for i in markers:
            output('    debug: name: %s, auto:%d' % (i.name, lines[i.command_num].auto))
    if len(name) == 0:
        temp_markers = markers
    elif not name.startswith('!'):
        temp_markers = [x for x in markers if x.name == name]
    else:
        temp_markers = [x for x in markers if x.name != name[1:]]
    if tag is None:
        return temp_markers
    else:
        if not tag.startswith('!'):
            return [x for x in temp_markers if tag in x.tags]
        else:
            return [x for x in temp_markers if tag[1:] not in x.tags]
def parse_selector(selector):
    arguments = selector[3:-1].split(',')
    name = ''
    tag = None
    for i in arguments:
        if i.startswith('name='):
            name = i[5:]
        elif i.startswith('tag='):
            tag = i[4:]
    return name, tag
def parse_lines(_lines):
    command_num = 0
    line_num = 0
    for line in _lines:
        line_num+=1
        i = line.strip()
        if len(i) == 0:
            pass
        elif i.startswith('//'):
            pass
        elif i.startswith('mark'):
            markers.append(Marker(i,command_num,line_num))
        else:
            lines.append(Line(i,line_num))
            command_num += 1
class Line:
    def __init__(self,line,line_num):
        self.text = line
        self.auto = True
        self.cond = False
        self.line_num = line_num
        self.has_run = False
        self.parse_prefix()
    def parse_prefix(self):
        if self.text.startswith('cond:'):
            self.cond = True
            self.text = self.text[5:]
            self.parse_prefix()
            return
        if self.text.startswith('non-auto:'):
            self.auto = False
            self.text = self.text[9:]
            self.parse_prefix()
            return
    def run(self, last_success):
        if self.auto:
            if (not self.cond) or last_success:
                result = self.run_command()
                if result:
                    self.has_run = True
                return result
        return False
    def run_command(self):
        tokens = self.text.split(' ')
        if tokens[0] == 'enable':
            if len(tokens) > 2:
                tag = tokens[2]
            else:
                tag = None
            success = False
            for i in find_marker(tokens[1],tag):
                if not lines[i.command_num].auto:
                    lines[i.command_num].auto = True
                    i.has_run = True
                    success = True
            return success
        elif tokens[0] == 'disable':
            if len(tokens) > 2:
                tag = tokens[2]
            else:
                tag = None
            success = False
            for i in find_marker(tokens[1],tag):
                if lines[i.command_num].auto:
                    lines[i.command_num].auto = False
                    i.has_run = True
                    success = True
            return success
        elif tokens[0] == 'tag':
            name, tag = parse_selector(tokens[1])
            if tokens[2] == 'add':
                for i in find_marker(name, tag):
                    if tokens[3] not in i.tags:
                        i.tags.append(tokens[3])
            elif tokens[2] == 'remove':
                for i in find_marker(name, tag):
                    if i.tags is not None and tokens[3] in i.tags:
                        i.tags.remove(tokens[3])
            return True
        elif tokens[0] == 'say':
            output(' '.join(tokens[1:]),self)
            return True
        elif tokens[0] == 'testfor':
            output(self.text)
            text = user_input()
            if text == 't':
                return True
            else:
                return False
        return False
    def str(self,last_success):
        return '    debug: %s, auto: %d, cond: %d, last_success: %d'\
                    % (self.text, self.auto, self.cond, last_success)
class Marker:
    def __init__(self,line,command_num,line_num):
        tokens = line.split(' ')
        if len(tokens) < 2 or tokens[0] != 'mark':
            raise 'mark_error'
        self.command_num = command_num
        self.name = tokens[1]
        self.tags = []
        self.line_num = line_num
        self.has_run = False
        if len(tokens) > 2:
            self.tags = [x for x in tokens[2:]]

if __name__ == '__main__':
    output("input commands(1 line for 1 command, 2 blank lines to exit")
    cont = True
    in_lines = []
    while True:
        user_in = input()
        if len(user_in) > 0:
            in_lines.append(user_in)
        else:
            if cont:
                cont = False
            else:
                break

    run(in_lines)
