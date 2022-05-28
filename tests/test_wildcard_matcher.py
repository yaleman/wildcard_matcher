""" tests wildcard_matcher """

import random
import string

import pytest

import wildcard_matcher

def test_has_stars_should():
    """ tests a pattern with stars """
    assert wildcard_matcher.has_stars("*")
    assert wildcard_matcher.has_stars("**")
    assert wildcard_matcher.has_stars("foo*123")
    assert wildcard_matcher.has_stars("*foo*123")

    assert not wildcard_matcher.has_stars("foo123")
    assert not wildcard_matcher.has_stars("foo123".encode("utf-8"))
    assert not wildcard_matcher.has_stars("")


def test_simple_pattern_endswith_star():
    """ tests a simple pattern that ends with * """
    assert wildcard_matcher.match("hello world", "hello*")
    assert wildcard_matcher.match("hello world", "hello *")
    assert wildcard_matcher.match("hello world", "hello w*")
    assert not wildcard_matcher.match("hello world", "foo*")

def test_simple_pattern_startswith_star():
    """ tests a simple pattern that ends with * """
    assert wildcard_matcher.match("hello world", "*world")
    assert wildcard_matcher.match("hello world", "* world")
    assert wildcard_matcher.match("hello world", "*o world")
    assert not wildcard_matcher.match("hello world", "*foo")

def test_complex_pattern():
    """ tests a more complex pattern """
    assert wildcard_matcher.match("hello world", "h*world*")
    assert wildcard_matcher.match("hello world", "*h*world*")
    assert wildcard_matcher.match("hello world", "*h*world")
    assert wildcard_matcher.match("hello world", "*h* world")

    assert not wildcard_matcher.match("hello world", "*h *world*")
    assert not wildcard_matcher.match("hello world", "*h *orld*")

def test_no_wildcard_in_pattern():
    """ tests when there's no wildcard """
    assert wildcard_matcher.match("test string", "test string")
    assert not wildcard_matcher.match("test string", "test pattern")
    assert not wildcard_matcher.match("test string", "test")
    assert not wildcard_matcher.match("test string", "pattern")
    assert not wildcard_matcher.match("test string", " pattern")
    assert wildcard_matcher.match("", "")
    assert not wildcard_matcher.match("asdfasdf", "")
    assert not wildcard_matcher.match("", "asdfasdf")


#pylint: disable=protected-access
def test_validator():
    """ tests the input validator """
    with pytest.raises(TypeError):
        wildcard_matcher._validate_input(123)
    assert wildcard_matcher._validate_input("hello world")
    assert wildcard_matcher._validate_input(b"hello world")
    assert wildcard_matcher._validate_input(b"hello world".decode("utf-8"))
    assert wildcard_matcher._validate_input("hello world".encode("utf-8"))

def test_empty_pattern_and_string():
    """ tests both empty pattern and string """
    assert wildcard_matcher.match("", "")

def test_empty_pattern_and_single_wilcard():
    """ tests both empty pattern and single wildcard """
    assert wildcard_matcher.match("", "*")

def test_single_wildcard():
    """ tests a bunch of strings and a pattern that's a single wildcard """
    test_pattern = "*"
    assert wildcard_matcher.match("1212341234", test_pattern)
    test_chars = string.ascii_letters + string.digits + string.printable + string.punctuation
    for _ in range(100):
        testval = ""
        for _ in range(100):
            testval = f"{testval}{random.choice(test_chars)}"
            assert wildcard_matcher.match(testval, test_pattern)
