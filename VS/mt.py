import requests

def translate_text(source, target, text):
    """
    Translates text from one language to another using a POST request, where the text is sent as plain text in the body and the language codes are in the parameters.

    Args:
        source (str): The source language code.
        target (str): The target language code.
        text (str): The text to be translated.

    Returns:
        str: The translated text if successful, or an error message.
    """
    # Define the API URL
    api_url = "https://translator-api.glosbe.com/translateByLangDetect"
    if source == "yor":
        source = "yo"
    if target == "yor":
        target = "yo"

    # Validate the language codes
    valid_langs = ['yo', 'fr', 'en', 'fon']
    if source not in valid_langs or target not in valid_langs:
        return "Invalid language code. Please use one of the following: 'yor', 'fr', 'en', 'fon'."


    # Prepare the parameters for the request
    params = {
        'sourceLang': source,
        'targetLang': target
    }

    # Prepare the headers for the request indicating plain text is being sent
    headers = {
        'Content-Type': 'text/plain'
    }

    # Make the POST request to the API, sending the text directly in the body
    response = requests.post(api_url, params=params, data=text, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        print(response_data)

        # Check if the translation was successful
        if 'translation' in response_data:
            return response_data['translation'] + '\n'
        else:
            return "Translation failed. Please check the input."
    else:
        return f"Failed to connect to the translation service. Status code: {response.status_code}"


# Example usage
#translated_text = translate_text('fr', 'fon', 'Imbécile, tu mens trop')
#print(translated_text)