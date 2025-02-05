from parser import Parser

if __name__ == '__main__':
    # url = input('Enter URL: ')  # 'https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/'
    zoon = Parser('https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/')
    # zoon._get_text_review()
    zoon._get_author()