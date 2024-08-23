import ast
import os

def main():

    for story in os.listdir("./chatgpt-stories"):
        if not story.endswith(".py"):
            continue

        # Read the file
        with open("./chatgpt-stories" + f"/{story}", "r") as file:
            file_content = file.read()

        # Extract variables using AST module
        variables = {}
        tree = ast.parse(file_content)

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables[target.id] = ast.literal_eval(node.value)

        # Now you have the variables extracted
        english_story = variables.get("english_story")
        pinyin_story = variables.get("pinyin_story")
        translation_array = variables.get("translation_array")

        # print("english_story", english_story)
        # print("pinyin_story", pinyin_story)
        # print("translation_array", translation_array)

        is_correct = True

        for i, e in enumerate(pinyin_story):
            if len(e) != len(translation_array[i]):
                print(f"Error in {story}: pinyin_story and translation_array have different lengths at index {i}")
                is_correct = False

        if not is_correct:
            print(f"Error in {story}: pinyin_story and translation_array have different lengths at index {i}")
            return
        print(f"Success in {story}")

    pass


if __name__ == "__main__":
    main()