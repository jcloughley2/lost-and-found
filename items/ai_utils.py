from django.conf import settings
from openai import OpenAI
import weave
import base64
import logging

logger = logging.getLogger(__name__)

# Initialize Weave project
weave.init('lost-and-found-tags')

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@weave.op()
def generate_tags(title: str, description: str) -> list:
    """
    Generate tags for an item based on its title and description using OpenAI's API.
    Returns a list of tag names.
    """
    try:
        if not settings.OPENAI_API_KEY:
            return []
        
        system_prompt = "You are a helpful assistant that generates relevant tags for lost and found items. Return only the tags separated by commas, without explanations or additional text."
        user_prompt = f"""Given the following lost/found item details, generate relevant tags.
        Title: {title}
        Description: {description}
        
        Generate up to 5 relevant tags that describe key characteristics like color, type, material, brand, or category.
        Format: red, leather, wallet, gucci, accessories"""

        response = client.chat.completions.create(
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
            
    except Exception as e:
        logger.error(f"Error generating tags: {str(e)}")
        return []
    



@weave.op()
def analyze_image(image) -> tuple:
    """
    Use OpenAI's vision model to analyze the image and generate title and description suggestions.
    Returns a tuple of (title, description).
    """
    try:
        if not settings.OPENAI_API_KEY:
            return "No OpenAI API Key", "Please configure your OpenAI API Key"

        # Read and encode the image
        base64_image = base64.b64encode(image.read()).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this image and provide:\n1. A brief, descriptive title (max 5 words)\n2. A detailed description of the item's appearance, including color, size, condition, and any distinctive features."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        logger.debug("OpenAI API Response received")
        logger.debug(f"Response content: {response.choices[0]}")

        # Parse the response
        result = response.choices[0].message.content
        logger.debug(f"Raw response content: {result}")

        # Split into title and description
        parts = result.split('\n', 1)
        if len(parts) == 2:
            # Clean up title - remove number prefix, "Title:", asterisks and any extra whitespace
            title = parts[0].replace('1.', '').replace('Title:', '').replace('*', '').strip()
            # Clean up description - remove number prefix, "Description:", asterisks and any extra whitespace
            description = parts[1].replace('2.', '').replace('Description:', '').replace('*', '').strip()
            logger.debug(f"Parsed title: {title}")
            logger.debug(f"Parsed description: {description}")
        else:
            title = "Item Title"
            description = result.strip().replace('*', '')
            logger.debug("Failed to split response into title and description")

        return title, description

    except Exception as e:
        logger.error(f"Error analyzing image with OpenAI: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return "Error Processing Image", f"There was an error processing the image: {str(e)}. Please try again or enter details manually."
