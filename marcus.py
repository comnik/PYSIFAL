import grammar

__TERMINALS__ = {
	'Bernd': 'N',
	'Marcus': 'N',
	'Noam': 'N',
	'Apfel': 'N',
	'Paper': 'N',
	'Ball': 'N',
	'isst': 'V',
	'schneidet': 'V',
	'wirft': 'V',
	'schreibt': 'V',
	'den': 'DET',
	'einen': 'DET',
	'ein': 'DET',
	'der': 'P',
	'die': 'P',
	'das': 'P'
}

def print_stack(s):
	_s_ = 'Stack: '
	for node in s:
		_s_ += '%s(%s) | ' % node
	
	print _s_[:-2]

def match_buffer(rules, active_node, position, G, buffer):
	'''Matches the buffer against a set of rules.'''
	#reduced = [rule for rule in rules if position < len(rule)]
	#if reduced != []:
	#	rules = reduced

	buf_0 = buffer[0]
	reduced = [rule for rule in rules if position < len(rule) and rule[position] == __TERMINALS__.get(buf_0, buf_0)]

	if len(reduced) == 1:
		return reduced[0]
	else:
		return None

def trace(s, to, G):
	#print("Tracing %s to %s" % (s,to))

	if s == to:
		return True

	for root, rules in G.iteritems():
		for rule in rules:
			if s in rule:
				#print("%s -> %s" % (root, rule))
				if trace(root, to, G) == True:
					return True
				#print('-----')

	return False

def filter_rules(s, G):
	'''Filter a set of rules for those which lead to s'''
	print("Filtering rules")
	for root, rules in G.iteritems():
		for rule in rules:
			print("%s in %s" % (s, rule))
			if s in rule:
				return root

	return None

def marcus(w, G, k=3):
	w = w.split(' ')

	stack = []
	buf = w[:3]
	w_i = 0

	stack.append((G['__root__'],0))

	while True:
		print('---------------------------------------')
		print_stack(stack)
		print('Buffer: '+' | '.join(buf))
		active = stack.pop()
		active_node = active[0]
		position = active[1]
		new_pos = position
		print('Active: %s\n' % active_node)

		if active_node in G: # Nonterminal
			rules = G[active_node]
			
			if rules == []:
				return False

			buf_0 = __TERMINALS__.get(buf[0], buf[0])
			buf[0] = buf_0
			
			rule_found = False	
			for rule in rules:
			#	print(rule)
			#	print(position)
				if position < len(rule) and buf_0 == rule[position]:
					#print("%s == %s" % (buf_0, rule[position]))
					#print("Matching Terminal %s" % buf_0)
					new_pos += 1
					if new_pos >= len(rule):
						if len(buf) < 2 or trace(__TERMINALS__.get(buf[1],buf[1]), active_node, G) == False:
							# this note can be closed and put into the buffer
							buf[0] = active_node
						else:
							# we can't close this node yet
							w_i += 1
							buf = w[w_i:w_i+3]
							stack.append( (active_node, new_pos) )
							stack.append( (filter_rules(__TERMINALS__.get(buf[0], buf[0]), G), 0) )
						
					else:
						w_i += 1
						buf = w[w_i:w_i+3]
						stack.append( (active_node, new_pos) )		
					
					rule_found = True
					break		

			if rule_found == False:
#				print("No Matching Terminal")
				rule = rules[0]
				stack.append( (active_node, position) )
				stack.append( (rule[position], 0) )

			#print("Found rule %s -> %s" % (active_node, " ".join(rule)))

		if len(stack) == 0:
			if len(buf) == 1:
				return True
			return False

		#raw_input()

	return False

def main():
	print("------------ Parser: MARCUS ------------\n")
	grammar_path = 'grammars/marcus.gr' #raw_input('Grammar file: ')
	G = grammar.load(grammar_path, False)

	#print(trace('DET', 'VP', G))
	#print(trace('N', 'S', G))

	while True:
		w = raw_input('\nInput: ')
		if marcus(w, G):
			print("[TRUE]: w is in L(G)")
		else:
			print("[FALSE]: w not in L(G)")

if __name__ == '__main__':
	main()