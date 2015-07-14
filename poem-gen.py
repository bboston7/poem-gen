#!/usr/bin/env python3

import os
import random

BEGIN = 0
END = 1

POEM_DIR = "poems"

class markov:
    def __init__(self):
        # word -> next word -> number of occurences
        self.associations = {}

    def _add_token(self, token, next):
        # Add a single word
        try:
            nexts = self.associations[token]
            try:
                nexts[next] += 1
            except KeyError:
                nexts[next] = 1
        except KeyError:
            nexts = {next : 1}
            self.associations[token] = nexts


    def add(self, example, preserve_newlines=False):
        """ Add example to dict of associations """

        if preserve_newlines:
            lines = example.splitlines(True)
            tokens = []
            for line in lines:
                tokens.extend(line.split(" "))
        else:
            tokens = example.split()

        if not len(tokens):
            # Empty example
            return

        for i in range(len(tokens)-1):
            # Add tokens one by one
            self._add_token(tokens[i], tokens[i+1])

        # Add begin marker for first token
        self._add_token(BEGIN, tokens[0])

        # Add end terminator for final token
        self._add_token(tokens[-1], END)

    def get_next(self, word):
        nexts = self.associations[word]

        count = 0
        for _, val in nexts.items():
            # Count total next words
            count += val

        # Randomly pick a number
        index = random.randint(1, count)

        # Count down to element
        for word, val in nexts.items():
            if index <= val:
                return word
            else:
                index -= val

        assert False

def parse_poem(fname, examples):
    """ Parse a poem.  Takes a file name and list of examples to populate """
    with open(fname) as f:
        last = False
        start = False
        for line in f:
            assert(len(line))
            if start:
                if line != "\n":
                    if last:
                        examples[-1] += line
                    else:
                        examples.append(line)
                        last = True
                else:
                    last = False
            elif line == "\n":
                # Ignore lines until first empty line
                start = True
    assert len(examples) > 1
    return examples

def parse_poems():
    """ Parse all poems in POEM_DIR.
    Returns a dictionary from author to markov chain """
    chains = {}
    for name in os.listdir(POEM_DIR):
        print("training " + name)
        examples = []
        for poem_file in os.listdir(POEM_DIR + "/" + name):
            parse_poem(POEM_DIR + "/" + name + "/" + poem_file, examples)
        m = markov()
        for example in examples:
            m.add(example, preserve_newlines=True)
        chains[name] = m
    return chains

def generate_poem(chain):
    """ Generate a poem from a given markov chain """
    next = chain.get_next(BEGIN)
    line = next
    next = chain.get_next(next)
    while next != END:
        if not line or line[-1] != "\n":
            line += " "
        line += next
        next = chain.get_next(next)
    return line


if __name__ == "__main__":
    chains = parse_poems()
    print("done!")
    while True:
        author = input("author? ")
        print()
        print(generate_poem(chains[author]))
