import pytest
from src.discordifyText import discordifyText
import re

class Tests:
    def test_dummify_get(self):
        actual = discordifyText.dummify('hello')
        assert len(actual) > 0
    def test_dummify_string(self):
        actual = discordifyText.dummify('hello')
        assert isinstance(actual, str)
    def test_dummify_equality(self):
        actual = discordifyText.dummify('hello')
        assert actual == "holle"

        actual = discordifyText.dummify('Hi, how are you?')
        assert actual == "Hu, how era yoi?"
    
    def test_stutterify_get(self):
        actual = discordifyText.stutterify('hello')
        assert len(actual) > 0
    def test_stutterify_string(self):
        actual = discordifyText.stutterify('hello')
        assert isinstance(actual, str)
    def test_stutterify_equality(self):
        actual = discordifyText.stutterify('hello')
        assert actual == "h-hello"

        actual = discordifyText.stutterify('Hello, how are you? I am fine, but tired.')
        assert actual == "H-Hello, how are y-you? I-I am fine, but... tired."

    def test_leetify_get(self):
        actual = discordifyText.leetify('hello')
        assert len(actual) > 0
    def test_leetify_string(self):
        actual = discordifyText.leetify('hello')
        assert isinstance(actual, str)
    def test_leetify_equality(self):
        actual = discordifyText.leetify('hello')
        assert actual == "H3LL0"

        actual = discordifyText.leetify('Hi, how are you?')
        assert actual == "H1, H0W 4R3 Y0U?"

    def test_uwuify_get(self):
        actual = discordifyText.uwuify('hello')
        assert len(actual) > 0
    def test_uwuify_string(self):
        actual = discordifyText.uwuify('hello')
        assert isinstance(actual, str)
    def test_uwuify_equality(self):
        actual = discordifyText.uwuify('hello')
        assert actual == "✧˖°. hewwo ₊˚⊹♡"

        actual = discordifyText.uwuify('Hello. How are you?')
        assert actual == "✧˖°. hewwo˚｡⋆୨୧˚\n⋆˙⟡ how awe you? ₊˚⊹♡"
        
    def test_sarcasmify_get(self):
        actual = discordifyText.sarcasmify('hello')
        assert len(actual) > 0
    def test_sarcasmify_string(self):
        actual = discordifyText.sarcasmify('hello')
        assert isinstance(actual, str)
    def test_sarcasmify_alternating_case(self):
        actual = discordifyText.sarcasmify('hello')
        actual = re.sub(r' 🙄$', '', actual)
        
        is_upper = None
        for i, char in enumerate(actual):
            if not char.isalpha():
                continue
                
            if is_upper is None:
                is_upper = char.isupper()
            else:
                assert char.isupper() != is_upper
                is_upper = char.isupper()
    
    def test_sarcasmify_emoji(self):
        # Test that the emoji is always added
        actual = discordifyText.sarcasmify('hello')
        assert actual.endswith(' 🙄')
        
        actual = discordifyText.sarcasmify('This is a test!')
        assert actual.endswith(' 🙄')

    def test_piratify_get(self):
        actual = discordifyText.piratify('hello')
        assert len(actual) > 0

    def test_piratify_string(self):
        actual = discordifyText.piratify('hello')
        assert isinstance(actual, str)

    def test_piratify_basic_replacements(self):
        actual = discordifyText.piratify('hello my friend')
        assert 'ahoy' in actual
        assert 'me' in actual
        assert 'matey' in actual

    def test_piratify_punctuation(self):
        actual = discordifyText.piratify('Hello, my friend!')
        assert actual.startswith('ahoy,')
        assert actual.endswith('!')

    def test_piratify_endings(self):
        actual = discordifyText.piratify('hello')
        assert any(ending in actual for ending in [' matey! ⚓', ' ye scurvy dog! 🏴‍☠️', ' arrr! ⚓', ' yarr harr! 🏴‍☠️', ' shiver me timbers! ⚓'])
