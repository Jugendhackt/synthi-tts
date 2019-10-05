from subprocess import Popen, PIPE
import sys
import fileinput

text = ""
if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = fileinput.input()[0].strip()


process = Popen(['espeak', '-q', '--ipa', '"' + text + '"'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
ipa = stdout.decode('utf-8').strip()
print(ipa)
print(ipa, file=sys.stderr)

