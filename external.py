'''
This holds the stuff for external stuff 
'''


class Team (teamname):
    
    def __init__ (self, teamname):
        self.teamname = teamname
        self.members = []
        self.points = 0

    def addUser (self, user):
        self.members.add(user)
        #return success        

    def removeUser (self, user):
        self.members.remove(user)
        #return success

    def listUsers (self):
        return self.members

    def addPoint


def listTeams():
    pass

def showMyTeam(user):
    
    for team in listteams():
        if member in team.members:
            return True
        else:
            return False 







