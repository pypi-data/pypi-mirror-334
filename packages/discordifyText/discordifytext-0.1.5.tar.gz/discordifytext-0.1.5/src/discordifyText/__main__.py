import discordifyText.discordifyText as discordifyText

def main():
    print('Enter one of the following functions: stutterify, uwuify, leetify, dummify, sarcasmify, piratify')
    func = input('>').strip()
    if func not in ['leetify','stutterify','uwuify','dummify', 'sarcasmify', 'piratify']:
        print('Invalid input.')
        return
    print('Enter the text you wish to transform:')
    text = input('>').strip()
    print('Here is your transformed text:')
    if func=='dummify':
        print(discordifyText.dummify(text))
    if func=='stutterify':
        print(discordifyText.stutterify(text))
    if func=='leetify':
        print(discordifyText.leetify(text))
    if func=='uwuify':
        print(discordifyText.uwuify(text))
    if func=='sarcasmify':
        print(discordifyText.sarcasmify(text))
    if func=='piratify':
        print(discordifyText.piratify(text))
    return 

if __name__=="__main__":
    main()