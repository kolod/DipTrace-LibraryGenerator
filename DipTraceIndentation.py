#!/usr/bin/python3
#-*- coding: utf-8 -*-

from reHelper import getTag

def DipTraceIndentation(library:str) -> str:
	result = ''

	exceptions = [
		'Source',
		'Shape',
	]

	tag = ''
	tags = []

	for line in library.splitlines():

		line = line.strip()
		identation = len(tags)

		if line == '':
			continue

		# End of file
		elif line == '()':
			tags.clear()
			identation = 0

		elif line == ')':
			if len(tags):
				if tags[-1] in exceptions:
					tags.pop()
					identation -= 1
			tag = tags.pop()
			identation -= 1

		elif line.startswith('('):
			tag = getTag(line)

			if line.endswith(')'):
				if tag in exceptions:
					if len(tags):
						if tag != tags[-1]:
							tags.append(tag)
						else:
							identation -= 1
					else:
						tags.append(tag)

			else:
				tags.append(tag)

		result += '  ' * identation + line + '\n'
	return result


if __name__ == "__main__":
	with open('test.asc', 'r', encoding="utf-8") as input:
		with open('test_new.asc', 'w', encoding="utf-8") as output:
			output.write(DipTraceIndentation(input.read()))