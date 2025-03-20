import os

def display_text(file_name):
    """
    Reads and displays the content of a text file from the `data` folder.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_dir, file_name)

    if not os.path.exists(file_path):
        print(f"Error: File '{file_name}' not found in the 'data' folder.")
        return

    with open(file_path, "r") as file:
        content = file.read()
        print(content)