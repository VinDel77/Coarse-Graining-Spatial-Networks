import pickle as p


def save_object(obj, description=None):
    if description is not None:
        print("Trying to save: {}".format(description))

    to_save = input("Do you wish to save this run? y/n  ")
    if to_save != 'y':
        return

    file_name = input("Enter filename: ")
    p.dump(obj, open(file_name + ".pickle", 'wb'))
    print("Saved")
