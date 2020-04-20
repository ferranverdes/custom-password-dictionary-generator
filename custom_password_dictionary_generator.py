#!/usr/bin/python3.7

import sys
import copy

COMBINATION_OPENER = '['
COMBINATION_CLOSER = ']'

class Word:
	"""
	Represents a word and its combinations that will be used in order to create
	potential passwords.
	"""

	def __init__(self, raw_word):
		self.raw_word = raw_word
		self.combinations = []

	def create_combinations(self):
		"""Generates all defined combinations for a word."""
		self.combinations = get_combinations_to_right_from_a_combination_list(
						parse_raw_word_to_combination_list(self.raw_word))

	def __repr__(self):
		"""String representation for an instance."""
		return self.raw_word

def get_substr_between_delimiters(str, opener_del, closer_del):
	"""
	Given two delimiters it returns the substring between them plus the position
	in the string for both.
	Example:

	Input:
		- str: 'hi[hello]there'
		- opener_del: '['
		- closer_del: ']'

	Output:
		('hello', 2, 8)
	"""
	start = str.find(opener_del)
	end = str.find(closer_del)
	return str[start+1:end], start, end

def find_next_combination(str):
	"""
	Locates the next substring contained by the specified delimiters and returns
	the same as the get_substr_between_delimiters function.
	"""
	return get_substr_between_delimiters(str, COMBINATION_OPENER, COMBINATION_CLOSER)

def is_first_char_a_combination_starter(str):
	"""Checks if the first character is an opener delimiter."""
	return str[0] == COMBINATION_OPENER

def parse_raw_word_to_combination_list(raw_word):
	"""
	Creates a list from a plain word that can be used to create all the combinations
	it contains.
	Example:

	Input:
		- raw_word: 'H[iI1]'
	Output:
		[['H'], ['i', 'I', '1']]
	"""

	if not raw_word:
		return []
	elif is_first_char_a_combination_starter(raw_word):
		combination, start, end = find_next_combination(raw_word)
		return [list(combination)] + parse_raw_word_to_combination_list(raw_word[end+1:])
	else:
		return [list(raw_word[0])] + parse_raw_word_to_combination_list(raw_word[1:])

def get_combinations_to_right_from_a_combination_list(combination_list):
	"""
	Creates a list containing all possible combinations from a combination list.
	Example:

	Input:
		- combination_list: [['H'], ['i', 'I', '1']]
	Output:
		['Hi', 'HI', 'H1']
	"""

	if len(combination_list) == 1:
		return combination_list.pop(0)
	else:
		first_part = combination_list.pop(0)
		rest = get_combinations_to_right_from_a_combination_list(combination_list)
		return [character + characters for character in first_part for characters in rest]

def get_combinations_to_right_between_element_and_list(elem, list, index=0):
	"""
	Given a single element, it provides all possible combinations using all other
	elements contained in the list only once or none.
	Example:

	Input:
		- elem: ['1']
		- list: ['2', '3']
	Output:
		[['1', '2'], ['1', '2', '3'], ['1', '3'], ['1', '3', '2']]
	"""
	if index == len(list):
		return []
	else:
		rest = copy.deepcopy(list)
		item = rest.pop(index)
		combination = elem + [item]
		return [combination] + \
			get_combinations_to_right_between_element_and_list(combination, rest) + \
			get_combinations_to_right_between_element_and_list(elem, list, index+1)

def get_all_combinations_from_list(list, index=0):
	"""
	Given a list, it provides all combinations using all elements contained only
	once or none.
	Example:

	Input:
		- list: ['1', '2', '3']
	Output:
		[['1'], ['1', '2'], ['1', '2', '3'], ['1', '3'], ['1', '3', '2'],
		['2'], ['2', '1'], ['2', '1', '3'], ['2', '3'], ['2', '3', '1'],
		['3'], ['3', '1'], ['3', '1', '2'], ['3', '2'], ['3', '2', '1']]
	"""
	if index == len(list):
		return []
	else:
		rest = copy.deepcopy(list)
		item = rest.pop(index)
		return [[item]] + \
			get_combinations_to_right_between_element_and_list([item], rest) + \
			get_all_combinations_from_list(list, index+1)

def get_combinations_to_right_between_words(word_list, acc_combinations=[], index=0):
	"""
	Given a Word list, it combines to right using their combinations attribute
	instead of the Word instance itself.
	Example:

	Input:
		- word_list: [h[i1], y[o0]u]
	Output:
		['hiyou', 'hiy0u', 'h1you', 'h1y0u']
	"""
	if index == len(word_list):
		return acc_combinations
	elif index == 0:
		word_combinations=word_list[0].combinations
		return get_combinations_to_right_between_words(word_list, word_combinations, index+1)
	else:
		word = word_list[index]
		new_combinations = []

		for acc_combination in acc_combinations:
			for word_combination in word.combinations:
				new_combinations.append(acc_combination + word_combination)

		return get_combinations_to_right_between_words(word_list, new_combinations, index+1)

def get_words_combinations(combinations, index=0):
	"""
	Given a Word combination list, it provides the combinations to right for each
	combination contained in the list.
	Example:

	Input:
		- combinations: [[h[i1]], [h[i1], y[o0]u], [y[o0]u], [y[o0]u, h[i1]]]
	Output:
		['hi', 'h1', 'hiyou', 'hiy0u', 'h1you', 'h1y0u',
		'you', 'y0u', 'youhi', 'youh1', 'y0uhi', 'y0uh1']
	"""
	if index == len(combinations):
		return []
	else:
		word_combinations = get_combinations_to_right_between_words(combinations[index])
		next_word_combinations = get_words_combinations(combinations, index+1)
		return word_combinations + next_word_combinations

def main():
	word_list = [Word(param) for param in sys.argv[1:]]
	[word.create_combinations() for word in word_list]
	word_list_combined = get_all_combinations_from_list(word_list)
	combinations = get_words_combinations(word_list_combined)
	[print(combination) for combination in combinations]

if __name__ == "__main__":
	main()
