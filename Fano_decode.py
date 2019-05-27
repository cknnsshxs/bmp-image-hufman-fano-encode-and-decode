import json
import numpy as np
from PIL import Image


class LetterCodeword(object):
    def __init__(self, letter='', codeword=''):
        self.letter = letter
        self.codeword = codeword


def fano_decoder(codebook_dict, codes):
    codeword = ''
    letters = ''
    for i in range(len(codes)):
        codeword = codeword + codes[i]
        for key, value in dict_.items():
            if codeword == value:
                letters = letters + key + ' '
                codeword = ''
    return letters


if __name__ == '__main__':
    # get the codebook_dict file
    with open("lena256gray_Fano_codebook.json", 'r') as f:
        dict_ = json.load(f)

    # read the encode file
    with open("lena256gray_Fano_encode.txt", 'r') as f:
        string = f.read()

    # decoding
    print('\nGenerating the decode file ...')
    letters = fano_decoder(dict_, string)

    # write the decode file
    convert_list = letters.split()
    conv_list = [int(i) for i in convert_list]
    decode_matrix = np.array(conv_list).reshape(256, 256)
    decode_img = Image.fromarray(decode_matrix.astype('uint8'))
    decode_img_gray = decode_img.convert('L')
    decode_img_gray.save('lena256gray_Fano_decode.bmp')
    print('Save successfully as \"lena256color_Fano_decode.bmp\"')
