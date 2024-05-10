import hashlib

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, key):
        base = 31
        prime = 997
        hash_value = 0
        for char in key:
            hash_value = (hash_value * base + ord(char)) % prime
        return hash_value % self.size

    def insert(self, key, value):
        index = self.hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self.hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

class SpellChecker:
    def __init__(self, dictionary_file):
        self.dictionary = HashTable(100)
        self.load_dictionary(dictionary_file)
        self.edit_distance_threshold = 2

    def load_dictionary(self, dictionary_file):
        with open(dictionary_file, 'r') as file:
            for word in file:
                self.dictionary.insert(word.strip().lower(), True)

    def levenshtein_distance(self, word1, word2):
        if len(word1) < len(word2):
            return self.levenshtein_distance(word2, word1)
        if len(word2) == 0:
            return len(word1)
        previous_row = range(len(word2) + 1)
        for i, c1 in enumerate(word1):
            current_row = [i + 1]
            for j, c2 in enumerate(word2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def suggest_corrections(self, word):
        suggestions = []
        for key in self.dictionary.table:
            for pair in key:
                if self.levenshtein_distance(pair[0], word) <= self.edit_distance_threshold:
                    suggestions.append(pair[0])
        return suggestions

    def check_spelling(self, text):
        misspelled = []
        words = text.split()
        for word in words:
            if not self.dictionary.get(word.lower()):
                misspelled.append(word)
        return misspelled

    def add_to_dictionary(self, word):
        self.dictionary.insert(word.lower(), True)

def main():
    spell_checker = SpellChecker('Dictionary.txt')
    while True:
        print("\n1. Check spelling")
        print("2. Add word to dictionary")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            text = input("Enter text to check: ")
            misspelled = spell_checker.check_spelling(text)
            if misspelled:
                print("Misspelled words:")
                for word in misspelled:
                    print(f"- {word}")
                    suggestions = spell_checker.suggest_corrections(word)
                    if suggestions:
                        print("Suggestions:")
                        for suggestion in suggestions:
                            print(f"  - {suggestion}")
            else:
                print("No misspelled words found.")
        elif choice == '2':
            new_word = input("Enter word to add to dictionary: ")
            spell_checker.add_to_dictionary(new_word)
            print(f"'{new_word}' has been added to the dictionary.")
        elif choice == '3':
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

main()