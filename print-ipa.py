from subprocess import Popen, PIPE
import sys

process = Popen(['espeak', '-q', '--ipa', '"' + ' '.join(sys.argv[1:]) + '"'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout.decode('utf-8').strip())
