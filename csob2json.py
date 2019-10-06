import re
import json

# Describes what kind a transaction can we extract.
# A transaction must have a unique 'name' 
# and a regex, which identifies the first line of transaction
transactionTypes = [
                {
                    "name": "cardPayment",
                    "firstLineRegex": r"^Transakcia"
                },
                {
                    "name": "outPayment",
                    "firstLineRegex": r"^Odoslan"
                },
                {
                    "name": "inPayment",
                    "firstLineRegex": r"^Prijat"
                }
            ]

def detectTransactionType(firstLine):
    """Detects if current string line is the beginning of one of transaction types according to
    'firstLineRegex"""
    for i in range(len(transactionTypes)):
        if re.match(transactionTypes[i]["firstLineRegex"], firstLine):
            return i
    return None

def extractRegexBetweenLines(regex, lines):
    """Extracts a single property, written in lines, specified by regex"""
    for line in lines:
        obj = re.search(regex, line)
        if obj != None:
            return obj.group(1)
    return "Not found"

def processParsedTransaction(transaction):
    """Parse semantics from transaction lines"""
    if transaction["type"] == "cardPayment":
        transaction["amount"] = extractRegexBetweenLines(r"^Suma: ([0-9.]+ [A-Z]+)",transaction["lines"]);
        transaction["place"] = extractRegexBetweenLines(r"^Miesto: (.*)",transaction["lines"]);
    return transaction
     

def parseLinesToTransactions(linesArray):
    """Group lines belonging to the same transaction"""
    transactions = []
    remainingLines = linesArray
    currentTransaction = { "lines": []}
    # While we still have lines to parse
    for line in linesArray:
        typeID = detectTransactionType(line)
        if typeID != None:
            transactions.append(currentTransaction)
            currentTransaction = { "type": transactionTypes[typeID]["name"], "lines": []}
        currentTransaction["lines"].append(line)

    return transactions[1:]

class StatefullCSOBFilter:
    """Filter only lines, belonging to transactions"""
    shouldSkip = True 
    
    @staticmethod
    def filterMethod(line):
        """Lines are kept in case a transaction lines started and empty line wasn't reached """
        if not StatefullCSOBFilter.shouldSkip and re.match(r"^\s*$", line) != None:
            StatefullCSOBFilter.shouldSkip = True
        elif StatefullCSOBFilter.shouldSkip and detectTransactionType(line) != None:
            StatefullCSOBFilter.shouldSkip = False
        return not StatefullCSOBFilter.shouldSkip


if __name__ == "__main__":
    with open("output","r") as f:
        # Filter out all lines, not containing transaction info
        content = list(filter(StatefullCSOBFilter.filterMethod, f))
        # Group lines into transactions
        parsedTransaction = parseLinesToTransactions(content)
        # Extract semantic information from lines
        processedTransactions = list(map(processParsedTransaction, parsedTransaction))

        print(json.dumps(processedTransactions, indent=4))

