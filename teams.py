'''
This holds the stuff for Team Management
'''
import re

#Module box
class Box():
    pass

#Module variables
__m = Box()
__m.teams = []





class Team():
    
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

    def point (self, point=1 ):
        self.points


# Return teams as a list
def listTeams():
    teams = []
    # will linearly become issue if alot of objects. don't expect to be issue (final last words)
    for obj in gc.get_objects():
        if isinstance(obj, Team):
            teams.append(obj)
    return teams

def showMyTeam(user):
    
    for team in __m.teams:
        if user in team.members:
            return team.teamname
        else:
            response = 'You were not found in a team'
            print response
            return response

def createTeam(command):
    teamname = re.sub('create ','',command,count=1)
    team = Team(teamname)
    __m.teams.append(team)
    print 'checkIfCommand print __m.teams: %s' % __m.teams # tests
    response = 'Created Team: %s' % (teamname)
    return response


def checkIfCommand(user, message):
    
    command = re.sub('team ','',message,count=1)

    if 'create' in command: 
        response = createTeam(command)
        return response

    elif 'join' in command:
        arg = re.sub('join ','',command,count=1)
        for team in __m.teams:
            if team.teamname is arg:
                team.addUser(user)
                response = '%s joined team %s!' % user , team.teamname
        return response

    elif 'leave' in command:
        arg = re.sub('leave ','',command,count=1)
        for team in __m.teams:
            if team.teamname is arg:
                team.removeUser(user)
                response = '%s left team %s!' % user , team.teamname
        return response

    elif 'show' in command:
        arg = re.sub('show ','',command,count=1)

        if 'all' in arg: 
            teams = (t.teamname for t in __m.teams)
            print teams
            response = 'The currently attending Teams are: \n   %s ' % ' '.join(teams)
            return response
            
        elif 'mine' in arg:
            response = showMyTeam(user)
            return response

        elif arg in __m.teams:
            for team in __m.teams:
                if user is team.teamname:
                    response = team.members
            return response
   
        else:
            response = 'I\'m afraid %s is not a team\nCreate it with "create team teamname"' % arg
            return response

        return response

    elif 'delete' in command:
        teamname = re.sub('delete ','',command,count=1)
        for team in __m.teams:
            if team.teamname is teamname:
                response = '%s has forfit like a little bitch, Sir.' % team.teamname
                __m.teams.remove(team)
        return response

    elif 'reset' in command:
        teamname = re.sub('reset','',command,count=1)
        __m.teams = []
        response = 'All of the teams have been cleared, Master Wayne'
        return response

    else:
        response = '''I only work with create, join, leave, show (all/teamname/mine), delete, and reset'''
        return response

    return response







