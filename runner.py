lines = """disable x if_1
enable x if_1_else
testfor pca
cond:disable x if_1_else
cond:enable x if_1
testfor pcb
cond:disable x if_1_else
cond:enable x if_1
//then部分
mark x if_1
non-auto:say 1
mark x if_1
//第二个if初始化
non-auto:disable x if_2
mark x if_1
non-auto:testfor @a[r=5]
mark x if_1
non-auto:cond:disable x if_2_else
mark x if_1
non-auto:cond:enable x if_2
//第二个if的then
mark x if_1 if_2
non-auto:say 2
//第二个if的else
mark x if_1 if_2_else
non-auto:say 3
//第一个if的else
mark x if_1_else
//第三个if
non-auto:disable x if_3
mark x if_1_else
non-auto:testfor pcc
mark x if_1_else
non-auto:cond:disable x if_3_else
mark x if_1_else
non-auto:cond:enable x if_3
mark x if_1_else if_3
non-auto:say 4
mark x if_1_else if_3_else
non-auto:say 5"""

import run_command
import random

cases = (
            ('t','f','1','t','2'),
            ('t','f','1','f','3'),
            ('f','t','1','t','2'),
            ('f','t','1','f','3'),
            ('t','t','1','t','2'),
            ('t','t','1','f','3'),
            ('f','f','t','4'),
            ('f','f','f','5')
        )
class IfTestCases:
    def __init__(self,cases,count=1):
        self.cases = cases
        self.case_index = 0
        self.state_index = 0
        self.cases_left = [x for x in range(len(cases))]
        self.count = count

    def get_input(self):
        result = self.cases[self.case_index][self.state_index]
        self.state_index += 1
        #print(result)
        return result
    def check_output(self,output,line=None):
        #print(output)
        if line is None:
            return
        expected = self.cases[self.case_index][self.state_index]
        self.state_index += 1
        if output != expected:
            print('case: %d, line: %d, expected: %s, actual: %s' % (self.case_index, line.line_num, expected, output))
    def has_cases(self):
        if len(self.cases_left) == 0:
            self.cases_left = [x for x in range(len(self.cases))]
        self.case_index = random.choice(self.cases_left)
        self.cases_left.remove(self.case_index)
        self.count -= 1
        self.state_index = 0
        return 't' if self.count > 0 else 'f'

test_cases = IfTestCases(cases,50)

run_command.user_input = test_cases.get_input
run_command.output = test_cases.check_output
run_command.if_continue = test_cases.has_cases

run_command.run(lines.split('\n'))
