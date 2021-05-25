class DFA:
    def __init__(self, states, alphabet, start_state, final_states, transition_funct):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transition_funct = transition_funct
        self.regex = ''
        self.dictStates = {}
        self.setTransitionDict()

    def setTransitionDict(self):
        dict_states = {r: {c: 'ϕ' for c in self.states} for r in self.states}
        for i in self.states:
            for j in self.states:
                indices = [k for k, v in enumerate(self.transition_funct[i]) if v == j]  # get indices of states
                if len(indices) != 0:
                    dict_states[i][j] = '|'.join([str(self.alphabet[v]) for v in indices])
        self.dictStates = dict_states

    def getIntermediateState(self):
        l=[]
        for state in self.states:
            if state not in ([self.start_state] + self.final_states):
                l.append(state)
        return l



    def getBack(self, state):
        l=[]
        for key, value in self.dictStates.items():
            if state in value.keys() and value[state]!='ϕ' and key!=state:
                l.append(key)
        return l


    def getNext(self, state):
        l=[]
        for key, value in self.dictStates[state].items():
            if value!='ϕ' and key != state:
                l.append(key)
        return l




    def toRegEx(self):
        intermediate_states = self.getIntermediateState()
        dict_states = self.dictStates

        for inter in intermediate_states:
            back = self.getBack(inter)
            next = self.getNext(inter)

            for i in back:
                for j in next:

                    if dict_states[inter][j] == 'ϕ':
                        dict_states[i][j] = '|'.join(('(' + dict_states[i][j] + ')'))
                    elif dict_states[i][inter] == 'ϕ':
                        dict_states[i][j] = '|'.join(('(' + dict_states[i][j] + ')'))
                    elif dict_states[i][j] =='ϕ':
                        dict_states[i][j] = ''.join(('(' + dict_states[i][inter] + ')', '(' + dict_states[inter][inter] + ')' + '*', '(' + dict_states[inter][j] + ')'))
                    elif dict_states[inter][inter]== 'ϕ':
                        dict_states[i][j] = '|'.join(('(' + dict_states[i][j] + ')', ''.join(('(' + dict_states[i][inter] + ')', '(' + dict_states[inter][j] + ')'))))
                    else:
                        dict_states[i][j] = '|'.join(('(' + dict_states[i][j] + ')', ''.join(('(' + dict_states[i][
                            inter] + ')', '(' + dict_states[inter][inter] + ')'+'*', '(' + dict_states[inter][j] + ')'))))

            dict_states = {r: {c: v for c, v in val.items() if c != inter} for r, val in dict_states.items() if
                           r != inter}  # remove intermediate  state

        init_loop = dict_states[self.start_state][self.start_state]
        init_to_final = dict_states[self.start_state][self.final_states[0]]
        final_loop=dict_states[self.final_states[0]][
            self.final_states[0]]
        final_to_init = dict_states[self.final_states[0]][self.start_state]
        re='(' + init_loop  + '|'  + '(' + init_to_final + ')' + '(' + final_loop + ')' +'(' + final_to_init + ')' + ')' + '' + '(' + init_to_final + ')'+ '(' + final_loop + ')'+ ''
        if init_loop=='ϕ':
            re = '(' '(' + init_to_final + ')' + '(' + final_loop + ')' +'(' + final_to_init + ')' + ')' + '' + '(' + init_to_final + ')'+ '(' + final_loop + ')'+ ''
        if final_loop=='ϕ':
            re= '(' + init_loop + '|' + '(' + init_to_final + ')'  + '(' + final_to_init + ')' + ')' + '*' + '(' + init_to_final + ')'

        if final_to_init =='ϕ' :
            re = '(' + init_loop + ')' +'' +'(' + init_to_final + ')' + '(' + final_loop + ')'+ ''

        if init_loop=='ϕ' and final_to_init=='ϕ':
            re =  '(' + init_to_final + ')' + '(' + final_loop + ')'+ '*'

        if init_loop == 'ϕ' and final_to_init == 'ϕ' and final_loop=='ϕ':
            re = '(' + init_to_final + ')'

        if init_to_final == 'ϕ':
            re = '(' + init_loop + ')' + '*'

        if init_to_final == 'ϕ' and  init_loop=='ϕ':
            re = ''

        return re




number_states=int(input('How many states does the DFA have?: '))
states=[]
for i in range(number_states):
    state=input()
    states.append(state)

number_alphabet=int(input('How many elements do you have in the alphabet? '))
alphabet=[]
for j in range(number_alphabet):
    alph=input()
    alphabet.append(alph)

start_state=input('Give the starting state: ')
number_f_states=int(input('How many final states are there?'))
final_states=[]
print('Give the final states: ')
for k in range(number_f_states):
    fstate=input()
    final_states.append(fstate)

'''
states = input('States in your DFA : ')
states = states.split() #in loc de split sa le citim pe rand cu un k
alphabet = input('Alphabet : ')
alphabet = alphabet.split()  #in loc de split sa le citim pe rand cu un k
start_state = input('Initial state : ')
final_states = input('Final states : ')
final_states = final_states.split() #in loc de split sa le citesti pe rand cu un k
'''
print('Transition table : ')
transition_table = [list(map(str, input().split())) for _ in range(len(states))]
transition_funct = dict(zip(states, transition_table))
print('Transition funct : ', transition_funct)
r = ''
for f in final_states:
    dfa = DFA(states, alphabet, start_state, [f], transition_funct)
    r += '|' + dfa.toRegEx()
    print('States Dictionary: ', dfa.dictStates)


r=r[1:]
print("Regular Expression : ", r)