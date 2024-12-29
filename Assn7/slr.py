import copy
from tabulate import tabulate

# perform grammar augmentation
def grammarAugmentation(rules, nonterm_userdef, start_symbol):

	newRules = []
	newChar = start_symbol + "'"
	while newChar in nonterm_userdef:
		newChar += "'"

	newRules.append([newChar, ['.', start_symbol]])

	for rule in rules:
		k = rule.split("->")
		lhs = k[0].strip()
		rhs = k[1].strip()
		
		multirhs = rhs.split('|')
		for rhs1 in multirhs:
			rhs1 = rhs1.strip().split()
			rhs1.insert(0, '.')
			newRules.append([lhs, rhs1])
	return newRules


# find closure
def findClosure(input_state, dotSymbol):
	global start_symbol, separatedRulesList, statesDict
	closureSet = []

	if dotSymbol == start_symbol:
		for rule in separatedRulesList:
			if rule[0] == dotSymbol:
				closureSet.append(rule)
	else:
		closureSet = input_state

	prevLen = -1
	while prevLen != len(closureSet):
		prevLen = len(closureSet)
		tempClosureSet = []
		for rule in closureSet:
			indexOfDot = rule[1].index('.')
			if rule[1][-1] != '.':
				dotPointsHere = rule[1][indexOfDot + 1]
				for in_rule in separatedRulesList:
					if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
						tempClosureSet.append(in_rule)
		for rule in tempClosureSet:
			if rule not in closureSet:
				closureSet.append(rule)
	return closureSet


def compute_GOTO(state):
	global statesDict, stateCount

	generateStatesFor = []
	for rule in statesDict[state]:
		if rule[1][-1] != '.':
			indexOfDot = rule[1].index('.')
			dotPointsHere = rule[1][indexOfDot + 1]
			if dotPointsHere not in generateStatesFor:
				generateStatesFor.append(dotPointsHere)

	if len(generateStatesFor) != 0:
		for symbol in generateStatesFor:
			GOTO(state, symbol)
	return


def GOTO(state, charNextToDot):
	global statesDict, stateCount, stateMap

	newState = []
	for rule in statesDict[state]:
		indexOfDot = rule[1].index('.')
		if rule[1][-1] != '.':
			if rule[1][indexOfDot + 1] == charNextToDot:
				shiftedRule = copy.deepcopy(rule)
				shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
				shiftedRule[1][indexOfDot + 1] = '.'
				newState.append(shiftedRule)

	addClosureRules = []
	for rule in newState:
		indexDot = rule[1].index('.')
		if rule[1][-1] != '.':
			closureRes = findClosure(newState, rule[1][indexDot + 1])
			for rule in closureRes:
				if rule not in addClosureRules and rule not in newState:
					addClosureRules.append(rule)

	for rule in addClosureRules:
		newState.append(rule)

	stateExists = -1
	for state_num in statesDict:
		if statesDict[state_num] == newState:
			stateExists = state_num
			break

	if stateExists == -1:
		stateCount += 1
		statesDict[stateCount] = newState
		stateMap[(state, charNextToDot)] = stateCount
	else:
		stateMap[(state, charNextToDot)] = stateExists
	return


def generateStates(statesDict):
	prev_len = -1
	called_GOTO_on = []
	while len(statesDict) != prev_len:
		prev_len = len(statesDict)
		keys = list(statesDict.keys())
		for key in keys:
			if key not in called_GOTO_on:
				called_GOTO_on.append(key)
				compute_GOTO(key)
	return


# calculation of first
def first(rule):
	global rules, nonterm_userdef, term_userdef, diction, firsts
	
	if len(rule) != 0 and (rule is not None):
		if rule[0] in term_userdef:
			return rule[0]
		elif rule[0] == '#':
			return '#'

	if len(rule) != 0:
		if rule[0] in list(diction.keys()):
			fres = []
			rhs_rules = diction[rule[0]]
			for itr in rhs_rules:
				indivRes = first(itr)
				if type(indivRes) is list:
					for i in indivRes:
						fres.append(i)
				else:
					fres.append(indivRes)
			if '#' not in fres:
				return fres
			else:
				newList = []
				fres.remove('#')
				if len(rule) > 1:
					ansNew = first(rule[1:])
					if ansNew != None:
						if type(ansNew) is list:
							newList = fres + ansNew
						else:
							newList = fres + [ansNew]
					else:
						newList = fres
					return newList
				fres.append('#')
				return fres


