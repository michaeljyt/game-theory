import sys


class Person:
    def __init__(self, name, canPropose, rankings):
        self.name = name  # string
        self.canPropose = canPropose  # boolean
        self.rankings = rankings  # list of strings containing preferences
        self.proposals = {}  # dictionary with key = place in ranking list, entry = suitor object
        self.tentMatch = None  # Person object of current tentative match
        self.partner = None  # Person object for final partner

    def propose(self, woman):
        woman.proposals[woman.rankings.index(self.name)] = self
        print(self.name + ' proposes to ' + woman.name + '.')

    def acceptProposal(self, man):
        try:
            self.tentMatch.tentMatch = None
        except:
            pass
        self.tentMatch = man
        man.tentMatch = self
        self.proposals = {}
        print(self.name + ' accepts proposal from ' + man.name + '.')

    def keepMatch(self):
        self.proposals = {}
        print(self.name + ' stays matched with ' + self.tentMatch.name + '.')


class Matcher:
    def __init__(self, number):
        self.people = {}
        self.number = number

    def _readIn(self):
        return sys.stdin.readline().strip()

    def _toClass(self, string):
        return self.people[string]

    def newPerson(self):
        print('Enter name:')
        newName = self._readIn()
        print('Can propose? (T/F)')
        proposes = self._readIn()
        if proposes == 'T':
            canPropose = True
        elif proposes == 'F':
            canPropose = False
        else:
            raise Exception("Must be T or F.")
        newName = Person(newName, canPropose, [])
        self.people[newName.name] = newName

    def addRankings(self):
        print('Which person would you like to add rankings for?')
        name = self._readIn()
        print('Add people in order of ranking, each name on a new line. Enter "Done" when finished entering names')
        stillEntering = True
        while stillEntering:
            newEntry = self._readIn()
            if newEntry == 'Done':
                stillEntering = False
            else:
                self._toClass(name).rankings.append(newEntry)

    def help(self):
        pass

    def matchRound(self, n):

        for person in self.people:
            person = self.people[person]
            if person.canPropose and person.tentMatch is None:
                choice = self._toClass(person.rankings[n-1])
                person.propose(choice)

        for person in self.people:
            person = self.people[person]
            if not person.canPropose and len(person.proposals) >= 1:
                topProposal = person.proposals[min(person.proposals)]
                if person.tentMatch is None:
                    person.acceptProposal(topProposal)
                elif person.rankings.index(person.tentMatch.name) < person.rankings.index(topProposal.name):
                    person.keepMatch()

        for person in self.people:
            person = self.people[person]
            try:
                if person.canPropose:
                    print(person.name + " is tentatively matched with " + person.tentMatch.name +".")
            except:
                print(person.name + " currently has no match.")
        sys.stdin.readline()

    def singleMen(self):
        single = 0
        for person in self.people:
            person = self.people[person]
            if person.canPropose and person.tentMatch is None:
                single += 1
        return single

    def marriageMatch(self):

        for person in self.people:
            person = self.people[person]
            print(person.name + (' can propose ' if person.canPropose else ' cannot propose ') +
                  'and has preference list ' + ", ".join(person.rankings))
        sys.stdin.readline()
        n = 0
        while self.singleMen() > 0:
            n += 1
            self.matchRound(n)
        for person in self.people:
            person = self.people[person]
            person.partner = person.tentMatch
            if person.canPropose:
                print(person.name + " marries " + person.partner.name + '.')
