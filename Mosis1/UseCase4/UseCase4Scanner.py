from scannerUseCase4 import Scanner
import charstream


class UseCase4Scanner(Scanner):
    def __init__(self, stream):

        # superclass constructor
        Scanner.__init__(self, stream)

        # define accepting states
        self.accepting_states = ["Init", "S1", "S2", "S4", "S5"]

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """

        if state == None:
            # new state
            return "Init"

        elif state == "Init":
            if input == 'E 1':
                # new state
                return "S1"
            elif input == 'E 2':
                return "S4"
            else:
                return "Init"

        elif state == "S1":
            if input == "G 1":
                # new state
                return "Init"
            elif input == "E 2":
                return "S2"
            else:
                return "S1"

        elif state == "S2":
            if input == "G 2":
                # new state
                return "S3"
            elif input == "G 1":
                return "Init"
            else:
                return "S2"

        elif state == "S3":
                return "S3"

        elif state == "S4":
            if input == "G 2":
                # new state
                return "Init"
            elif input == "E 1":
                return "S5"
            else:
                return "S4"

        elif state == "S5":
            if input == "G 1":
                # new state
                return "S6"
            elif input == "G 2":
                return "Init"
            else:
                return "S5"

        elif state == "S6":
                return "S6"

        else:
            return None

    def entry(self, state, input):
        pass


def main():
    f = open("trace.txt", 'r')
    inputstring = f.read()
    dummyLine = ("dummy\n")
    inputstring = dummyLine + inputstring
    stream = charstream.CharacterStream(inputstring)
    scanner = UseCase4Scanner(stream)
    result = scanner.scan()
    if result:
        print ">> Correct "
        stream.commit()
    else:
        print ">> Violation"


if __name__ == "__main__":
    main()