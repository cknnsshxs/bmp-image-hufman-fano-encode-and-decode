# This file is used to implement fano encoding
from PIL import Image
import numpy as np
import math
import json
import sys

sys.setrecursionlimit(1000)


def creat_prob_dict(pixel_string_list):
    dict_sym_count = dict()
    prob_dict = dict()
    total_num = 0

    for v in pixel_string_list:
        if v in dict_sym_count:
            dict_sym_count[v] += 1
        else:
            dict_sym_count[v] = 1
        total_num += 1

    for key, value in dict_sym_count.items():
        prob = value / total_num
        prob_dict[key] = prob

    return prob_dict


# rearrange the symbol list in descending order and create symbol-probability-code list
def arrange_order(prob_dict):
    sym_prob_code = []
    prob_dict_order = dict(sorted(prob_dict.items(), key=lambda x:x[1], reverse=True))
    for key, value in prob_dict_order.items():
        sym_prob_code.append([key, value, ""])
    return sym_prob_code


# find the divide position
def divide_position(turple_list):  
    empty_list = []
    for k in range(len(turple_list)):
        sumA = 0
        sumB = 0
        for i in range(k):
            sumA += turple_list[i][1]
        for i in range(k, len(turple_list)):
            sumB += turple_list[i][1]
        dif = abs(sumA - sumB)
        empty_list.append((k, dif))
    sorted_list = sorted(empty_list, key=lambda dif: dif[1])
    return sorted_list[0][0]


# Fano coding process
def fano_coding(sym_prob_code, direc):  
    if len(sym_prob_code) == 1:
        if direc == 'left':
            sym_prob_code[0][2] += '0'
        elif direc == 'right':
            sym_prob_code[0][2] += '1'
        return
    if len(sym_prob_code) == 2:
        sym_prob_code[0][2] += '0'
        sym_prob_code[1][2] += '1'
        return
    index = divide_position(sym_prob_code)
    length = len(sym_prob_code)
    for i in range(index + 1):
        sym_prob_code[i][2] += '0'
    for i in range(index + 1, len(sym_prob_code)):
        sym_prob_code[i][2] += '1'
    fano_coding(sym_prob_code[0:index + 1], 'left')
    fano_coding(sym_prob_code[index + 1:length], 'right')
    return sym_prob_code


# Calculate the coding efficiency
def fano_efficiency(encode_list):
    total_weight = 0
    entropy = 0.0
    av_len = 0.0
    for item in encode_list:
        entropy = entropy - item[1]*math.log(item[1], 2)
        av_len = av_len + item[1] * len(item[2])
    print("Source Entropy =", entropy)
    print("Average Length =", av_len)
    print("Coding Efficiency =", entropy / av_len)


def fano_coder(pixel_string_list,codebook_dict):
    output_string = ""
    for item in pixel_string_list:
        for key, value in codebook_dict.items():
            if item == key:
                output_string += value
    return output_string


if __name__ == "__main__":
    img = Image.open('lena256.bmp')
    mtx = np.array(img)
    mtx_list = mtx.tolist()
    mtx_list = sum(mtx_list, [])
    pixel_string_list = [str(i) for i in mtx_list]

    prob_dict = creat_prob_dict(pixel_string_list)
    sym_prob_code = arrange_order(prob_dict)
    encode_list = fano_coding(sym_prob_code, 'left')
    codebook_dict = dict()
    for item in encode_list:
        codebook_dict[item[0]] = item[2]

    dict_str = ''
    for item in encode_list:
        dict_str = dict_str + item[0] + ' '
        dict_str = dict_str + item[2]
        dict_str = dict_str + '\n'

    fano_efficiency(encode_list)
    print('\nGenerating the codebook ...')
    with open("lena256gray_Fano_codebook.txt", 'w') as f:
        f.write(dict_str)
    print('Write successfully as \"lena256gray_Fano_codebook.txt\"')
    with open("lena256gray_Fano_codebook.json", 'w') as f:
        json.dump(codebook_dict, f)
    print('Write successfully as \"lena256gray_Fano_codebook.json\"')

    print("Encoding the file ...")
    write_content = fano_coder(pixel_string_list, codebook_dict)
    with open("lena256gray_Fano_encode.txt", 'w') as f:
        f.write(write_content)
    print('Write successfully as \"lena256gray_Fano_encode.txt\"')
