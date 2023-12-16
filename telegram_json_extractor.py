import json
import re
import pandas as pd
 
# Opening JSON file
def EvaluateWorldVote(record):
    try:
        gamedate= record['date']
        whoname= record['from']
        whoid= record['from_id']
        performance =ExtractPerformance(record['text'])
        return {
            'gamedate': gamedate,
            'whoname': whoname,
            'whoid': whoid,
            'gamenumber': performance['gamenumber'],
            'performance': performance['performance']
        }
    except:
        return {
        'gamedate': '',
        'whoname': '',
        'whoid': '',
        'gamenumber': '',
        'performance': ''
    }


def ExtractPerformance(text):
    try:
        vote = EvalTextSplitArray(text)
        gamenumber= re.findall('[#]\d+', vote)
        performance = re.findall('[\w|\d]\/\d', vote)
        if gamenumber:
            gamenumber = gamenumber[0].replace('#','')
        if performance:
            performance = performance[0].split('/')
            if 'x' in str(performance[0]).lower():
                performance[0] = str(performance[0]).lower().replace('x','7')

        return {
            'gamenumber':gamenumber,
            'performance': performance[0]
        }
    except:
        return {
        'gamenumber':'',
        'performance': ''
    }

def EvalTextSplitArray(text):
    if len(text) > 1:
        for palabra in text:
            if "palabra del día" in palabra:
                wordlvote = palabra.split('\n')
                for vote in wordlvote:
                    if "palabra del día" in vote:
                        return vote
    return ""

def Main(TelegramConversations):
    # jsonFile = open('.data/result.json')
    # history = json.load(jsonFile)

    parcialresults = pd.DataFrame(columns=['gamedate', 'whoname', 'whoid', 'gamenumber','performance'])

    for record in TelegramConversations['messages']:
        texto = str(record['text'])
        if "La palabra del día" in texto:
            vote=EvaluateWorldVote(record)
            votedf = pd.DataFrame([vote])
            parcialresults = pd.concat([parcialresults,votedf],  ignore_index=True, sort=False)
            # df = df.append(vote, ignore_index = True)

    parcialresults.to_csv('./data/results.csv', index=False)

    return True

    # jsonFile.close()

