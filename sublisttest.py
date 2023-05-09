def combine_short_sublists(list_of_lists):
    if not list_of_lists:
        return []

    # Find the length of the largest sublist
    max_length = max(len(sublist) for sublist in list_of_lists)

    # Initialize an empty list to store the new sublists
    combined_sublists = []

    # Iterate through the list_of_lists
    for sublist in list_of_lists:
        # If the current sublist is shorter than the largest sublist
        if len(sublist) < max_length:
            # Check if there's a previous sublist in the combined_sublists that can be extended
            for previous_sublist in combined_sublists:
                if len(previous_sublist) + len(sublist) == max_length:
                    previous_sublist.extend(sublist)
                    break
            else:  # If no suitable previous sublist was found, add the current sublist as is
                combined_sublists.append(sublist)
        else:
            combined_sublists.append(sublist)

    return combined_sublists

# Example usage
list2 = [[1, 2, 3], [4, 5], [6, 7, 8], [9], [10, 11]]

combined_list = combine_short_sublists(list2)
print(combined_list)  # Output: [[1, 2, 3], [4, 5, 9], [6, 7, 8], [10, 11]]
