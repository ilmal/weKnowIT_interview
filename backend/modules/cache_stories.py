import os
import re

def get_file_name(story_name, language):
    if not os.path.exists(os.environ["CACHE_SAVE_DIR"]): return False
    return f"{os.environ['CACHE_SAVE_DIR']}/{re.sub('[^A-Za-z0-9]+', '', story_name)}_{language}.txt"


def cache_story(story_name, translation_arr, language):

    file_name = get_file_name(story_name, language)

    if not file_name: return False

    with open(file_name, "w+") as file:
        file.write(str(translation_arr))

    print("Story is cached to: ", file_name)



def get_cached_story(story_name, language):
    file_name = get_file_name(story_name, language)

    if not os.path.exists(file_name) or not file_name: return False

    print("Reading cache for story: ", file_name)

    content = open(file_name, "r").read()
    array_str = content[content.find('['):content.rfind(']')+1]

    if not array_str:
        print("READING FROM EMPTY FILE")
        os.remove(file_name)
        return False

    arr = eval(array_str)

    return arr


