"""
test
"""
import random

import string


print(random.randint(1,10))

letters = 'abcdef'
print(random.choice(letters))

print(random.sample(letters, 3))

nums = [1, 2, 3, 4, 5]
random.shuffle(nums)  # Shuffles in place
print(nums)

print(string.ascii_lowercase)   # abcdefghijklmnopqrstuvwxyz
print(string.ascii_uppercase)   # ABCDEFGHIJKLMNOPQRSTUVWXYZ
print(string.digits)            # 0123456789
print(string.punctuation)       # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~