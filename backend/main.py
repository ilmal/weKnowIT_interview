from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import ast
import json

import httpcore
setattr(httpcore, 'SyncHTTPTransport', any)

import os
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'
import eventlet

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')

from modules.import_stories import import_stories
from modules.translate_story import translate_story
from modules.get_stories import get_stories
from modules.cache_stories import cache_story, get_cached_story

# dev_story = [['The Three Little Pigs', 'Sān zhī xiǎo zhū'], ["The story of The Three Little Pigs featured here has been adapted from different sources and from childhood memory. The primary sources are English Fairy Tales, retold by Flora Annie Steel (1922) with illustrations by L. Leslie Brooke from the 1904 version. This story is featured in our Favorite Fairy Tales and Children's Stories.", 'Zhèlǐ chūxiàn de sān zhī xiǎo zhū de gùshì shì cóng bùtóng láiyuán hé tóngnián jìyì zhōng gǎibiān ér lái de. Zhǔyào zīliào láiyuán shì yīngyǔ tónghuà gùshì, yóu Flora Annie Steel(1922) chóngxīn jiǎngshùle 1904 nián bǎnběn de L. Leslie Brooke de chātú. Zhège gùshì zài wǒmen zuì xǐhuān de tónghuà hé értóng gùshì zhōng zhǎn chū.'], ['Once upon a time there was an old mother pig who had three little pigs and not enough food to feed them. So when they were old enough, she sent them out into the world to seek their fortunes.', 'Céngjǐhéshí, yǒuyī zhǐ lǎo mǔ zhū yǒusān zhī xiǎo zhū, méiyǒu zúgòu de shíwù lái wèi tāmen. Yīncǐ, dāng tāmen niánjì zúgòu dà de shíhòu, tā jiāng tāmen sòng dào shìjiè shàng xúnqiú mìngyùn.'], ["The first little pig was very lazy. He didn't want to work at all and he built his house out of straw. The second little pig worked a little bit harder but he was somewhat lazy too and he built his house out of sticks. Then, they sang and danced and played together the rest of the day.", 'Dì yī zhǐ xiǎo zhū hěn lǎnduò. Tā gēnběn bùxiǎng gōngzuò, tā yòng dàocǎo jiànzàole zìjǐ de fángzi. Dì èr zhǐ xiǎo zhū de gōngzuò gèngjiā nǔlì, dàn tā yě yǒuxiē lǎnduò, tā yòng gùnzi gàile fángzi. Ránhòu, tāmen zài yītiān de qíyú shíjiān lǐ chànggē, tiàowǔ bìng yīqǐ yǎnzòu.'], ['The third little pig worked hard all day and built his house with bricks. It was a sturdy house complete with a fine fireplace and chimney. It looked like it could withstand the strongest winds.', 'Dì sān zhī xiǎo zhū zhěng tiān dū zài nǔlì gōngzuò, bìngyòng zhuāntóu jiànzàole tā de fángzi. Zhè shì yī jiàn jiāngù de fángzi, shàngmiàn yǒu yīgè jīngměi de bìlú hé yāncōng. Kàn qǐlái tā kěyǐ chéngshòu zuì qiáng de fēng.'], ['The next day, a wolf happened to pass by the lane where the three little pigs lived; and he saw the straw house, and he smelled the pig inside. He thought the pig would make a mighty fine meal and his mouth began to water.', 'Dì èr tiān, yī zhǐ láng pèngqiǎo jīngguò sān zhī xiǎo zhū jūzhù de chēdào. Ránhòu tā kàn dàole dàocǎo wū, tā wén dàole lǐmiàn de zhū. Tā rènwéi zhū huì zuò yī dùn fēngshèng de fàncài, tā de zuǐ kāishǐ jiāo shuǐ.'], ['So he knocked on the door and said:', 'Suǒyǐ tā qiāo mén shuō:'], ['  Little pig! Little pig!', 'Xiǎo zhū! Xiǎo zhū!'], ['  Let me in! Let me in!', 'Ràng wǒ jìnqù! Ràng wǒ jìnqù!'], ["But the little pig saw the wolf's big paws through the keyhole, so he answered back:", 'Dànshì xiǎo zhū tōngguò yàoshi kǒng kàn dàole láng de dà zhuǎzi, suǒyǐ tā huídále:'], ['  No! No! No! ', 'Bù! Bù! Bù!'], ['  Not by the hairs on my chinny chin chin!', 'Wǒ de xiàbā xiàbā shàng de tóufǎ bùshì.'], ['Then the wolf showed his teeth and said:', 'Ránhòu láng lùchū yáchǐ, shuō:'], ["  Then I'll huff ", 'Nà wǒ huì fánnǎo de'], ["  and I'll puff ", 'Wǒ huì chuī'], ["  and I'll blow your house down.", 'Wǒ huì bǎ nǐ de fángzi chuī dào.'], ['So he huffed and he puffed and he blew the house down! The wolf opened his jaws very wide and bit down as hard as he could, but the first little pig escaped and ran away to hide with the second little pig.', 'Suǒyǐ tā nùqì chōngchōng, chuīle, tā bǎ fáng zǐ zhá le xiàlái! Láng dǎkāile tā de xiàbā, jǐn kěnéng de zhāng kāi xiàbā, dàn dì yī zhǐ xiǎo zhū táotuōle, táozǒule, yòng dì èr zhǐ xiǎo zhū duǒ qǐlái.'], ['The wolf continued down the lane and he passed by the second house made of sticks; and he saw the house, and he smelled the pigs inside, and his mouth began to water as he thought about the fine dinner they would make.', 'Láng jìxù zǒu shàng chēdào, tā jīngguò dì èr zuò mù gùn de fángzi. Ránhòu tā kàn dàole fángzi, tā wén dàole lǐmiàn de zhū de qìwèi, dāng tā xiǎngdào tāmen huì zuò de wǎncān shí, tā de zuǐ kāishǐ jiāo shuǐ.'], ['So he knocked on the door and said:', 'Suǒyǐ tā qiāo mén shuō:'], ['  Little pigs! Little pigs!', 'Xiǎo zhū! Xiǎo zhū!'], ['  Let me in! Let me in!', 'Ràng wǒ jìnqù! Ràng wǒ jìnqù!'], ["But the little pigs saw the wolf's pointy ears through the keyhole, so they answered back:", 'Dànshì xiǎo zhū tōngguò yàoshi kǒng kàn dàole láng de jiān tóu ěrduǒ, suǒyǐ tāmen huídále:'], ['  No! No! No!', 'Bù! Bù! Bù!'], ['  Not by the hairs on our chinny chin chin!', 'Bùshì wǒmen xiàbā shàng de tóufǎ!'], ['So the wolf showed his teeth and said:', 'Suǒyǐ láng lùchū yáchǐ, shuō:'], ["  Then I'll huff ", 'Nà wǒ huì fánnǎo de'], ["  and I'll puff ", 'Wǒ huì chuī'], ["  and I'll blow your house down!", 'Wǒ huì bǎ nǐ de fángzi chuī dào!'], ['So he huffed and he puffed and he blew the house down! The wolf was greedy and he tried to catch both pigs at once, but he was too greedy and got neither! His big jaws clamped down on nothing but air and the two little pigs scrambled away as fast as their little hooves would carry them.', 'Suǒyǐ tā nùqì chōngchōng, chuīle, tā bǎ fáng zǐ zhá le xiàlái! Láng hěn tānlán, tā shìtú yīcì zhuā dào liǎngtóu zhū, dàn tā tài tānlánle, dōu méiyǒu! Tā de dà gé gǔ chúle kōngqì wài, shénme dōu méiyǒu jiā zhù, liǎng zhī xiǎo zhū xiàng tāmen de xiǎo tízi nàyàng kuài dì pále chūlái.'], ["The wolf chased them down the lane and he almost caught them. But they made it to the brick house and slammed the door closed before the wolf could catch them. The three little pigs they were very frightened, they knew the wolf wanted to eat them. And that was very, very true. The wolf hadn't eaten all day and he had worked up a large appetite chasing the pigs around and now he could smell all three of them inside and he knew that the three little pigs would make a lovely feast.", "Láng jiāng tāmen zhuīgǎn dào chēdào shàng, tā jīhū zhuā zhùle tāmen. Dànshì tāmen dàodále zhuān fáng, ránhòu zài láng zhuā zhù tāmen zhīqián guān shàngmén. Tāmen fēicháng hàipà de sān zhī xiǎo zhū, tāmen zhīdào láng xiǎng chī tāmen. Nà shì fēicháng fēicháng zhēnshí de. Láng bìng méiyǒu zhěng tiān chīfàn, tā mángzhe dàchīyījīng de shíyù, zhuīzhú zhū, xiànzài tā kěyǐ zài lǐmiàn wén dào suǒyǒu sān zhī xiǎo zhū, tā zhīdào sān zhī xiǎo zhū huì zuò yīgè kě'ài de shèngyàn."], ['So the wolf knocked on the door and said:', 'Suǒyǐ láng qiāo mén shuō:'], ['  Little pigs! Little pigs!', 'Xiǎo zhū! Xiǎo zhū!'], ['  Let me in! Let me in!', 'Ràng wǒ jìnqù! Ràng wǒ jìnqù!'], ["But the little pigs saw the wolf's narrow eyes through the keyhole, so they answered back:", 'Dànshì xiǎo zhū tōngguò yàoshi kǒng kàn dàole láng de xiázhǎi yǎnjīng, suǒyǐ tāmen huídále:'], ['  No! No! No! ', 'Bù! Bù! Bù!'], ['  Not by the hairs on our chinny chin chin!', 'Bùshì wǒmen xiàbā shàng de tóufǎ!'], ['So the wolf showed his teeth and said:', 'Suǒyǐ láng lùchū yáchǐ, shuō:'], ["  Then I'll huff ", 'Nà wǒ huì fánnǎo de'], ["  and I'll puff ", 'Wǒ huì chuī'], ["  and I'll blow your house down.", 'Wǒ huì bǎ nǐ de fángzi chuī dào.'], ["Well! he huffed and he puffed. He puffed and he huffed. And he huffed, huffed, and he puffed, puffed; but he could not blow the house down. At last, he was so out of breath that he couldn't huff and he couldn't puff anymore. So he stopped to rest and thought a bit.", 'Chūsè dì! Tā nùqì chōngchōng, chuǎn bùguò qì. Tā chuǎnqì, nùqì chōngchōng. Tā nùqì chōngchōng, nùqì chōngchōng, fúzhǒng, fúzhǒng. Dànshì tā bùnéng bǎ fángzi chuī dào. Zuìhòu, tā chuǎn bùguò qì, yǐ zhìyú tā wúfǎ fánnǎo, tā zài yě wúfǎ chuīle. Suǒyǐ tā tíng xiàlái xiūxíle yīxià.'], ['But this was too much. The wolf danced about with rage and swore he would come down the chimney and eat up the little pig for his supper. But while he was climbing on to the roof the little pig made up a blazing fire and put on a big pot full of water to boil. Then, just as the wolf was coming down the chimney, the little piggy pulled off the lid, and plop! in fell the wolf into the scalding water.', 'Dàn zhè tài duōle. Láng fènnù de tiàowǔ, fāshì tā huì cóng yāncōng xiàlái chī diào xiǎo zhū chī wǎnfàn. Dànshì, dāng tā pá shàng wūdǐng shí, xiǎo zhū gòuchéngle lièhuǒ, fàng zài yīgè chōngmǎn shuǐ de dà guō shàng zhǔfèi. Ránhòu, zhèngdàng láng cóng yāncōng xiàlái shí, xiǎo zhū cóng gàizi shàng lā xiàlái, ránhòu! Zài jiāng láng dào rù tàng shuǐzhōng.'], ['So the little piggy put on the cover again, boiled the wolf up, and the three little pigs ate him for supper.', 'Yīncǐ, xiǎo zhū zàicì fàng zài gàizi shàng, bǎ láng zhǔfèile, sān zhī xiǎo zhū chīle wǎnfàn.'], ["If you enjoyed this story, you may be interested in our collection of Children's Stories or other titles from our library of Pre-K Read-Aloud Stories.", 'Rúguǒ nín xǐhuān zhège gùshì, nàme nín kěnéng huì duì wǒmen de “Pre-K Read-Aloud gùshì” túshū guǎn zhōng de értóng gùshì huò qítā biāotí gǎn xìngqù.']]

