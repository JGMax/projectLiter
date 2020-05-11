def morphAnalysisRus(wordsList, postsList, statisticList, morph):
    for word in wordsList:
        analyseResult = morph.parse(word.lower())[0]
        if analyseResult.tag.POS:
            if analyseResult.tag.POS not in postsList:
                postsList.append(analyseResult.tag.POS)
                statisticList[analyseResult.tag.POS] = 0

            statisticList[analyseResult.tag.POS] += 1
