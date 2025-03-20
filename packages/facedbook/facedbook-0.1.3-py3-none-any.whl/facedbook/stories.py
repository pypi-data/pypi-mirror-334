import random


# function to create a random scary story based on the inputted number of sentences
def face_story(n: int = 3) -> str:

    faces = {
        0: "(ノωヽ)",
        1: "(／。＼)",
        2: "(ﾉ_ヽ)",
        3: "..・ヾ(。＞＜)シ",
        4: "(″ロ゛)",
        5: "(;;;*_*)",
        6: "(・人・)",
        7: "＼(〇_ｏ)／",
        8: "(/ω＼)",
        9: "(/_＼)",
        10: "〜(ᗒᗣᗕ)〜",
        11: "Σ(°△°|||)︴",
        12: "(((＞＜)))",
        13: "＼(º □ º l|l)/",
        14: "〣( ºΔº )〣",
        15: "( ꩜ ᯅ ꩜;)⁭ ⁭",
        16: "＼(˚☐˚”)/ ",
        17: "ヾ(｡ꏿ﹏ꏿ)ﾉﾞ",
        18: "(つ﹏⊂)", 
        19: "(ᗒᗣᗕ)՞", 
        20: "ε=ε=(っ*´□`)っ",
        21: "(ｼ;ﾟДﾟ)ｼ",
        22: "(ò_ó╬)",
        23: "(☉_☉’)",
        24: "٩(ര̀ᴗര́)و"
    }

    actions = {
        0: "saw something move in the shadows behind",
        1: "felt an eerie presence near",
        2: "heard whispers coming from",
        3: "was followed by",
        4: "screamed as they saw",
        5: "was chased through the woods by",
        6: "vanished mysteriously after meeting",
        7: "saw glowing red eyes next to",
        8: "was trapped in a haunted house with",
        9: "heard footsteps behind them, but only saw",
        10: "saw their reflection turn into",
        11: "had their candle flicker out near",
        12: "felt icy fingers brush their shoulder from",
        13: "couldn't escape the nightmare of",
        14: "was dragged into the darkness by",
        15: "found an ancient book that summoned",
        16: "was warned in a dream about",
        17: "woke up to find",
        18: "saw a shadow move when looking at",
        19: "was cursed by", 
        20: "heard an echo in a low, quiet voice by", 
        21: "was awakened by scratching sounds made by",
        22: "was frozen in place as he heard raspy breathing from",
        23: "felt a pair of ice cold hands wrap around them from", 
        24: "watched helplessly as the shadows swallowed",
        25: "heard their own voice calling them from the darkness near", 
        26: "watched in horror as their door slowly creaked open, revealing",
        27: "was pulled under the bed by something that looked like",
        28: "felt the temperature drop suddenly as they passed",
        29: "screamed in panic as he was being chased by"
    }

    story = []
    for _ in range(n):
        face1 = faces[random.randint(0, len(faces) - 1)]
        face2 = faces[random.randint(0, len(faces) - 1)]
        action = actions[random.randint(0, len(actions) - 1)]

        sentence = f"{face1} {action} {face2}."
        story.append(sentence)

    return "\n".join(story)