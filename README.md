# command-block-simulator
simulate some command block logic

## Syntax
### Command block
Commands will be put in a auto 'chain command block', execute one by one  
这里的命令将会放在一个auto的'CCB'里, 一个接一个运行下去

The *auto* and *cond* tag will control the execution of the command(just like in minecraft)  
cb的auto和cond控制命令会不会被执行(类似MC里)

if the command block is auto, and not conditional, or conditional and the last command executed is success(in this game tick), the command will be executed  
如果cb是auto, 而且不是cond, 或者是cond而且上一条命令成功执行(本游戏刻), 则会运行该命令

### prefix
#### cond:Command
make the command block become conditional(the last command executed in this game tick need to be success in order to execute the command)  
令命令方块成为条件制约(本游戏刻上一个命令成功执行时才能执行)
#### non-auto:Command
make the command block become not auto(however, this is only initiation, that means after enable command, it would not automatically reset)  
for command block that are not auto, it would not execute in any situation(unless enabled by the enable command)  
本命令方块不是auto:1b(不会自动执行, 必须先enable)  
注意: 这是初始状态, enable之后下次执行不会自动disable

### command
for the \<\> tags, it is required  
\<\>里的部分是必须的  
for the [] tags, they are optional  
[]里的部分不一定需要输入
#### mark \<markers name\> \[markers tag1\] \[markers tag2\] ...
place a marker in the position of the next command block(it is an entity, and users can use that marker to control the auto of the command block)  
在下一个命令的位置放置marker(可以控制该命令的auto)

Notice: This is not a regular command(will not be placed in command blocks)  
注意: 本命令不算一般命令(不会被放置在cb里)

#### enable \<marker name\> [marker tag]
Control the auto tag of the command block that the marker at(auto:1b, that means it would execute)  
auto:1b 指定marker所在的cb

#### disable \<marker name\> [marker tag]
Control the auto tag of the command block that the marker at(auto:0b, that means it would execute)  
auto:0b 指定marker所在的cb

#### tag \<selector\> \<add|remove\> \<tag\>
Add/remove tag from the specific marker  
为指定marker加上/删除tag

Note That this can only check the name and tag of the marker(for other parameters, it would be ignored)  
选择器部分目前只支持name和tag

#### say \<message\>
Print message on the screen  
输出指定信息

#### testfor \<what ever\>
Prompt the user to input if that command is success or not(this is the main function of this project)  
要求用户输入该句命令是成功还是失败

Note: t = success, others = fail  
t: 成功, 其他: 失败

## Example:
pseudocode:
```
if:
    testfor 1
    or
    testfor 2
then:
    say 1/2 success
    if:
        testfor @a[r=5]
    then:
        say people around here
    else:
        say no people here
else:
    if:
        testfor u
    then:
        say u are here
    else:
        say who is here
```
commands:
```
disable if_1
enable if_1_else
testfor 1
cond:disable if_1_else
cond:enable if_1
testfor 2
cond:disable if_1_else
cond:enable if_1
mark if_1
non-auto:say 1/2 success
mark if_1
non-auto:disable if_2
mark if_1
non-auto:enable if_2_else
mark if_1
non-auto:testfor @a[r=5]
mark if_1
non-auto:cond:disable if_2_else
mark if_1
non-auto:cond:enable if_2
mark if_2
non-auto:say people around here
mark if_2_else
non-auto:say no people here
mark if_1_else
non-auto:disable if_3
mark if_1_else
non-auto:enable if_3_else
mark if_1_else
non-auto:testfor u
mark if_1_else
non-auto:cond:disable if_3_else
mark if_1_else
non-auto:cond:enable if_3
mark if_3
non-auto:say u are here
mark if_3_else
non-auto:say who is here
```
