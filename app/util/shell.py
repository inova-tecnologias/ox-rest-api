from cmd import Cmd
from ..beta.soap.ox import (
    credentials, Context, User
)


class MyPrompt(Cmd):
    prompt = 'oxcli> '
    intro = "Welcome! Type ? to list commands"
 
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
 
    def do_get_contexts(self, inp):
        [
            print(c.id, c.name) for c in 
            Context.service.listAll(auth=credentials)
        ]

    def help_get_contexts(self):
        print("List OxCloud Contexts and IDs.")
    
    def do_get_accounts(self, inp):
        ctxs = Context.service.listAll(auth=credentials)
        users = []
        for c in ctxs:
            print("Getting accounts from %s, id:%i" %(c.name, c.id))
            users = User.service.listAll(auth=credentials, ctx=c)
            [print(u.id, u.name) for u in User.service.getMultipleData(
                auth=credentials,
                ctx=c,
                users=users)]
            print()

    def help_leo(self):
        print("esse comando printa leozinho")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))
 
    do_EOF = do_exit
    help_EOF = help_exit
 
