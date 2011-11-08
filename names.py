import random
words = [
         "noble",
         "altruistic",
         "honest",
         "friend",
         "loyal",
         "gentle",
         "good",
         "trustworthy",
         "innocent",
         "great",
         "harmless",
         "carefree",
         "obedient",
         "authentic",
         "reliable",
         "dependable",
         "true",
         "august",
         "grand",
         "majestic",
         "graceful",
         "sublime",
         "magnanimous",
         "ethical",
         "respectable",
         "healthy",
         "beautiful",
         "desire",
         "strong",
         "vindicated",
         "victor",
         "virtuous",
         "generous",
         "benevolent",
         "charitable",
         "helpful",
         "kind",
         ]
male_names = [
         "james",
         "john",
         "robert",
         "michael",
         "william",
         "david",
         "richard",
         "charles",
         "joseph",
         "thomas",
         "christopher",
         "daniel",
         "paul",
         "mark",
         "donald",
         "george",
         "kenneth",
         "steven",
         "edward",
         "brian",
         "ronald",
         "anthony",
         "kevin",
         "jason",
         "jeff",
         ]
female_names = [
         "mary",
         "patricia",
         "linda",
         "barbara",
         "elizabeth",
         "jennifer",
         "maria",
         "susan",
         "margaret",
         "dorothy",
         "lisa",
         "nancy",
         "karen",
         "betty",
         "helen",
         "sandra",
         "donna",
         "carol",
         "ruth",
         "sharon",
         "michelle",
         "laura",
         "sarah",
         "kimberly",
         "deborah",
         ]

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
    def __init__(self, source, chainlen = 2):
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            print "Chain length must be between 1 and 10, inclusive"
            sys.exit(0)
    
        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen
    
        for l in source:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def New(self):
        """
        New name from the Markov chain
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()  

def get_generator(dictionary):
    return MName(dictionary)

male_name_generator = get_generator(words + male_names)
female_name_generator = get_generator(words + female_names)
def get(male):
    if male:
        return male_name_generator.New()
    return female_name_generator.New()
    
