import os


def inputfile():
    year_dir = '2015'
    filename = os.path.join(year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


def getinput(f, test):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read()
