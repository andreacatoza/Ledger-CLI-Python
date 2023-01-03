from dataclasses import dataclass,field,asdict
from typing import List
import pandas as pd
import argparse
data=[]

#READ THE FILLES:
def readFile(filename):
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith(';'):
                    continue
                if line.startswith('!include'):
                    readFile(line.split()[1]) 
                    continue
                data.append(line)
#MUST HAVE:
#Support for commands  register, balance and print 
#Support flags --sort, --price-db, --file 
#Add the arguments and parses them
parser = argparse.ArgumentParser(prog = 'Ledger',
                                formatter_class = argparse.RawDescriptionHelpFormatter,
                                description= "This is Ledger, the accounting tool that will heelp you to keep your finances on track")

parser.add_argument('-f', '--file', 
                    help='Input a file to read',
                    required=True)

#THE REQUIRED COMANDS STARTS HERE
#sort command
parser.add_argument('-s', '--sort',
                    help='Sort by amount, comment or date')

#prices database command
parser.add_argument('--price-db', nargs=2,
                    help='Load a prices database for your brokerage account')

#optional commands
parser.add_argument("command",
                    choices=['balance', 'bal', 'register', 'reg', 'print'],
                    help='Select a command to execute')

#Parse the arguments given as inputs 
args = parser.parse_args()

#Once the program has read the lines, it will transform the inputs as dataclasses and proced
# to do the accounting part 
@dataclass
class Transaction:
    date: str = "00/00/00"
    description: str = ""
    account: int = 0
    currency: str = ""
    amount: float = 0.0
#Data for some tests
#Transaction("01/15/20","cash", 2931,"dolar", 1293.00)
#print(a)

@dataclass
class GeneralLedger:
    transactions: List[Transaction] = field(default_factory=list)
    #this function transform the list in libraries and here you have the aritmetcs required.
    def trial_balance(self):
        df = pd.DataFrame([asdict(txn) for txn in gl.transactions])
        return df.pivot_table(index=["description","account","currency"],
        values="amount",
        aggfunc=sum).reset_index()

gl = GeneralLedger(
    [Transaction("01/15/20","cash", 2931,"dolar", 1293.00),Transaction("01/15/20","cash", 2931,"dolar", -1293.00),Transaction("03/12/21","debit", 3949,"dolar", 100.00)]

)

b=gl.trial_balance()
#print(b)
