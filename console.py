class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(message, severity = bcolors.OKBLUE):
    print(f"{severity}{message}{bcolors.ENDC}")

def separate(severity = bcolors.HEADER):
    print(f"{severity}{bcolors.UNDERLINE}\n=======================\n{bcolors.ENDC}")

def multiple_choise_input(options):
    #Input
    option = int(input())

    #Output
    if (option in options):
        return options.get(option)
    else:
        log('Error: Wrong user input x.x, please cooperate.', bcolors.FAIL)
        exit()

def multiple_choise(options):
    #Displaying
    log(f"Please select any of these options (1-{len(options)}): ", bcolors.OKBLUE)
    for aux_option in options:
        shown_option = options.get(aux_option) or ""
        log(str(aux_option) + ": " + shown_option, bcolors.OKCYAN)

    return multiple_choise_input(options)

def multiple_choise_lootboxes(options, balance):
    #Displaying
    log(f"Please select any of these lootboxes (insert the cost): ", bcolors.OKBLUE)
    for aux_option in options:
        shown_option = options.get(aux_option) or ""
        cant_afford = balance < aux_option
        color = bcolors.OKCYAN
        if cant_afford:
            color = bcolors.FAIL
        log(str(aux_option) + ": " + shown_option, color)

    return multiple_choise_input(options)