import string
alphabetDictionary = dict(zip(string.ascii_lowercase, string.ascii_uppercase))

words = 'hello Friends I am A boy'

words = words.split()

titleCase = ''


for word in words:

    if alphabetDictionary.get(word[0]):
        titleCase += alphabetDictionary[word[0]]+ word[1:] + ' '
    else:
        titleCase += word + ' '

print(titleCase)