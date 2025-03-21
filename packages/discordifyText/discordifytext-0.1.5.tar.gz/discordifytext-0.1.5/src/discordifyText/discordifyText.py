import re
import sys
import random

sys.stdout.reconfigure(encoding='utf-8')

#dummify(text: str) -> str – Reverses the vowels in a string.
def dummify(s):
    vowels = "aeiouAEIOU"
    vowel_list = [char for char in s if char in vowels]
    result = []
    for char in s:
        if char in vowels:
            result.append(vowel_list.pop())
        else:
            result.append(char)
    return "".join(result)

#stutterify(text: str) -> str – Adds a stuttering effect to the text.
def stutterify(s):
    pronouns = {"you","wait","what","so","um","uh","i"}
    conjunctions = {'but','and'}

    def stutter(word):
        prefix = word[:1]
        return f"{prefix}-{word}" if word else word
    
    words = re.findall(r"\b\w+\b|[^\w\s]", s)
    if words:
        words[0] = stutter(words[0])
    for i in range(1, len(words)):
        word = words[i].lower()
        if word in pronouns:
            words[i] = stutter(words[i])
        elif word in conjunctions:
            words[i] += "..."  
    result = []
    for i, word in enumerate(words):
        if i > 0 and re.match(r"[.,!?;:]", word):  
            result[-1] += word
        else:
            result.append(word)

    return " ".join(result)

#leetify(text: str) -> str – Converts text into 1337 speak.
def leetify(s):
    s = s.upper()

    leet= {
        'O': '0', 'I': '1', 'Z': '2', 'E': '3',
        'A': '4', 'S': '5', 'G': '6', 'T': '7',
        'B': '8', 'P': '9'
    }

    result = ""
    for char in s:
        if char in leet:
            result += leet[char] 
        else:
            result += char

    return result

#uwuify(text: str) -> str – L to w, sparkle ASCII at the start and end
def uwuify(s):
    s = s.lower().strip()

    uwu= {
        'l':'w','r':'w', '.':'˚｡⋆୨୧˚\n⋆˙⟡'
    }

    result = ""
    result += '✧˖°. '

    for char in s:
        if char in uwu:
            result += uwu[char] 
        else:
            result += char

    if (s[len(s)-1] == '.'):        
        return result[:-4]
    else:
        result += ' ₊˚⊹♡'
        return result

#sarcasmify(text: str) -> str – Alternates between uppercase and lowercase letters
def sarcasmify(s):
    result = []
    should_be_upper = bool(random.getrandbits(1))  # Random start
    
    for char in s:
        if char.isalpha():
            result.append(char.upper() if should_be_upper else char.lower())
            should_be_upper = not should_be_upper
        else:
            result.append(char)
    
    result.append(" 🙄")
    
    return "".join(result)

def piratify(s):
    """Convert text into pirate speak, adding pirate slang and nautical flair.
    
    Args:
        s (str): The input text to convert to pirate speak
        
    Returns:
        str: The piratified text with nautical emojis
        
    Example:
        >>> piratify("Hello my friend")
        'ahoy me matey! ⚓'
    """
    pirate_dict = {
        'hello': 'ahoy',
        'hi': 'yarr',
        'my': 'me',
        'your': 'yer',
        'you': 'ye',
        'is': 'be',
        'are': 'be',
        'the': "th'",
        'yes': 'aye',
        'no': 'nay',
        'stop': 'avast',
        'friend': 'matey',
        'friends': 'crew',
        'everyone': 'all hands',
        'food': 'grub',
        'drink': 'grog',
        'money': 'doubloons',
        'treasure': 'booty'
    }
    
    endings = [
        " matey! ⚓",
        " ye scurvy dog! 🏴‍☠️",
        " arrr! ⚓",
        " yarr harr! 🏴‍☠️",
        " shiver me timbers! ⚓"
    ]
    
    words = s.lower().split()
    
    for i, word in enumerate(words):
        clean_word = word.strip('.,!?')
        if clean_word in pirate_dict:
            punct = word[len(clean_word):]
            words[i] = pirate_dict[clean_word] + punct
    
    result = ' '.join(words)
    
    if not result.rstrip()[-1] in '.!?':
        result += random.choice(endings)
    
    return result
