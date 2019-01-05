import pickle as p


def save_object(obj, description=None, skip_dialogue=False):
    if skip_dialogue:
        file_name  = description
    else:
        if description is not None:
            print("Trying to save: {}".format(description))

        to_save = input("Do you wish to save this run? y/n  ")
        if to_save != 'y':
            return
        file_name = input("Enter filename: ")
    with open(file_name + ".pickle", 'wb') as f:
        p.dump(obj, f)