languages = [
    "zh-cn"
]

@app.route("/api/get_languages", methods=["GET"])
def api_get_languages():
    print("Handling get languages...")
    return languages

@app.route("/api/get_stories", methods=["GET"])
def api_get_stories():
    print("Handling get_stories...")
    return get_stories()

@app.route("/api/get_story_text", methods=["GET"])
def api_get_story_text():
    if not request.args.get('story', '') or not request.args.get('language', ''): 
        return "request was without story or language info", 400
        raise Exception("request did not have story or language info!")
    story = request.args.get('story', '')
    language = request.args.get('language', '')

    for e in get_stories():
        if str(story).lower() == str(e[1]).lower():
            print("Importing story...")
            (story, story_name) = import_stories(e)
            story_lines = [e.replace("\r", "") for e in story.split("\n") if not e == "" and not e == "\r"]

            if language not in languages: return "language provided is not supported", 400

            cached_story = get_cached_story(story_name, language)
            if cached_story:
                return cached_story

            print("Translating the data...")
            translation_arr = translate_story(story_lines, language)

            cache_story(story_name, translation_arr, language)

            return translation_arr



    return "The story provided was not found on the server", 400

@app.route("/api/get_generated_stories", methods=["GET"])
def api_get_generated_stories():
    stories = os.listdir(os.environ['GENERATED_STORIES_SAVE_DIR'])
    result_list = []

    if len(stories) > 0:
        for e in stories:
            if not ".py" in e:
                continue
            result_list.append([[], [e.split(".")[0]]])
        return result_list
    return False


@app.route("/api/get_generated_text", methods=["GET"])
def api_get_generated_text():
    if not request.args.get('story', '') : 
        return "request was without story or language info", 400

    story = request.args.get('story', '')

    print("STORY: ", story)

    # Read the file
    with open(os.environ['GENERATED_STORIES_SAVE_DIR'] + f"/{story}.py", "r") as file:
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

    print("english_story", english_story)
    print("pinyin_story", pinyin_story)
    print("translation_array", translation_array)

    return json.dumps({
        "english_story": english_story,
        "pinyin_story": pinyin_story,
        "translation_array": translation_array
    })





def main():
    (story, story_name) = import_stories(stories[0])

    story_lines = [e for e in story.split("\n") if not e == "" and not e == "\r"]

    translation_arr = translate_story(story_lines, "zh-cn")

    for e in translation_arr:
        print(e[0])
        print(e[1])
        print("\n\n")



if __name__ == "__main__":
    flask.run(app, debug=True, port=5000)
    socketio.run(app, debug=True, port=5000)
