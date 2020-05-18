import nltk


def morphAnalysisRus(wordsList, postsList, statisticList, morph):
    for_next_analysis_dict = {}
    for word in wordsList:
        analyseResult = morph.parse(word.lower())[0]
        if analyseResult.tag.POS:
            if analyseResult.tag.POS not in postsList:
                postsList.append(analyseResult.tag.POS)
                statisticList[analyseResult.tag.POS] = 0
                for_next_analysis_dict[analyseResult.tag.POS] = []

            statisticList[analyseResult.tag.POS] += 1
            for_next_analysis_dict[analyseResult.tag.POS].append(word)
    return for_next_analysis_dict


def morphAnalysisEng(wordsList, postsList, statisticList):
    for_next_analysis_dict = {}
    for word in wordsList:
        analyseResult = nltk.pos_tag(word.lower())[0]
        if analyseResult.tag.POS:
            if analyseResult.tag.POS not in postsList:
                postsList.append(analyseResult.tag.POS)
                statisticList[analyseResult.tag.POS] = 0
                for_next_analysis_dict[analyseResult.tag.POS] = []

            statisticList[analyseResult.tag.POS] += 1
            for_next_analysis_dict[analyseResult.tag.POS].append(word)
    return for_next_analysis_dict
