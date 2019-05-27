import math
import json
import numpy as np
from PIL import Image


class LetterCodeword(object):
    def __init__(self, letter=0, weight=0, codeword=''):
        self.letter = letter
        self.weight = weight
        self.codeword = codeword


class LeafNode(object):
    def __init__(self, letter=0, weight=0, left=None, right=None, ok=0):
        self.letter = letter
        self.weight = weight
        self.left = left
        self.right = right
        self.ok = ok

    def isleaf(self):
        return True


class InterNode(object):
    def __init__(self, weight=0, left=None, right=None, ok=0):
        self.weight = weight
        self.left = left
        self.right = right
        self.ok = ok

    def isleaf(self):
        return False


def sort(list_):
    # sorted from small weight to large
    list_ = sorted(list_, key=lambda x: x.weight)  
    return list_


def get_weight(pixel_string_list):
    letter_weight_dict = dict()
    leaves = []
    for item in pixel_string_list:
        if item in letter_weight_dict:
            letter_weight_dict[item] += 1
        else:
            letter_weight_dict[item] = 1
    for key, value in letter_weight_dict.items():
        leaf = LeafNode()
        leaf.letter, leaf.weight = key, value
        leaves.append(leaf)
    return sort(leaves)


def build_huff_tree(list_):
    while len(list_) != 1:
        a, b = list_[0], list_[1]
        new_node = InterNode()
        new_node.weight = a.weight + b.weight
        new_node.left, new_node.right = a, b
        list_ = list_[2:]
        list_.append(new_node)
        list_ = sort(list_)
    huff_tree = list_[0]
    return huff_tree


def letter_coder(huff_tree, codeword):
    if huff_tree.isleaf():
        item = LetterCodeword()
        item.letter = huff_tree.letter
        item.weight = huff_tree.weight
        item.codeword = codeword
        huff_tree.ok = 1
        return item
    else:
        if huff_tree.left.ok != 1:
            codeword = codeword + '0'
            return letter_coder(huff_tree.left, codeword)
        elif huff_tree.right.ok != 1:
            codeword = codeword + '1'
            return letter_coder(huff_tree.right, codeword)
        else:
            huff_tree.ok = 1


def constr_dict(leaves):
    huff_tree = build_huff_tree(leaves)
    node_num = 2 * len(leaves) - 1
    dict_list = []
    codebook_dict = dict()
    for i in range(node_num):
        dict_list.append(letter_coder(huff_tree, ''))
    for i in range(len(dict_list) - 1, -1, -1):
        if dict_list[i] == None:
            dict_list.pop(i)
    for item in dict_list:
        codebook_dict[item.letter] = item.codeword
    return sort(dict_list), codebook_dict


def huff_coder(codebook_dict, pixel_string_list):
    output = ''
    for item in pixel_string_list:
        for key, value in codebook_dict.items():
            if item == key:
                output += value
    return output


def huff_efficiency(leaves, dict_list):
    total_weight = 0
    entropy = 0.0
    av_len = 0.0
    for item in leaves:
        total_weight += item.weight
    for item in leaves:
        p = item.weight / total_weight
        entropy = entropy - p * math.log(p, 2)
    for item in dict_list:
        p = item.weight / total_weight
        av_len = av_len + p * len(item.codeword)
    print("Source Entropy =", entropy)
    print("Average Length =", av_len)
    print("Coding Efficiency =", entropy / av_len)


if __name__ == "__main__":
    img = Image.open('lena256.bmp')
    mtx = np.array(img)
    mtx_list = mtx.tolist()
    mtx_list = sum(mtx_list, [])
    pixel_string_list = [str(i) for i in mtx_list]
    leaves = get_weight(pixel_string_list)

    # construct codebook_dict
    dict_list, codebook_dict = constr_dict(leaves)
    dict_str = ''
    for item in dict_list:
        dict_str = dict_str + item.letter + ' '
        dict_str = dict_str + item.codeword
        dict_str = dict_str + '\n'

    # calculate the coding efficiency
    huff_efficiency(leaves, dict_list)

    # write codebook file
    print('\nGenerating the codebook ...')
    with open("lena256gray_Huffman_codebook.txt", 'w') as f:
        f.write(dict_str)
    print('Write successfully as \"lena256gray_Huffman_codebook.txt\"')
    with open("lena256gray_Huffman_codebook.json", 'w') as f:
        json.dump(codebook_dict, f)
    print('Write successfully as \"lena256gray_Huffman_codebook.json\"')
    
    # encoding
    print('\nGenerating the encode file ...')
    codes = huff_coder(codebook_dict, pixel_string_list)

    # write encode file
    with open("lena256gray_Huffman_encode.txt", 'w') as f:
        f.write(codes)
    print('Write successfully as \"lena256gray_Huffman_encode.txt\"')
