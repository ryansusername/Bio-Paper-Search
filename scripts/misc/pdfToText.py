import textract
import codecs


def main():
    file = '504977.pdf'
    
    with codecs.open(file,encoding='iso8859_8',errors='ignore') as stream:
        byte_str = stream.read()

        result = textract.process(byte_str)


main()
