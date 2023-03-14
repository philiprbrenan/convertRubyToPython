#-------------------------------------------------------------------------------
# Convert a ruby file to python
#-------------------------------------------------------------------------------
import os, re, sys

def convertRubyToPython(ruby) :                                                 # Convert an attay of ruby to an array of python
  python = []                                                                   # The resulting python

  for lineI in range(len(ruby)):                                                # Spaces to tabs
    l = ruby[lineI]
    m = re.search(r"(\A\s+)(\S.*)\Z", l)
    if m:
      l = "\t" * round(len(m[1]) / 2) + m[2]

    m = re.search(r"(\A.*)\[:(\w+)\](.*\Z)", l)                                 # Hash look ups
    if m:
      l = m[1]+'["' + m[2] + '"]' + m[3]

    if re.match(r"\A\s*(def|if|else|elsif)\s+", l) :                            # Add colon at end of structure statements
      l += ":"

    l = re.sub(r"\belsif\b",     "elif",   l)                                   # Elsif

    l = re.sub(r"\bupcase\b",   "upper()", l)                                   # upcase   to upper()
    l = re.sub(r"\bdowncase\b", "lower()", l)                                   # downcase to lower()
    l = re.sub(r"\.push\b",     ".append", l)                                   # .push to .append
    l = re.sub(r"\bputs\b",     "print",   l)                                   # puts     to print
    l = re.sub(r"\bnil\b",      "None",    l)                                   # nil to None
    l = re.sub(r"\bfalse\b",    "False",   l)                                   # false to False
    l = re.sub(r"\btrue\b",     "True",    l)                                   # true  to false
    l = re.sub(r"#\{",          "{",       l)                                   # Format string content
    l = re.sub(r'(\A[^"]*)"',  r'\1f"',    l)                                   # Format string

    if re.match("\A\s*end\s*\Z", l) :                                           # Remove end statements
      l = '';

    python.append(l)                                                            # After modifications

  return python                                                                 # Array of python

if len(sys.argv) > 1:                                                           # Read file supplied as argument 1 on the command line
  f = sys.argv[1]
  assert re.search(r"\.rb\Z", f), f"Ruby file required, not ={f}="
  with open(f, "r") as i:                                                       # Read file
    ruby = i.readlines()

  for lineI in range(len(ruby)):                                                # Spaces to tabs
     ruby[lineI] = re.sub(os.linesep + r'\Z', '', ruby[lineI])

  python = convertRubyToPython(ruby)                                            # Convert

  if True:                                                                      # Write to corresponding python file
    F = re.sub("\.rb\Z", ".py", f)
    with open(F, "w") as o:
      for p in python:
        print(p, file=o)

else:                                                                           # Test conversion
  ruby = """
def aaa(a)
  if (a[:aa] == b)
    puts b.upcase
  elsif (a[:bb] == b)
    puts b.downcase, true, false, nil
  else
    puts("#{a} #{b}")
  end
""".split("\n");

  python = convertRubyToPython(ruby)                                            # Convert

  for p in python:
    print(p)