# calculation of follow
def follow(nt):
	global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
	
	solset = set()
	if nt == start_symbol:
		solset.add('$')

	for curNT in diction:
		rhs = diction[curNT]
		for subrule in rhs:
			if nt in subrule:
				while nt in subrule:
					index_nt = subrule.index(nt)
					subrule = subrule[index_nt + 1:]
					if len(subrule) != 0:
						res = first(subrule)
						if '#' in res:
							newList = []
							res.remove('#')
							ansNew = follow(curNT)
							if ansNew != None:
								if type(ansNew) is list:
									newList = res + ansNew
								else:
									newList = res + [ansNew]
							else:
								newList = res
							res = newList
					else:
						if nt != curNT:
							res = follow(curNT)
					if res is not None:
						if type(res) is list:
							for g in res:
								solset.add(g)
						else:
							solset.add(res)
	return list(solset)


def createParseTable(statesDict, stateMap, T, NT):
	global separatedRulesList, diction

	rows = list(statesDict.keys())
	cols = T + ['$'] + NT

	Table = []
	for x in range(len(rows)):
		Table.append([''] * len(cols))

	for entry in stateMap:
		state = entry[0]
		symbol = entry[1]
		a = rows.index(state)
		b = cols.index(symbol)
		if symbol in NT:
			Table[a][b] = Table[a][b] + f"{stateMap[entry]} "
		elif symbol in T:
			Table[a][b] = Table[a][b] + f"S{stateMap[entry]} "

	numbered = {}
	key_count = 0
	for rule in separatedRulesList:
		tempRule = copy.deepcopy(rule)
		tempRule[1].remove('.')
		numbered[key_count] = tempRule
		key_count += 1

	addedR = f"{separatedRulesList[0][0]} -> {separatedRulesList[0][1][1]}"
	rules.insert(0, addedR)
	for rule in rules:
		k = rule.split("->")
		k[0] = k[0].strip()
		k[1] = k[1].strip()
		rhs = k[1]
		multirhs = rhs.split('|')
		for i in range(len(multirhs)):
			multirhs[i] = multirhs[i].strip()
			multirhs[i] = multirhs[i].split()
		diction[k[0]] = multirhs

	for stateno in statesDict:
		for rule in statesDict[stateno]:
			if rule[1][-1] == '.':
				temp2 = copy.deepcopy(rule)
				temp2[1].remove('.')
				for key in numbered:
					if numbered[key] == temp2:
						follow_result = follow(rule[0])
						for col in follow_result:
							index = cols.index(col)
							if key == 0:
								Table[stateno][index] = "Accept"
							else:
								Table[stateno][index] = Table[stateno][index] + f"R{key} "

	print("\nSLR(1) Parsing Table:\n")
	table_print = tabulate(Table, headers=cols, showindex=[f'I{i}' for i in rows], tablefmt="fancy_grid")
	print(table_print)


def printResult(rules):
	for rule in rules:
		print(f"{rule[0]} -> {' '.join(rule[1])}")


def printInfo():
	global diction, term_userdef, nonterm_userdef, firsts, follows
	print("\nNon-Terminals: ", nonterm_userdef)
	print("Terminals: ", term_userdef)
	print("\nGrammars:")
	for lhs in diction:
		print(f"{lhs} -> {diction[lhs]}")
	print("\nFirsts: ", firsts)
	print("Follows: ", follows)


# Main input with a new grammar
rules = [
    "E -> T E'",
    "E' -> + T E' | #",
    "T -> F T'",
    "T' -> * F T' | #",
    "F -> ( E ) | id"
]

print("Grammar:")
for rule in rules:
    print(rule)

nonterm_userdef = ['E', 'E\'', 'T', 'T\'', 'F']
term_userdef = ['+', '*', '(', ')', 'id', '#']
start_symbol = nonterm_userdef[0]

separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)

statesDict = {}
stateMap = {}
stateCount = 0
statesDict[0] = findClosure([separatedRulesList[0]], separatedRulesList[0][1][1])
generateStates(statesDict)

firsts = {}
follows = {}
diction = {}

for rule in rules:
	k = rule.split("->")
	k[0] = k[0].strip()
	k[1] = k[1].strip()
	rhs = k[1]
	multirhs = rhs.split('|')
	for i in range(len(multirhs)):
		multirhs[i] = multirhs[i].strip()
		multirhs[i] = multirhs[i].split()
	diction[k[0]] = multirhs

for rule in nonterm_userdef:
	firsts[rule] = first([rule])

for rule in nonterm_userdef:
	follows[rule] = follow(rule)

createParseTable(statesDict, stateMap, term_userdef, nonterm_userdef)
