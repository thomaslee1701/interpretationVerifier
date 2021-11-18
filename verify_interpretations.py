import re

class Verify:
    def __init__(self, interpretation, UD={1,2,3}):
        self.UD = UD
        self.interpretation = interpretation # Contains the interpretation we want to test
        self.values_dict = {} # Contains the current x, y, and z values
    """
    Inputs: 
    sets - the sets for the interpretation
    s - a letter for a set
    value - value to check if it is in the set s
    Returns: True or False depending on if the value is in the set.
    """
    def isin(self, s, value):
        return value in self.interpretation[s]

    def logic_and(self):
        return False

    """
    Inputs:
    query - string
    """
    def isSingleSet(self, query):
        # Check if query is in the form F{a...b}
        if len(query) < 4 or not query[0].isalpha():
            return False
        arguments = query[2:-1] # a...b
        return all([letter.isalpha() for letter in arguments])

    def isForAll(self, query):
        if query[:6].lower() == 'forall':
            return True
        return False

    def isExists(self, query):
        if query[:6].lower() == 'exists':
            return True
        return False

    def isAnd(self, query): # query in the form (...).(...)
        pattern = "^\((.*)\)\.\((.*)\)$"
        match = re.search(pattern, query)
        if match:
            return True
        else:
            return False

    def isOr(self, query): # query in the form (...)v(...)
        pattern = "^\((.*)\)v\((.*)\)$"
        match = re.search(pattern, query)
        if match:
            return True
        else:
            return False

    def isConditional(self, query): # query in the form (...)>(...)
        pattern = "^\((.*)\)>\((.*)\)$"
        match = re.search(pattern, query)
        if match:
            return True
        else:
            return False

    def isNot(self, query):
        if query[0]== '-':
            return True
        return False

    def isBiconditional(self, query): # query in the form (...)=(...)
        pattern = "^\((.*)\)=\((.*)\)$"
        match = re.search(pattern, query)
        if match:
            return True
        else:
            return False

    def verify(self, query):
        query = query.replace(" ", "")
        if self.isForAll(query): # query starts with ForAllx(...), ForAlly(...), etc...
            letter = query[6] # x, y, etc
            rest = query[8:-1]
            for value in self.UD:
                self.values_dict[letter] = value
                if not self.verify(rest):
                    return False
            return True
        elif self.isExists(query): # query starts with ForAllx(...), ForAlly(...), etc...
            letter = query[6] # x, y, etc
            rest = query[8:-1]
            for value in self.UD:
                self.values_dict[letter] = value
                if self.verify(rest):
                    return True
            return False
        elif self.isAnd(query):
            pattern = "^\((.*)\)\.\((.*)\)$"
            groups = re.search(pattern, query).groups()
            return self.verify(groups[0]) and self.verify(groups[1])
        elif self.isOr(query):
            pattern = "^\((.*)\)v\((.*)\)$"
            groups = re.search(pattern, query).groups()
            return self.verify(groups[0]) or self.verify(groups[1])
        elif self.isConditional(query):
            pattern = "^\((.*)\)>\((.*)\)$"
            groups = re.search(pattern, query).groups()
            return (not self.verify(groups[0])) or ((self.verify(groups[0]) and self.verify(groups[1])))
        elif self.isNot(query):
            rest = query[2:-1]
            return not self.verify(rest)
        elif self.isBiconditional(query):
            pattern = "^\((.*)\)=\((.*)\)$"
            groups = re.search(pattern, query).groups()
            return ((not self.verify(groups[0])) and (not self.verify(groups[1]))) or ((self.verify(groups[0]) and self.verify(groups[1])))
        elif self.isSingleSet(query): # query is in the form F{a...b}
            s = query[0]
            arguments = query[2:-1]
            arguments = list(arguments) # split up each individual letter x, y, etc
            converted_args = [self.values_dict[arg] for arg in arguments]
            if len(converted_args) == 1: # single element list -> just one argument
                converted_args = converted_args[0]
            return self.isin(s, converted_args)
        
        return False