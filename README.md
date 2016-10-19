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

## Example 1(IF):
pseudocode:
```
if:
    testfor pca
    or
    testfor pcb
then:
    say 1
    if:
        testfor @a[r=5]
    then:
        say 2
    else:
        say 3
else:
    if:
        testfor pcc
    then:
        say 4
    else:
        say 5
```
commands:
```
disable x if_1
enable x if_1_else
testfor pca
cond:disable x if_1_else
cond:enable x if_1
testfor pcb
cond:disable x if_1_else
cond:enable x if_1
mark x if_1
non-auto:say 1
mark x if_1
non-auto:disable x if_2
mark x if_1
non-auto:testfor @a[r=5]
mark x if_1
non-auto:cond:disable x if_2_else
mark x if_1
non-auto:cond:enable x if_2
mark x if_1 if_2
non-auto:say 2
mark x if_1 if_2_else
non-auto:say 3
mark x if_1_else
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
non-auto:say 5
```
## Example 2(Event)
Execute the commands in 'do' when the commands in 'when' success for the **First Time**  
When the commands in 'when' fails, it would reset the 'do' part, and prepare for executing those commands when the commands in 'when' success again

I am bad at english, so i'll just give an example.

For the following example, it would say someone here when someone enters the r=3 area, but it would not say 'someone here' repeatedly.
Instead, it would wait until the player left that range, and say it when the player re-enter that range.

pseudocode
```
when:
    testfor @a[r=3]
do:
    say someone here
```
commands
```
enable do_1_reset
disable do_1
testfor @a[r=3]
cond:disable do_1_reset
cond:enable do_1 on
cond:tag @e[type=marker,name=do_1] remove on
mark do_1_reset
non-auto:tag @e[type=marker,name=do_1] add on
mark do_1 on
non-auto:say someone here
```
