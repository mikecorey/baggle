''' it's a (very) basic baggle game '''

import sys
import random
import time


class Baggle:
    ''' it's a basic Baggle game '''

    def __init__(self, time_limit=90, dictionary=None):
        self.time_limit = time_limit
        self.dictionary = dictionary
        self.found_words = []
        self.board = [[random.choice(Baggle.dice[i*4+j]) for j in range(4)] for i in range(4)]
        if self.dictionary:
            print(f'Using a dictionary with {len(self.dictionary)} words.')

    def play(self):
        ''' plays the game '''
        start = time.time()
        while time.time() - start < self.time_limit:
            self.print_board()
            print()
            word = input(f'{round(self.time_limit - (time.time() - start), 1)} > ')
            if time.time() - start < self.time_limit:
                if self.check_word(word):
                    self.found_words.append(word)
                    print(f'Added {word}')
                else:
                    print('Not Valid!')
            else:
                print('Out of time...')
        print(f'\nFinal words: {self.found_words}')
        print(f'TOTAL SCORE: {sum([Baggle.point_vals[min(len(w), 8)] for w in self.found_words])}')

    def cheat(self):
        ''' shows all the valid words in the dictionary '''
        for dict_word in self.dictionary:
            if self.check_word(dict_word, print_reason=False):
                print (dict_word)

    def check_word(self, word, print_reason=True):
        '''tests to see if a word is valid to play'''
        if len(word) < 3:
            if print_reason:
                print('Word too short!')
            return False
        if word in self.found_words:
            if print_reason:
                print('Already found word!')
            return False
        if not Baggle.__recursive_word_search(self.board, word.replace('qu', 'q')):
            if print_reason:
                print('Not on board!')
            return False
        if self.dictionary is not None and word not in self.dictionary:
            if print_reason:
                print('Not in dictionary!')
            return False
        return True

    def print_board(self):
        ''' prints the game board '''
        for i in range(4):
            print(''.join([f'{x if x != "q" else "qu":3}' for x in self.board[i]]))


    dice = ['hevwrt', 'lnnhzr', 'afpksf', 'estiso',
            'ltyetr', 'exilrd', 'baoobj', 'eeisun',
            'mutcio', 'qimunh', 'wttaoo', 'soahcp',
            'aaeegn', 'syidtt', 'revldy', 'ghwene'
            ]

    point_vals = [0, 0, 0, 1, 1, 2, 3, 5, 11]

    @staticmethod
    def __recursive_word_search(board, word, next_to=None):
        if len(word) == 0:
            return True
        starts = set()
        for i in range(4):
            for j in range(4):
                if board[i][j] == word[0]:
                    starts.add((i,j))
        if next_to is not None:
            adj = {(i,j) for j in range(next_to[1]-1,next_to[1]+2,1)
                for i in range(next_to[0]-1, next_to[0]+2, 1)}
            starts = starts.intersection(adj)
        for start in starts:
            new_board = [row[:] for row in board]
            new_board[start[0]][start[1]] = ''
            if Baggle.__recursive_word_search(new_board, word[1:], next_to=start):
                return True
        return False

    @staticmethod
    def load_dictionary(dict_filename):
        ''' loads a dictionary from a file. '''
        with open(dict_filename, 'r', encoding='utf-8') as dict_f:
            return [x.strip() for x in dict_f.readlines() if x[0].islower() and len(x) >= 3]


def main():
    ''' entry point for baggle game '''
    dictionary = None
    if len(sys.argv) > 1:
        dictionary = Baggle.load_dictionary(sys.argv[1])
    baggle = Baggle(time_limit=90, dictionary=dictionary)
    if len(sys.argv) > 2 and sys.argv[2] == 'CHEAT':
        baggle.cheat()
    baggle.play()


if __name__ == '__main__':
    main()
