import difflib
import os
import re
import vim
import subprocess

from vimpy import Command, variables

class ClangFormatEx(Command):
  range = True
  bang = True

  def __init__(self):
    Command.__init__(self)

  def run(self, line1=0, line2=0):
    buf = vim.current.buffer
    text = '\n'.join(buf)
    print line1, line2

    cmd = [
      'clang-format',
      '-lines', str(line1) + ':' + str(line2),
      '-style=' + os.getenv('CLANG_FORMAT_FILE', 'Chromium'),
    ]
    p = subprocess.Popen(cmd,
      stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input=text)

    lines = stdout.split('\n')
    sequence = difflib.SequenceMatcher(None, vim.current.buffer, lines)

    for op in reversed(sequence.get_opcodes()):
      if op[0] is not 'equal':
        vim.current.buffer[op[1]:op[2]] = lines[op[3]:op[4]]

