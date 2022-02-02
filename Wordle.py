import random as r

WORD_LENGTH = 5
GUESS_THRESHOLD = 1 	# how many possibilities before it just guesses
RANDOM_START = False

def index_letter(letter):
	return ord(letter.lower()) - ord('a')

def avg(num_array):
	return sum(num_array) / len(num_array)

def std_dev(num_array, calctype='sample'):
	assert calctype in ('sample', 'population')
	return (sum([abs(x-avg(num_array))**2 for x in num_array])/(len(num_array) - (1 if (calctype == 'sample') else 0)))**0.5

def weave_correct(old, new):
	out = []
	for old_chr, new_chr in zip(old, new):
		assert old_chr == -1 or new_chr == -1 or old_chr == new_chr
		if old_chr != -1:
			out.append(old_chr)
		elif new_chr != -1:
			out.append(new_chr)
		else:
			out.append(-1)
	assert len(out) == WORD_LENGTH
	return out


def build_wordlist(src_filename):
	wordlist = []

	with open(src_filename, 'r') as file:
		for line in file:
			# includes newline
			if len(line) == WORD_LENGTH + 1:
				wordlist.append(line[:-1].lower())
	return wordlist

def build_letterdist(wordlist):
	# this is good, but not perfect
	# general improvement looks like maximizing the number of words a word knocks out, which will be different from the letter
	# we need to figure out how to do this in less than x^2 time? (ie not checking every word to see how many it knocks out)
	# x^2 is long, but only 73 million brute force (with scrabble dict)
	letterdist=[0]*26

	for word in wordlist:
		for letter in word:
			letterdist[index_letter(letter)] += 1

	return letterdist

	# for x in range(26):
	# 	print(f"{chr(ord('a') + x)}: {letterdist[x]}")

def build_wordscores(wordlist, letterdist, func=None):
	avg_letterweight = avg(letterdist)
	std_dev_letterweight = std_dev(letterdist, calctype='population')

	wordscores = []
	for word in wordlist:
		# print('test')
		current_score = 0
		used_letters = [False]*26
		for letter in word:
			if not used_letters[index_letter(letter)]:
				if func == None:
					current_score += letterdist[index_letter(letter)]
				else:
					current_score += letterdist[index_letter(letter)] * func(letter)
					# print(f'{func(letter)} ', end='')

				used_letters[index_letter(letter)] = True
		wordscores.append(current_score)

		# print((avg_letterweight + std_dev_letterweight * (2 * len(wordlist) / 8851)) * 5)
		# if (avg_letterweight + std_dev_letterweight * 2) * 5 < current_score:
			# print(f"\t{word}: {current_score}")
			# pass
	return wordscores

def process_feedback(wordlist, guess):
	# X Y G for not contained, contained but wrong place, right letter right place
	assert guess is not None
	while (len(feedback := input(f"{guess}: ")) != WORD_LENGTH):
		pass

	contained = set()
	not_contained = set()
	correct = [-1]*WORD_LENGTH

	index = 0
	for clue in feedback:
		assert clue.lower() in ('x', 'y', 'g'), "bad feedback given"
		if clue.lower() == 'x':
			not_contained.add(guess[index])
		if clue.lower() in ('y', 'g'):
			contained.add(guess[index])
		if clue.lower() == 'g':
			correct[index] = guess[index]
		index += 1
	# print(not_contained)
	return (contained, not_contained, correct)

def build_attempt_eliminate(wordlist, effective_letterdist, contained, not_contained):
	# this will score words based on the number of words within 
	special_wordscores = build_wordscores(wordlist, effective_letterdist, lambda x: 1 if (x not in contained and x not in not_contained) else 0)

	return build_attempt_guess(wordlist, special_wordscores)



def build_attempt_guess(wordlist, wordscores):
	return wordlist[wordscores.index(max(wordscores))]


def eliminate(wordlist, contained, not_contained, correct):
	new_wordlist = []
	elim_count = 0

	for word in wordlist:
		index = 0
		c_contains = dict.fromkeys(contained, False)
		eliminate_flag = False
		for letter in word:
			if letter in not_contained:
				eliminate_flag = True
			if correct[index] != -1 and letter != correct[index]:
				eliminate_flag = True
			if letter in contained:
				c_contains[letter] = True
			index += 1

		if False in c_contains.values():
			eliminate_flag = True

		if eliminate_flag:
			elim_count += 1
		else:
			new_wordlist.append(word)
			# print(f"could be: {word}")

	# print(f"eliminated: {elim_count} ({len(new_wordlist)} remaining)")
	print(f"{len(new_wordlist)} remaining")
	return new_wordlist




def main():
	wordlist = build_wordlist('ospd.txt')
	effective_wordlist = wordlist[:]

	if RANDOM_START:
		print('random starting word:')
		contained, not_contained, correct = process_feedback(wordlist, r.choice(wordlist))
	else:
		contained = set()
		not_contained = set()
		correct = [-1]*WORD_LENGTH

	
	phase = 'eliminate'

	while True:
		# once there is very few possibilites, just guess
		if len(effective_wordlist := eliminate(effective_wordlist, contained, not_contained, correct)) <= GUESS_THRESHOLD:
			phase = 'guess'
			wordlist = effective_wordlist

		letterdist = build_letterdist(wordlist)
		wordscores = build_wordscores(wordlist, letterdist)

		if phase == 'eliminate':
			print('attempting to eliminate')

			effective_letterdist = build_letterdist(effective_wordlist)
			# print(type(not_contained))
			guess = build_attempt_eliminate(wordlist, effective_letterdist, contained, not_contained)
		elif phase == 'guess':
			print('attempting to guess')
			guess = build_attempt_guess(wordlist, wordscores)

		new_contained, new_not_contained, new_correct = process_feedback(wordlist, guess)
		contained |= new_contained
		not_contained |= new_not_contained
		correct = weave_correct(correct, new_correct)
		# print(contained)
		# print(not_contained)
		# print(correct)


		





if __name__ == '__main__':
	main()