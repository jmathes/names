import random
def get_wordlist(type):
    file = open(type+'.txt', 'r')
    list = file.readlines()
    file.close()
    return list

positive_adjectives = get_wordlist('positive_adjectives')
male_names = get_wordlist('male_names')
female_names = get_wordlist('female_names')
last_names = get_wordlist('last_names')

###############################################################################
# Markov Name model
# A random name generator, by Peter Corbett
# http://www.pick.ucam.org/~ptc24/mchain.html
# This script is hereby entered into the public domain
###############################################################################
class Mdict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.d:
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)  

class MName:
    """
    A name from a Markov chain
    """
    def __init__(self, source, chainlen = 2, maxlen = 9):
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            raise ValueError("Chain length must be between 1 and 10, inclusive (you provided %s)", chainlen)
    
        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen
        self.maxlen = maxlen
    
        for l in source:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def New(self, maxlen=None):
        """
        New name from the Markov chain
        """
        if maxlen is None:
            maxlen = self.maxlen
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if len(name) > maxlen:
                break
            elif suffix == "\n":
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()  


generators = {
              'male': MName(positive_adjectives + male_names),
              'female': MName(positive_adjectives + female_names),
              'androgynous': MName(positive_adjectives + male_names + female_names),
              'asexual': MName(positive_adjectives),
              'surname': MName(positive_adjectives + last_names),
              }
generators['surname'].maxlen = 15

def supported_types():
    return generators.keys() + ['random']

def get(type):
    if type == ['random']:
        type = random.choice(generators.keys())
    if type not in generators.keys():
        raise NotImplementedError('Unsupported name type: %s' % type)
    return generators[type].New()
