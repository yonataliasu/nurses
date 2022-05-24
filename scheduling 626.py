import pandas
from pulp import *


problem = LpProblem('num_nurses', LpMinimize)

def get_weekday_workers(starting, weekday):
  skipper = 0
  sum = 0
  for day in starting:
    if skipper == 1:
      skipper = 0
      continue
    if day == weekday:
      skipper = 1
      continue
    sum += starting[day]
  return sum

nurses_req = {
    'Sun':100,    
    'Mon':200,
    'Tue':150,
    'Wed':250,
    'Thu':90,
    'Fri':160,
    'Sat':300
    }
x = []
for index, weekday in enumerate(nurses_req.keys()):
  x.append(LpVariable(f'{weekday}', lowBound=0 , cat=LpInteger))

#Objective Function
problem += x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6], 'Objective Function'

#Constraints
problem += x[0] + x[3] + x[4] + x[5] + x[6] >= nurses_req['Mon'] , 'Monday Constraint'
problem += x[0] + x[1] + x[4] + x[5] + x[6] >= nurses_req['Tue'], 'Tuesday Constraint'
problem += x[0] + x[1] + x[2] + x[5] + x[6] >= nurses_req['Wed'], 'Wednesday Constraint'
problem += x[0] + x[1] + x[2] + x[3] + x[6] >= nurses_req['Thu'], 'Thursday Constraint'
problem += x[0] + x[1] + x[2] + x[3] + x[4] >= nurses_req['Fri'], 'Friday Constraint'
problem += x[1] + x[2] + x[3] + x[4] + x[5] >= nurses_req['Sat'], 'Saturday Constraint'
problem += x[2] + x[3] + x[4] + x[5] + x[6] >= nurses_req['Sun'], 'Sunday Constraint'

# Trivial constraints
problem += x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] >= 0
problem += x[0] >= 0
problem += x[1] >= 0
problem += x[2] >= 0
problem += x[3] >= 0
problem += x[4] >= 0
problem += x[5] >= 0
problem += x[6] >= 0

problem.solve()

starting = {}
for index, weekday in enumerate(nurses_req.keys()):
  starting[weekday] = int(x[index].varValue)

title = ["Number of Nurses starting duty", "Total number of Nurses working"]
data = []
for index, weekday in enumerate(nurses_req.keys()):
  data.append([])
  data[index].append(starting[weekday])
  data[index].append(get_weekday_workers(starting, weekday))
y = pandas.DataFrame(data, nurses_req.keys(), title)  
print(y)
print("Total Nurses: ", value(problem.objective))
