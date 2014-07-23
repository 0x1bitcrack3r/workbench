
''' HelpCLI worker '''

from colorama import Fore, Style

class HelpCLI(object):
    ''' This worker does CLI formatting and coloring for any help object '''
    dependencies = ['help']

    def execute(self, input_data):
        ''' Do CLI formatting and coloring based on the type_tag '''
        input_data = input_data['help']
        type_tag = input_data['type_tag']

        # Standard help text
        if type_tag == 'help':
            output = '\n%s%s%s%s%s' % (Style.BRIGHT, Fore.BLUE, input_data['help'], Fore.RESET, Style.RESET_ALL)

        # Worker
        elif type_tag == 'worker':
            output = '\n%s%s%s%s' % (Style.BRIGHT, Fore.YELLOW, input_data['name'], Style.RESET_ALL)
            output += '\n %sInput: %s%s%s' % (Fore.BLUE, Fore.GREEN, input_data['dependencies'], Fore.RESET)
            output += '\n%s%s' % (Fore.GREEN, input_data['docstring'])

        # Command
        elif type_tag == 'command':
            output = '\n%s%s%s%s%s%s' % (Style.BRIGHT, Fore.YELLOW, input_data['command'],
                                             Style.RESET_ALL, Fore.BLUE, input_data['sig'])
            output += '%s\n%s%s' % (Fore.GREEN, input_data['docstring'], Fore.RESET)

        # WTF: Alert on unknown type_tag and return a string of the input_data
        else:
            print 'Alert: help_cli worker received malformed object: %s' % str(input_data)
            output = '\n%s%s%s' % (Fore.RED, str(input_data), Fore.RESET)

        # Return the formatted and colored help
        return {'help': output}

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' help_cli.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    input_data1 = workbench.work_request('help', 'workbench')
    input_data2 = workbench.work_request('help', 'meta')
    input_data3 = workbench.work_request('help', 'store_sample')

    # Execute the worker (unit test)
    worker = HelpCLI()
    output = worker.execute(input_data1)
    print '\n<<< Unit Test >>>'
    print output['help']
    output = worker.execute(input_data2)
    print '\n<<< Unit Test >>>'
    print output['help']
    output = worker.execute(input_data3)
    print '\n<<< Unit Test >>>'
    print output['help']      

    # Execute the worker (server test)
    output = workbench.work_request('help_cli', 'meta')
    print '\n<<< Server Test >>>'
    print output['help_cli']['help']

if __name__ == "__main__":
    test()
