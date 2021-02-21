#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from DipTrace.reHelper import getTag


def DipTraceIndentation(library: str) -> str:
    result = ''
    tags = []

    for line in library.splitlines():

        line = line.strip()
        identation = len(tags)

        # Skip empty lines
        if line == '':
            continue

        # End of file
        elif line == '()':
            tags.clear()
            identation = 0

        # Enter subobject
        elif line.startswith('('):
            tag = getTag(line)

            if not line.endswith(')'):
                tags.append(tag)

            elif tag == 'Source':
                tags.append(tag)

            elif tag == 'pt':
                if len(tags) > 1 and tags[-1] == 'PadMask_TopSegments':
                    identation += 1
                if len(tags) > 1 and tags[-1] == 'PadMask_BotSegments':
                    identation += 1

            # Exception for Shape object in pattern
            elif tag == 'Shape':
                if tags[-1] == 'Shape' and 'Pattern' in tags:
                    identation -= 1
                elif tags[-1] == 'Shapes':
                    tags.append(tag)

        # Leave subobject
        elif line == ')':

            if len(tags) == 0:
                print('Warning unexpected ")"')
                result += '  ' * identation + line + '\n'
                continue

            if tags[-1] == 'Shape' and 'Pattern' in tags:
                tags.pop()
                identation -= 1

            tag = tags.pop()
            identation -= 1

        # Do indentation
        result += '  ' * identation + line + '\n'

    return result


if __name__ == "__main__":
    pass
