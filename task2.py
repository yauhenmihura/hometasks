#!/usr/bin/env python

def palindrome(seq):
   return seq == seq[::-1]

words = input('Enter sentence, separated by a space: ').split()
print("Yes, it is a palindrom" if palindrome(words) else "It is not a palindrome")