# Provides a list of options for life.py
# Each line of the string represent a single row on the board, with 1 === alive and 0 === dead
# Expected format is a multiline string, where the first line is discarded and subsequent lines begin with no indentation. Place the end quotes on their own, otherwise empty line.

def get_seed(seed_desc):
    if seed_desc == 'Pulsar':
        return '''
0000000000000000000000000000000
0000000000000000000000000000000
0000111000111000000011100011100
0000000000000000000000000000000
0010000101000010001000010100001
0010000101000010001000010100001
0010000101000010001000010100001
0000111000111000000011100011100
0000000000000000000000000000000
0000111000111000000011100011100
0010000101000010001000010100001
0010000101000010001000010100001
0010000101000010001000010100001
0000000000000000000000000000000
0000111000111000000011100011100
'''
    elif seed_desc == 'Penta-decathlon':
        return '''
000000000000000000000000000000000000000
000000000000000000000000000000000000000
000000000000000000000000000000000000000
000000000000000000000000000000000000000
000000111000000000011100000000001110000
000000010000000000001000000000000100000
000000010000000000001000000000000100000
000000111000000000011100000000001110000
000000000000000000000000000000000000000
000000111000000000011100000000001110000
000000111000000000011100000000001110000
000000000000000000000000000000000000000
000000111000000000011100000000001110000
000000010000000000001000000000000100000
000000010000000000001000000000000100000
000000111000000000011100000000001110000
'''

def get_entity(entity_desc):
    if entity_desc == 'Pulsar':
        return '''
0011100011100
0000000000000
1000010100001
1000010100001
1000010100001
0011100011100
0000000000000
0011100011100
1000010100001
1000010100001
1000010100001
0000000000000
0011100011100
'''  
    elif entity_desc == 'R-pentomino':
        return '''
0110
1100
0100
'''
    elif entity_desc == '':
        return '''
'''