from parser import *

if __name__ == '__main__':
    # url = input('Enter URL: ')  # 'https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/'
    zoon = Parser('https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/')
    print(zoon._get_text_review(), '\n')
    print(zoon._get_author())