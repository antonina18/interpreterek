import subprocess

class Command:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def with_arg(self, arg):
        return Command(self.name, self.args + [arg])



    def evaluate(self, stdin, stdout, stderr):
        return subprocess.Popen([self.name] + self.args, stdin=stdin, stdout=stdout, stderr=stderr)




class Pipe:
    def __init__(self, cmd1, cmd2):
        self.cmd1 = cmd1
        self.cmd2 = cmd2

    def evaluate(self, stdin, stdout, stderr):
        input = self.cmd1.evaluate(stdin, subprocess.PIPE, stderr)
        output = self.cmd2.evaluate(input.stdout, stdout, stderr)
        return output

class RedirectOutToFile:
    def __init__(self, cmd, filename):
        self.cmd = cmd
        self.filename = filename

    def evaluate(self, stdin, stdout, stderr):
        file = open(self.filename, "wa")
        return self.cmd.evaluate(stdin, file, stderr)

class TruncateFile:
    def __init__(self, cmd, filename):
        self.cmd = cmd
        self.filename = filename

    def evaluate(self, stdin, stdout, stderr):
        file = open(self.filename, "w")
        return self.cmd.evaluate(stdin, file, stderr)



class RedirectInFromFile:
    def __init__(self, cmd, filename):
        self.cmd = cmd
        self.filename = filename

    def evaluate(self, stdin, stdout, stderr):
        file = open(self.filename, "r")
        return self.cmd.evaluate(file, stdout, stderr)

#
# class CommandList:
#     def __init__(self, cmd1, cmd2):
#         self.cmd1 = cmd1
#         self.cmd2 = cmd2
#
#     def evaluate(self, stdin, stdout, stderr):
#         self.cmd1.evaluate(stdin, stdout, stderr).wait()
#         return self.cmd2.evaluate(stdin, stdout, stderr)