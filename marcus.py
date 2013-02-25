from grammar import load_grammar

from nltk.tree import *
from nltk.draw import tree

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
		_s_ += '%s(%s) | ' % (node.root, node.pos)
	
	print _s_[:-2]

def print_buffer(b):
	print('Buffer: %s' % " | ".join([str(x) for x in b]))

def trace(s, to, G):
	print("Tracing %s to %s" % (s,to))

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
	'''Filter a grammar for rules which lead to s'''
	#print("Filtering rules")
	for root, rules in G.iteritems():
		for rule in rules:
			print("%s in %s" % (s, rule))
			if s in rule:
				return root

	return None

class Node:
	def __init__(self, root, pos, childs=[]):
		self.root = root
		self.pos = pos
		self.node = Tree(self.root, childs)

	def __str__(self):
		return self.root

def marcus(w, G, k=3):
	w = w.split(' ')

	stack = []
	buf = w[:3]
	w_i = 0

	stack.append( Node(G['__root__'], 0) )
	
	while True:
		print('---------------------------------------')
		print_stack(stack)
		print_buffer(buf)
		
		active = stack.pop()
		position = active.pos
		new_pos = active.pos

		print('Active: %s\n' % active.root)
		
		if active.root in G: # Nonterminal
			rules = G[active.root]
			
			if rules == []:
				print("No rules found!")
				return None

			# { this can probably be optimized into one or two lines
			buf_0 = buf[0]
			if buf_0 in __TERMINALS__:
				buf_0 = Node(__TERMINALS__[buf_0], 0, [buf_0])
				buf[0] = buf_0
			# }

			rule_found = False	
			for rule in rules:

				# check if we can possibly be inside this rule
				# and check if the next buffer node matches the expected node from the rule
				
				if active.pos < len(rule) and buf_0.root == rule[active.pos]:
					new_pos += 1
										
					if new_pos >= len(rule):
						# The rule is finished now, we can either close it
						# or keep it open to wait for new tokens.
					
						if len(buf) < 2 or trace(__TERMINALS__[buf[1]], active.root, G) == False:
							# this note can be closed and put into the buffer
							active.node.append(buf[0].node)
							buf[0] = active
						else:
							active.node.append(buf[0].node)

							# we can't close this node yet
							w_i += 1
							buf = w[w_i:w_i+3]
							
							# return the active node to the stack, since it has to stay open
							active.pos = new_pos
							stack.append(active)
							
							# add a new node to look for
							stack.append( Node(filter_rules(__TERMINALS__[buf[0]], G), 0) )
						
					else:
						# Take the node at buf[0] and place it onto the active node
						active.node.append(buf[0].node)

						# ...and update the buffer
						w_i += 1
						buf = w[w_i:w_i+3]

						# return the updated active node to the stack, 
						active.pos = new_pos
						stack.append(active)

					rule_found = True
					break		

			if rule_found == False:
				# No unambiguous rule found, we need to generate new expected nodes
				# return the active node to the stack
				stack.append(active)
				
				# wait for the next possible rule to match
				rule = rules[0]
				print("%s (%s)" % (" ".join(rule), position))
				stack.append( Node(rule[position], 0) )

			#print("Found rule %s -> %s" % (active.root, " ".join(rule)))

		if len(stack) == 0:
			if len(buf) == 1:
				return buf[0].node # this node should by now be the root of the whole parse tree
			return None

		#raw_input()

	print("No parse found!")
	return None

def main():
	print("------------ Parser: MARCUS ------------\n")
	grammar_path = 'grammars/marcus.gr' #raw_input('Grammar file: ')
	G = load_grammar(grammar_path, False)

	#print(trace('DET', 'VP', G))
	#print(trace('N', 'S', G))

	while True:
		w = raw_input('\nInput: ')
		parse_tree = marcus(w, G)

		if parse_tree is None:
			print("[FALSE]: w not in L(G)")
		else:
			print("[TRUE]: w is in L(G)")
			parse_tree.draw()

if __name__ == '__main__':
	main()