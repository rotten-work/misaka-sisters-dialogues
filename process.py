# coding=utf8

import copy
from tqdm import tqdm

# Get the dialogues data
# The dialogues is a 1d list of dialogues containing new line
# Example:
"""
['天气好冷啊！不知道今天会不会下雪\r\n我希望下雪。do，御坂满怀期待地望着天空，如此回应\r\n注意保暖呀\r\n谢谢关心，你也要注意身体。do，御坂如此表达感谢', '我脸上长痘痘了\r\n我最近脸上也长痘痘了，我不喜欢痘痘。do，御坂如此述说\r\n一般我不长痘的\r\n你可以去医务室看看医生，他们应该知道如何治疗。do，御坂如此提议\r\n好的，我找时间去看医生\r\n那就去吧。do，御坂如此回应', '我去写作业了\r\n注意身体，不要熬夜。do，御坂如此表达关心\r\n嗯，我今晚会早点睡的\r\n你最近都瘦了。do，御坂如此指出\r\n嗯，是啊，要注意身体了\r\n没事的话，我告辞了。']
"""
def get_dialogues(path):
    # 读取对话数据
    with open(dialogues_path, 'rb') as f:
        data = f.read().decode("utf-8")

    # 注意需要区分linux和windows环境下的换行符
    if "\r\n" in data:
        dialogues = data.split("\r\n\r\n")
    else:
        dialogues = data.split("\n\n")
    
    print("there are {} dialogue(s) in dataset".format(len(dialogues)))
    # print(dialogues)

    return dialogues

# Convert dialogues to lines_list
# The lines_list is a 2d list of lines grouped by dialogues
# Example:
"""
[['天气好冷啊！不知道今天会不会下雪', '我希望下雪。do，御坂满怀期待地望着天空，如此回应', '注意保暖呀', '谢谢关心，你也要注意身体。do，御坂如此表达感谢'], ['我脸上长痘痘了', '我最近脸上也长痘痘了，我不喜欢痘痘。do，御坂如此述说', '一般我不长痘的', '你可以去医务室看看医生，他们应该知道如何治疗。do，御坂如此提议', '好的，我找时间去看医生', '那就去吧。do，御坂如此回应'], ['我去写作业了', '注意身体，不要熬夜。do，御坂如此表达关心', '嗯，我今晚会早点睡的', '你最近都瘦了。do，御坂如此指出', '嗯，是啊，要注意身体了', '没事的话，我告辞了。']]
"""
def dialogues_to_lines_list(dialogues):
    lines_list = []
    for index, dialogue in enumerate(tqdm(dialogues)):
        if "\r\n" in dialogue:
            utterances = dialogue.split("\r\n")
        else:
            utterances = dialogue.split("\n")

        lines_list.append(utterances)

    return lines_list

# Replace 'do' with a special character, like 'と'
# Example:
"""
[['天气好冷啊！不知道今天会不会下雪', '我希望下雪。と，御坂满怀期待地望着天空，如此回应', '注意保暖呀', '谢谢关心，你也要注意身体。と，御坂如此表达感谢'],
"""
def replace_do_with_special_character(lines_list, sp):
    for i, lines in enumerate(tqdm(lines_list)):
        for j, line in enumerate(lines):
            if j % 2 == 1:
                line = line.replace('do', sp)
                lines_list[i][j] = line
    
    return lines_list

# Replace '我' but not '我' in ‘我们’ with '御坂'
# Example:
"""
[['天气好冷啊！不知道今天会不会下雪', '御坂希望下雪。do，御坂满怀期待地望着天空，如此回应', '注意保暖呀', '谢谢关心，你也要注意身体。do，御坂如此表达感谢'],
"""
def replace_I_with_Yuban(lines_list):
    temp_characters = "@#$"
    for i, lines in enumerate(tqdm(lines_list)):
        for j, line in enumerate(lines):
            if j % 2 == 1:
                line = line.replace('我们', temp_characters)
                line = line.replace('我', '御坂')
                line = line.replace(temp_characters, '我们')
                lines_list[i][j] = line

    return lines_list

# Prefix '御坂，' to asking sentences
# Example:
"""
[['御坂，天气好冷啊！不知道今天会不会下雪', '我希望下雪。do，御坂满怀期待地望着天空，如此回应', '御坂，注意保暖呀', '谢谢关心，你也要注意身体。do，御坂如此表达感谢'], 
"""
def prefix_Yuban_to_asking_sentences(lines_list):
    for i, lines in enumerate(tqdm(lines_list)):
        for j, line in enumerate(lines):
            if j % 2 == 0:
                lines_list[i][j] = f"御坂，{line}"

    return lines_list

# Replace '御坂' with '我' in responding sentences
# Example:
"""
[['天气好冷啊！不知道今天会不会下雪', '我希望下雪。do，我满怀期待地望着天空，如此回应', '御坂，注意保暖呀', '谢谢关心，你也要注意身体。do，我如此表达感谢'], 
"""
def replace_Yuban_with_I(lines_list):
    for i, lines in enumerate(tqdm(lines_list)):
        for j, line in enumerate(lines):
            if j % 2 == 1:
                line = line.replace('御坂', '我')
                lines_list[i][j] = line

    return lines_list    


if __name__ == '__main__':
    dialogues_path = "御坂妹妹对话语料需求/dialogues_example.txt"
    dialogues = get_dialogues(dialogues_path)

    lines_list = dialogues_to_lines_list(dialogues)

    print("Replace_do_with_special_character:")
    input = copy.deepcopy(lines_list)
    result = replace_do_with_special_character(input, 'と')
    print(result)

    print("Replace_I_with_Yuban:")
    input = copy.deepcopy(lines_list)
    result = replace_I_with_Yuban(input)
    print(result)

    print("Prefix_Yuban_to_asking_sentences:")
    input = copy.deepcopy(lines_list)
    result = prefix_Yuban_to_asking_sentences(input)
    print(result)

    print("Replace_Yuban_with_I:")
    input = copy.deepcopy(lines_list)
    result = replace_Yuban_with_I(input)
    print(result)