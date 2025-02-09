from parser import *

# url = input('Enter URL: ')  # 'https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/'
if __name__ == '__main__':
    url = "https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/"

    parser = Parser(url)
    parser.add_parser(StarsParser())
    parser.add_parser(AuthorParser())
    parser.add_parser(ReviewParser())
    parser.run()