import webbrowser

from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

def group_match_strings(strings, funcc, threshold=85, func2=None):
    groups = []
    assigned = set()

    for i, string1 in enumerate(strings):
        if i in assigned:
            continue

        group = [string1]
        assigned.add(i)

        for j, string2 in enumerate(strings[i+1:]):
            if i + 1 + j in assigned:
                continue
            score = fuzz.token_set_ratio(funcc (string1), funcc (string2))
            if func2:
                if func2 (string1, string2):
                    score = 100

            if score >= threshold:
                group.append(string2)
                assigned.add(i + 1 + j)

        groups.append(group)

    return groups

def process_lists(lists, process, display):
    while True:
        # Display lists with their indexes
        print("Lists:")
        for i, lst in enumerate(lists):
            print(f"{i}: {display(lst)}")

        # Get user input for action
        action = input("Choose an action (s/j/a/q): ").lower()

        if action == "s":
            # Split the selected list
            index = int(input("Enter the index of the list you want to split: "))
            if 0 <= index < len(lists):
                sublist = lists.pop(index)
                for item in sublist:
                    lists.append([item])
            else:
                print("Invalid index.")
        elif action == "o":
            index = int(input("Enter the index of the list you want to split: "))
            if 0 <= index < len(lists):
                for item in lists[index]:
                    webbrowser.open(item[0])
        elif action == "j":
            # Join two lists together
            index1 = int(input("Enter the index of the first list to join: "))
            index2 = int(input("Enter the index of the second list to join: "))
            if 0 <= index1 < len(lists) and 0 <= index2 < len(lists):
                lists[index1] = lists[index1] + lists[index2]
                del lists[index2]
            else:
                print("Invalid indexes.")
        elif action == "d":
            print("Delete an item from a list.")
            index = int(input("delete an item: "))
            if 0 <= index < len(lists):
                lists.pop(index)
            else:
                print("Invalid index.")
        elif action == "a":
            index = int(input(" process list: "))
            if 0 <= index < len(lists):
                process(lists[index])
        elif action == "0":
            process(lists[0])
            break
        elif action == "a":
            index = int(input(": "))
            # Placeholder for add action
            print("Add action not implemented yet.")

        elif action == "q" or action == "":
            # Quit
            print("Exiting...")
            break
        else:
            print("Invalid action.")


