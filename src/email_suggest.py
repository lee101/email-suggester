'''
Created on 14/03/2013

@author: user-000
'''
import unittest
from collections import defaultdict
import random
import re
import string

class Suggester(object):
    prob_given_previous_word = defaultdict(lambda: defaultdict(int))


    def write_email(self, body):
        '''
        given body a string of text containing training data 
        write some random stuff
        '''
        body = re.sub(r'\n\n+', r'\n', body)
        words = body.split(' ')

        newline_prob = body.count('\n') / float(len(words))
        end_prob = 1.0 / len(words)

        for i in range(len(words)):
            self.prob_given_previous_word[self.strip_punctuation(words[i - 1])][self.strip_punctuation(words[i])] += 1

        # # format the dict to allow picking words randomly
        for key in self.prob_given_previous_word.keys():
            self.prob_given_previous_word[key] = self.cdf(self.prob_given_previous_word[key])
            # #pick first word
        email = [random.choice(words)]
        prev_pos = 0
        while end_prob < random.random():
            if newline_prob > random.random():
                email[prev_pos] += ".\n"
                continue
                # use prob_given_previous_word to generate new word
            possible_next_words = self.prob_given_previous_word[self.strip_punctuation(email[prev_pos])]
            if len(possible_next_words) == 0:
                if not email[prev_pos].endswith(".\n"):
                    email[prev_pos] += ".\n"
                new_word = random.choice(words)
                email.append(new_word)
            else:
                word_pos = random.randint(0, possible_next_words[-1][1])
                new_word_pos = self.argmax(possible_next_words, lambda x: x[1] < word_pos)
                new_word = possible_next_words[new_word_pos][0]
                email.append(new_word)
            prev_pos += 1
        return ' '.join(email).replace(" ,", ",")

    def strip_punctuation(self,s):
        return  s.translate(string.maketrans("",""), string.punctuation).replace("\n","")
    def argmax(self, a, key=lambda x: x):
        maxIndex = 0
        maxVal = key(a[maxIndex])
        for i in range(1, len(a)):
            if key(a[i]) >= maxVal:
                maxIndex = i
                maxVal = key(a[maxIndex])
        return maxIndex


    def cdf(self, hist):
        '''
        takes in a dict or a counter object returns an array of pairs
        the values become a cumulative distribution function
        '''
        x = hist.items()
        for i in range(1, len(x)):
            x[i] = (x[i][0], x[i][1] + x[i - 1][1])
        return x


class Test(unittest.TestCase):
    def testArgMax(self):
        s = Suggester().argmax([1, 2, 3, 4, 5, 6, 7], key=lambda x: x != 7)
        self.assertEqual(s, 5)

    def testName(self):
        f = open('testdoc.txt')
        print Suggester().write_email(f.read())
    def testStripPunctuation(self):
        s = Suggester().strip_punctuation("hello,.;'\"()!@#$%^&*`\n")
        self.assertEqual(s, "hello")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
