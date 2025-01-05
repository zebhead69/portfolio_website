BIPwords = ("abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act", "action", ...
)

my_seed_list = ["priority, negative, defense, shadow, ball, legal, resource, civil, fat, inherit, scrap, juice, label, switch, clog, month, whale, you, luggage, ginger, narrow, awesome, coyote, velvet"]

def find_matching_words(my_seed, BIPwords_list):
    
    
    matching_words = []
    BIPwords_set = set(BIPwords_list)  # Convert to set for efficiency

    for word in my_seed:
        if word in BIPwords_set:
            matching_words.append(word)
    print(matching_words)
    return matching_words




     