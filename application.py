import json
import pandas as pd
import telegram_json_extractor as tje
import results_correct_output as rco



jsonFile = open('./data/result.json')

history = json.load(jsonFile)

if tje.Main(history):
    rco.CreateFinalGrid()
    print("OK")


jsonFile.close()


