import boto3


Items_List = ['pen']
Probable_Place_List = {
    "pen":"Try checking behind the table or in the attic"}



def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the Find my things Alexa Skill. I will help you locate your most valuable things. To help me learn better, please report to me where you have previously lost an item.\
    If you would like to hear where the requested item is, you could say for example: where is my pen"
    reprompt_MSG = "Do you want to hear more about a particular item?"
    card_TEXT = "Pick an item."
    card_TITLE = "Choose an item ."
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")


def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "helpFindItem":
        #print(event)
        return find_items(event)       
    elif intent_name == "reportItems":
        return update_table(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)



def find_items(event):
    name=event['request']['intent']['slots']['items']['value']
    item_list_lower=[w.lower() for w in Items_List]
    if name.lower() in item_list_lower:
        reprompt_MSG = "Do you want to hear more about a particular item?"
        card_TEXT = "You've picked " + name.lower()
        card_TITLE = "You've picked " + name.lower()
        return output_json_builder_with_reprompt_and_card(Probable_Place_List[name.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't reported this one before! Please let me know when you find it so I can help you better next time"
        reprompt_MSG = "Do you want to hear more about a particular items?"
        card_TEXT = "Use the full name."
        card_TITLE = "Wrong name."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def update_table(event):
    lostItem = event['request']['intent']['slots']['item']['value']
    foundPlace = event['request']['intent']['slots']['place']['value']
    Items_List.append(lostItem)
    Probable_Place_List[lostItem]=str("Your "+lostItem+" is most probably near the "+foundPlace)
    

    
    
    card_TEXT = "You've aded the item " + lostItem
    card_TITLE = "  "
    reprompt_MSG = "Your item has been successfully added : "+card_TEXT+" "+card_TITLE
    
    prompt = " "
    return output_json_builder_with_reprompt_and_card(reprompt_MSG, card_TEXT, card_TITLE,prompt, False)
    
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG =  " I will help you locate your most valuable things. To help me learn better, please report to me where you have previously lost an item.\
    If you would like to hear where the requested item is, you could say for example: Where is my pen?. Be sure to use the right name when asking about the item."
    reprompt_MSG = "If you want me to repeat it please say, help"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular items?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)


def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
