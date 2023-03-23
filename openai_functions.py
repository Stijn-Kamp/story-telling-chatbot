import openai
from utilities import get_token

openai.organization = "org-yTnKcEYXKSAXPU4wcEqibe9c"
openai.api_key = get_token("OPENGBT_TOKEN")
openai.Model.list()


def generate_text(role:str, prompt:str, blacklist: list = []):
    """
    Generates a text based on a specific prompt.
    Returns a generated etxt based on the prompt given. If no text could be generated or if blacklisted words were found, None is returned instead.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt},
                ]
        )
    except:
        return None

    result = ''
    for choice in response.choices:
        result += choice.message.content
    
    # Filter out the blacklisted words and phrases
    for blacklist_item in blacklist:
        if blacklist_item in result:
            return None
    
    return result