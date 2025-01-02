import openai
from django.conf import settings

def generate_tags(title, description):
    """
    Generate tags for an item based on its title and description using OpenAI's API.
    Returns a list of tag names.
    """
    try:
        if not settings.OPENAI_API_KEY:
            return []
            
        openai.api_key = settings.OPENAI_API_KEY
        
        system_prompt = "You are a helpful assistant that generates relevant tags for lost and found items. Return only the tags separated by commas, without explanations or additional text."
        user_prompt = f"""Given the following lost/found item details, generate relevant tags.
        Title: {title}
        Description: {description}
        
        Generate up to 5 relevant tags that describe key characteristics like color, type, material, brand, or category.
        Format: red, leather, wallet, gucci, accessories"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        tags_text = response.choices[0].message.content.strip()
        return [tag.strip().lower() for tag in tags_text.split(',')]
            
    except Exception:
        return [] 