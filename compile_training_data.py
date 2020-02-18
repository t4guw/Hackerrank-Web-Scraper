import re
import numpy as np

def get_dataset():
    pairs = get_pairs() # list of raw statements/solutions

    #build_dictionary_file(pairs[0])

    tokenized_states = []
    
    vocab = open('vocabulary.txt', 'r')
    word_dict = {}
    rank = 1
    lines = vocab.readlines()

    for word in lines:
        word_dict[word[:-1]] = rank
        rank += 1
    raw_words = []
    for statement in pairs[0]:
        statement = re.split(r'[\.\!\?\,\:\;\(\)\s*]', statement.replace('\n', ''))
        while '' in statement:
            statement.remove('')
        print(statement)
        tokenized_states.append([word_dict[word.lower()] for word in statement])
        raw_words.append(statement)
    
    labels = label_nested_for(pairs[1])

    return ((np.array(tokenized_states[0:300]), np.array(labels[0:300])), (np.array(tokenized_states[300:-1]), np.array(labels[300:-1])))

def get_pairs():
    file = open("algorithms_problems_hr.txt", "r")
    raw_lines = file.read()

    statement_re = re.compile(r'(?<=STATEMENT:)[\w\W]+?(?=----------)')
    solution_re = re.compile(r'(?<=TOP SOLUTION:\W----------)[\w\W]+?(?=----------)')
    raw_str = ''

    for line in raw_lines:
        raw_str += line

    found_statements = statement_re.findall(raw_str)
    found_solutions = solution_re.findall(raw_str)

    statements_cleaned = []
    solutions_cleaned = []

    for i in range(len(found_statements)):
        if not ('{"models":[],"page":1,"total":0}' in found_solutions[i]):
            statements_cleaned.append(found_statements[i])
            solutions_cleaned.append(found_solutions[i])
    
    return (statements_cleaned, solutions_cleaned)

def get_label(sol_lines):
    #print(sol_lines)
    for_re = re.compile(r'^[\W]+?(?=for)')
    end_re = re.compile(r'^[\W]+?(?=[\w])')

    for_len = 0
    for_flag = False

    for_len = 0
    for line in sol_lines:
        line = line.replace('\t', '    ')
        #print(line, for_re.findall(line))
        
        curr_found = (for_re.findall(line), end_re.findall(line))
        

        curr_for_len = 0
        curr_end_len = 0

        if len(curr_found[0]) != 0:
            curr_for_len = len(curr_found[0][0])
        if len(curr_found[1]) != 0:
            curr_end_len = len(curr_found[1][0])
        
        if curr_for_len != 0:
            #print(curr_for_len, for_len, for_flag)
            if for_flag and curr_for_len > for_len:
                #print(curr_for_len, for_len, for_flag)
                return 1
            for_flag = True
            for_len = curr_for_len
        elif for_flag and curr_end_len == for_len:
            for_len = 0
            for_flag = False
            continue
    return 0

def label_nested_for(solutions):
    pairs = get_pairs()
    label_list = []
    count = 0
    #print(get_label(pairs[1][16].splitlines()))
    for sol_str in solutions:
        count += 1
        label_list.append(get_label(sol_str.splitlines()))
        
       
    return label_list





def build_stat_file():
    file = open("statements.txt", "w")
    pairs = get_pairs()

    for element in pairs[0]:
        element = element.splitlines()
        
        file.write(element)

def build_dictionary_file(statements):
    word_dict = {}
    for statement in statements:
        #print(re.split(r'[\.\!\?\s*]', statement))
        for word in re.split(r'[\.\!\?\,\:\;\(\)\s*]', statement.replace('\n', '')):
            word = word.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    vocab = open('vocabulary.txt', 'w')
    for word in sorted(word_dict, key=word_dict.get, reverse=True):
        vocab.write(word + '\n')
