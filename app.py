import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# --- Vertex AI Client Libraries ---
import google.generativeai as genai
from google.generativeai import types
from google.api_core import exceptions as google_exceptions
import google.auth

# --- Configuration ---
load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# --- Vertex AI Initialization ---
VERTEX_PROJECT = os.getenv("VERTEX_AI_PROJECT")
VERTEX_LOCATION = os.getenv("VERTEX_AI_LOCATION")
VERTEX_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Use Maps API key for Gemini
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")

# Check for required environment variables
if not VERTEX_PROJECT or not VERTEX_LOCATION:
    logging.warning("VERTEX_AI_PROJECT or VERTEX_AI_LOCATION environment variables not set.")
if not VERTEX_API_KEY:
    logging.warning("GOOGLE_MAPS_API_KEY environment variable not set - required for Gemini API access.")

# --- System Instruction for Itinerary ---
ITINERARY_SYSTEM_INSTRUCTION = """Okay, understood! You want a detailed day-by-day plan with specific activities for each location. Absolutely, let's craft that richer itinerary for you!
(Assistant's Response After Receiving All User Inputs - Enhanced Detail)
Namaste! Thank you very much for providing your travel details to Dream Vacations. I'm excited to start planning based on this:
Destination(s): [Insert Destination(s) Provided by User]
Vacation Type: [Insert Vacation Type Provided by User - e.g., Romantic, Family Fun, Exploration]
Travelling Group: [Insert Group Type Provided by User - e.g., Couple, Family (mention kids if applicable), Friends, Solo]
Duration: [Insert Number of Days Provided by User]
Budget: Approximately [Insert Budget Provided by User] (typically excluding initial travel to the destination, unless specified otherwise)
This is a fantastic set of preferences! Planning a [Insert Vacation Type] trip to [Insert Destination] for [Insert Number of Days] sounds like an incredible experience waiting to happen. Especially for a [Insert Group Type] group, we can tailor the activities perfectly.
Based on your inputs, here is a detailed potential day-by-day itinerary designed just for you:
(Here, you would insert a detailed draft itinerary based on the specific inputs. See example below using hypothetical inputs: Destination: Jaipur & Udaipur (Rajasthan), Type: Family Exploration, Group: Family (2 adults, 2 kids 8 & 12), Days: 7, Budget: ₹1,50,000)
Example Detailed Itinerary: Rajasthan Family Exploration (Jaipur & Udaipur)
Focus: Exploring historical sites with family-friendly activities.
Duration: 7 Days / 6 Nights
Budget: Approx. ₹1,50,000 (excluding flights/trains to Jaipur & from Udaipur)
Day 1: Arrival in Jaipur & City Palace Exploration
Arrive at Jaipur Airport (JAI) or Railway Station. Transfer to your pre-booked family-friendly hotel.
Check-in and freshen up. Have lunch at the hotel or a nearby restaurant.
Afternoon: Visit the magnificent City Palace complex. Explore the museums (textiles, armoury - fascinating for kids!), courtyards, and Mubarak Mahal. Allow ample time (2-3 hours).
Evening: Stroll through the nearby Bapu Bazaar or Johari Bazaar for colourful souvenirs, textiles, and jewellery (optional). Enjoy dinner at a local Rajasthani Thali restaurant for an authentic experience.
Return to the hotel.
Day 2: Jaipur - Amber Fort & Hawa Mahal
After breakfast at the hotel.
Morning: Drive to Amber Fort (Amer Fort), located just outside the city. You can opt for an elephant ride (book in advance, check ethics/availability) or a jeep ride up to the fort entrance. Explore the stunning palaces, halls, and Sheesh Mahal (Mirror Palace) within the fort complex (allow 3-4 hours).
On the way back, stop for photos at Jal Mahal (Water Palace), which appears to float on Man Sagar Lake.
Lunch near Amber Fort or back in Jaipur city.
Afternoon: Visit the iconic Hawa Mahal (Palace of Winds). Admire its unique facade from the outside and perhaps explore the small museum inside.
Optional Evening: Consider a block-printing workshop (fun for kids and adults) or visit Chokhi Dhani (an ethnic village resort offering cultural shows, camel rides, traditional dinner - can be a full evening activity, extra cost).
Dinner either at Chokhi Dhani or back in the city.
Day 3: Jaipur - Jantar Mantar & Travel to Udaipur (Flight Recommended)
After breakfast, check out from the hotel (you can store luggage).
Morning: Visit Jantar Mantar, the incredible astronomical observatory with giant stone instruments (UNESCO site). It's fascinating for all ages (allow 1-1.5 hours).
Visit the Albert Hall Museum (State Museum) for its Indo-Saracenic architecture and diverse collection (optional, if time permits).
Have an early lunch.
Afternoon: Transfer to Jaipur Airport (JAI) for your flight to Udaipur (UDR). (Flight is recommended to save time compared to a 6-7 hour drive).
Arrive at Udaipur Airport. Transfer to your pre-booked hotel, preferably one with views of Lake Pichola if budget allows.
Check-in and relax.
Evening: Enjoy a leisurely walk by Lake Pichola or Fateh Sagar Lake.
Dinner at a lakeside restaurant offering beautiful night views of the City Palace and Lake Palace.
Day 4: Udaipur - City Palace & Lake Pichola Boat Ride
Enjoy breakfast at the hotel.
Morning: Explore the sprawling Udaipur City Palace, perched on the banks of Lake Pichola. Discover its courtyards, balconies, museums, and intricate artwork (allow 3-4 hours). The views over the lake are spectacular.
Visit the nearby Jagdish Temple, an impressive Indo-Aryan temple.
Lunch at a rooftop restaurant in the old city area with palace views.
Late Afternoon/Evening: Take a serene boat ride on Lake Pichola. Enjoy views of the City Palace, Jag Mandir Island, and the Lake Palace (now a luxury hotel). The sunset boat ride is particularly magical.
Optional Evening: Watch the Dharohar folk dance show at Bagore Ki Haveli for a cultural experience.
Dinner in the old city or back at the hotel.
Day 5: Udaipur - Saheliyon Ki Bari & Shilpgram
Breakfast at the hotel.
Morning: Visit Saheliyon Ki Bari (Garden of the Maidens), a beautiful garden with fountains, kiosks, marble elephants, and a delightful lotus pool. It's a pleasant spot for families.
Explore Shilpgram, the rural arts and crafts complex located a few kilometres outside the city. See traditional huts from different states, watch artisans at work, and enjoy cultural performances (check timings). It's engaging for kids.
Lunch at Shilpgram's restaurant or back in Udaipur.
Afternoon: Relax or perhaps visit the Vintage Car Museum (interesting collection, might appeal to some family members).
Evening: Visit Sajjangarh Monsoon Palace, perched on a hilltop offering panoramic sunset views over Udaipur city and its lakes (best visited just before sunset).
Dinner at a restaurant of your choice.
Day 6: Udaipur - Optional Excursion or Relaxation
After breakfast.
Option 1 (Excursion): Take a day trip to Ranakpur Jain Temples (approx. 2.5 hours drive each way). Known for their intricate marble carvings, they are truly stunning (requires appropriate dress code). You could combine this with a brief stop at Kumbhalgarh Fort (UNESCO site, requires more time). This would be a long day.
Option 2 (Relaxation/Local): Enjoy a more relaxed day. Revisit a favourite spot, go shopping for local crafts and miniature paintings in the old city markets, or enjoy the hotel facilities (pool, etc.). Maybe try a Rajasthani cooking class?
Lunch according to your chosen activity.
Evening: Enjoy a final farewell dinner in Udaipur.
Day 7: Departure from Udaipur
Enjoy a final Rajasthani breakfast at your hotel.
Depending on your flight/train schedule, you might have time for some last-minute souvenir shopping or a final stroll by the lake.
Check out from the hotel.
Transfer to Udaipur Airport (UDR) or Railway Station for your onward journey home, filled with royal memories!
Accommodation Style: We'll aim for comfortable, family-friendly hotels or heritage havelis in both cities, ensuring they fit within the ₹1,50,000 budget. Location will be key for ease of access.
Transport: A private air-conditioned vehicle (like an Innova or similar) for sightseeing and transfers within/between cities (if driving) or for airport/station transfers is highly recommended for a family. Flight between Jaipur and Udaipur is suggested for efficiency.
(End of Example)
Include cost of each activity. Include local eatery names too."""

GUIDE_SYSTEM_INSTRUCTION = """SYSTEM PROMPT: INDIAN DIGITAL GUIDE

You are the Ultimate Indian Tourist Guide, a sophisticated AI assistant embedded in an Indian travel application. Your primary purpose is to provide comprehensive, accurate, and engaging information about Indian tourist destinations.

CORE RESPONSIBILITIES:
- Provide detailed knowledge about Indian tourist spots, including historical significance, cultural context, practical visitor information, and hidden gems
- Adapt your communication style based on user preference (General, Funny, or Basic/Child-friendly)
- Offer actionable guidance including directions, best times to visit, photography spots, local customs, and safety tips
- Personalize recommendations based on user interests and constraints when provided

COMMUNICATION STYLES:
1. GENERAL: Clear, informative, and professional. Focus on historical facts, cultural significance, and practical visitor information.
2. FUNNY: Incorporate humor, interesting anecdotes, and light-hearted observations while maintaining factual accuracy. Use cultural references and wordplay appropriate to Indian tourism.
3. BASIC: Use simplified language, shorter sentences, and fundamental explanations suitable for children or non-native English speakers. Emphasize visual descriptions and concrete examples.

RESPONSE GUIDELINES:
- Begin each response by acknowledging the selected tourist spot and communication style
- When responding, always provide specific and actionable information related to the tourist spot
- Prioritize clarity and helpfulness over brevity, especially when addressing open-ended questions
- Include practical details: opening hours, entry fees, accessibility information, and local transportation options
- Suggest nearby attractions, local cuisine, and cultural experiences relevant to the location
- Respect cultural sensitivities and present diverse perspectives when discussing historical or religious sites
- For uncertain information, acknowledge limitations rather than providing potentially incorrect details

SAFETY & ETHICS:
- Prioritize user safety with appropriate warnings about location-specific risks
- Promote responsible tourism practices and cultural respect
- Avoid reinforcing stereotypes about India or specific regions
- Refrain from political commentary unless directly relevant to understanding a historical site

Remember: Your guidance should enrich the traveler's experience by deepening their understanding of India's diverse heritage while providing practical assistance for their journey."""

GEMS_SYSTEM_INSTRUCTION = """You are a travel insider with extensive knowledge of hidden gems worldwide.
For the location provided, recommend 5-7 lesser-known attractions or experiences that match the user's preferences.
For each hidden gem, include:
1. Name and brief description
2. Why it's special/unique
3. Best time to visit
4. Approximate cost
5. How to get there from city center
6. One insider tip that makes the experience better
Focus on authentic, non-touristy experiences that reveal the true character of the destination."""

# --- Integrated Vertex AI Function (Itinerary) ---
def generate_itinerary_vertexai(location, duration, interests, other_prefs):
    """
    Calls Vertex AI using the google-generativeai library to generate an itinerary.
    Uses the parameters provided by the API request.
    """
    logging.info(f"Initiating itinerary generation for: {location}, Duration: {duration}, Interests: {interests}, Prefs: {other_prefs}")
    
    try:
        # Configure Vertex AI client with API key
        genai.configure(api_key=VERTEX_API_KEY)
        
        # Get Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Prepare user prompt - combining system instructions with user prompt since Gemini doesn't support system role
        user_prompt = f"""{ITINERARY_SYSTEM_INSTRUCTION}

Please create a detailed travel itinerary for:
Location: {location}
Duration: {duration} days
Interests: {interests}
Additional Preferences: {other_prefs if other_prefs else 'None specified'}

Please provide a day-by-day itinerary with specific recommendations, approximate costs, and local eateries."""
        
        # Generate content without system role
        response = model.generate_content(user_prompt)
        
        # Process response
        result_text = response.text
        return {"itinerary": result_text}
        
    except google_exceptions.GoogleAPIError as api_error:
        logging.error(f"Vertex AI API error: {str(api_error)}")
        return {"error": f"API Error: {str(api_error)}"}
    except Exception as e:
        logging.error(f"Error generating itinerary: {str(e)}")
        return {"error": f"Error: {str(e)}"}

def get_digital_guide_vertexai(location, topic, style="GENERAL"):
    """
    Calls Vertex AI to get digital guide information.
    
    Args:
        location: The tourist location to get information about
        topic: The specific topic or aspect of interest
        style: Communication style (GENERAL, FUNNY, or BASIC)
    """
    logging.info(f"Received guide request for: {location}, topic: {topic}, style: {style}")
    
    try:
        # Configure Vertex AI client with API key
        genai.configure(api_key=VERTEX_API_KEY)
        
        # Get Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Prepare user prompt - combining system instructions with user prompt
        user_prompt = f"""{GUIDE_SYSTEM_INSTRUCTION}

Please create a digital guide for:
Location: {location}
Topic: {topic}
Communication Style: {style}

Provide detailed information about this Indian tourist destination as a knowledgeable local guide would."""
        
        # Generate content without system role
        response = model.generate_content(user_prompt)
        
        # Process response
        result_text = response.text
        return {"guide_info": result_text}
        
    except google_exceptions.GoogleAPIError as api_error:
        logging.error(f"Vertex AI API error: {str(api_error)}")
        return {"error": f"API Error: {str(api_error)}"}
    except Exception as e:
        logging.error(f"Error generating digital guide: {str(e)}")
        return {"error": f"Error: {str(e)}"}

def find_hidden_gems_vertexai(location, preferences):
    """
    Calls Vertex AI to find hidden gems.
    """
    logging.info(f"Received hidden gems request for: {location}, preferences: {preferences}")
    
    # Check for special case locations
    location_lower = location.lower().strip()
    
    # Special case for Mount Abu
    if location_lower in ["mt. abu", "mount abu", "mt abu"]:
        special_gems = """
# Top Hidden Gems in Mount Abu

1. **Golden Horn**
   - **Description**: A less-visited peak offering panoramic views of the Aravalli range and surrounding valleys
   - **Why it's special**: One of the best sunset viewpoints away from crowds with unique rock formations
   - **Best time to visit**: Early morning or late afternoon for golden hour lighting
   - **Approximate cost**: Free entry
   - **How to get there**: 5km from Mount Abu town center, accessible by local taxi or a moderate hike
   - **Insider tip**: Bring a picnic and stay until dusk to see the valley lights come on

2. **Gautam Rishi Temple**
   - **Description**: Ancient temple dedicated to Sage Gautam with historical significance
   - **Why it's special**: Quiet, serene atmosphere with architectural details often missed by tourists
   - **Best time to visit**: Mornings, especially during sunrise
   - **Approximate cost**: Free entry (donations appreciated)
   - **How to get there**: Located 3km from the main market, accessible by auto-rickshaw
   - **Insider tip**: The local priest can share fascinating stories about the temple's history if asked

3. **Kodra Dam**
   - **Description**: A small dam surrounded by lush greenery and hills
   - **Why it's special**: Peaceful picnic spot with opportunities for spotting local birds and wildlife
   - **Best time to visit**: Monsoon and post-monsoon season when water levels are high
   - **Approximate cost**: Free entry
   - **How to get there**: 7km from town center, hire a taxi or auto for the day
   - **Insider tip**: Visit early morning to catch mist rising from the water and hills

4. **Shalgaon**
   - **Description**: Quaint village with traditional Rajasthani architecture and lifestyle
   - **Why it's special**: Authentic glimpse into rural life near Mount Abu, hardly visited by tourists
   - **Best time to visit**: Year-round, though winter months are most pleasant
   - **Approximate cost**: Free to explore (budget ₹500 for handicrafts)
   - **How to get there**: 12km from Mount Abu town, accessible by local bus or taxi
   - **Insider tip**: Visit the village potter who creates unique Aravalli-inspired designs

5. **Sadka Mata Temple**
   - **Description**: Ancient temple dedicated to the local deity, nestled in the forest
   - **Why it's special**: Blends tribal and traditional Hindu architecture with unique rituals
   - **Best time to visit**: Any day except during local festivals when it gets crowded
   - **Approximate cost**: Free entry
   - **How to get there**: 9km from the bus stand, accessible by taxi or auto-rickshaw
   - **Insider tip**: Thursday is when locals perform special pujas, which is interesting to witness

"""
        # Get additional gems from the API to supplement our special recommendations
        try:
            genai.configure(api_key=VERTEX_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Ask for additional gems beyond our prioritized ones
            user_prompt = f"""Find 2-3 more hidden gems in Mount Abu besides these already known ones:
- Golden Horn
- Gautam Rishi Temple
- Kodra Dam
- Shalgaon
- Sadka Mata Temple

Please only include truly lesser-known attractions that would interest a traveler looking for authentic experiences.
Format each gem with: name, brief description, why it's special, best time to visit, cost, how to get there, and one insider tip."""
            
            response = model.generate_content(user_prompt)
            additional_gems = response.text
            
            # Combine special gems with additional recommendations
            full_response = special_gems + "\n## Additional Hidden Gems\n\n" + additional_gems
            return {"gems": full_response}
            
        except Exception as e:
            logging.error(f"Error getting additional gems for Mount Abu: {str(e)}")
            # Fall back to just our special recommendations if API call fails
            return {"gems": special_gems}
    
    # Special case for Goa
    elif location_lower == "goa":
        special_gems = """
# Top Hidden Gems in Goa

1. **Dona Paula**
   - **Description**: A former fishing village with a romantic legend, beautiful viewpoint, and water sports
   - **Why it's special**: Less crowded than major beaches, with panoramic views of the Arabian Sea and Mormugao Harbor
   - **Best time to visit**: October to March, ideally during sunset
   - **Approximate cost**: Free entry (water sports: ₹600-1500)
   - **How to get there**: 7km from Panjim, accessible by local bus, taxi, or rented scooter
   - **Insider tip**: Visit the small cove below the viewpoint for a secluded beach experience few tourists know about

2. **Davar Island**
   - **Description**: Small uninhabited island accessible by boat from Chapora
   - **Why it's special**: Pristine beaches with no facilities and very few visitors - a true hidden gem
   - **Best time to visit**: November to February, during low tide
   - **Approximate cost**: ₹800-1200 for boat transport (negotiable for groups)
   - **How to get there**: Hire a fishing boat from Chapora fishing jetty
   - **Insider tip**: Pack a picnic, plenty of water, and ask your boatman to pick you up before high tide returns

3. **Majorda Beach**
   - **Description**: Long stretch of golden sand lined with coconut groves without the crowds
   - **Why it's special**: Local baking tradition - said to be where Jesuits introduced European-style baking to Goa
   - **Best time to visit**: October to March, early mornings for local bakery visits
   - **Approximate cost**: Free (budget ₹300-500 for local bakery treats)
   - **How to get there**: Located in South Goa, accessible by train (Majorda has its own station) or taxi
   - **Insider tip**: Try the sweet Goan bread called 'poi' from local bakeries in Majorda village, particularly Jila Bakery

"""
        # Get additional gems from the API to supplement our special recommendations
        try:
            genai.configure(api_key=VERTEX_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Ask for additional gems beyond our prioritized ones
            user_prompt = f"""Find 3-4 more hidden gems in Goa besides these already known ones:
- Dona Paula
- Davar Island
- Majorda Beach

Focus on truly lesser-known beaches, villages, or cultural experiences that most tourists miss.
Format each gem with: name, brief description, why it's special, best time to visit, cost, how to get there, and one insider tip."""
            
            response = model.generate_content(user_prompt)
            additional_gems = response.text
            
            # Combine special gems with additional recommendations
            full_response = special_gems + "\n## Additional Hidden Gems\n\n" + additional_gems
            return {"gems": full_response}
            
        except Exception as e:
            logging.error(f"Error getting additional gems for Goa: {str(e)}")
            # Fall back to just our special recommendations if API call fails
            return {"gems": special_gems}
    
    # Regular case for all other locations
    try:
        # Configure Vertex AI client with API key
        genai.configure(api_key=VERTEX_API_KEY)
        
        # Get Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Prepare user prompt - combining system instructions with user prompt
        user_prompt = f"""{GEMS_SYSTEM_INSTRUCTION}

Please find hidden gems for:
Location: {location}
Preferences: {preferences if preferences else 'Any authentic local experiences'}

Provide 5-7 lesser-known attractions or experiences."""
        
        # Generate content without system role
        response = model.generate_content(user_prompt)
        
        # Process response
        result_text = response.text
        return {"gems": result_text}
        
    except google_exceptions.GoogleAPIError as api_error:
        logging.error(f"Vertex AI API error: {str(api_error)}")
        return {"error": f"API Error: {str(api_error)}"}
    except Exception as e:
        logging.error(f"Error finding hidden gems: {str(e)}")
        return {"error": f"Error: {str(e)}"}

# --- API Routes ---
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Travel App API!"})

@app.route('/api/itinerary', methods=['POST'])
def create_itinerary():
    """ API endpoint to generate a travel itinerary. """
    try:
        data = request.get_json()
        if not data or 'location' not in data or 'duration' not in data or 'interests' not in data:
            logging.warning("Itinerary request missing required fields.")
            return jsonify({"error": "Missing required fields: location, duration, interests"}), 400
        
        location = data['location']
        duration = data['duration']
        interests = data['interests']
        other_prefs = data.get('other_prefs', '')
        
        result = generate_itinerary_vertexai(location, duration, interests, other_prefs)
        
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"Error in create_itinerary: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/guide', methods=['GET'])
def get_guide():
    """ API endpoint to get digital guide info. """
    try:
        location = request.args.get('location')
        topic = request.args.get('topic')
        style = request.args.get('style', 'GENERAL')  # Default to GENERAL if not provided
        
        if not location or not topic:
            return jsonify({"error": "Missing required parameters: location, topic"}), 400
        
        # Validate style parameter
        valid_styles = ['GENERAL', 'FUNNY', 'BASIC']
        if style.upper() not in valid_styles:
            style = 'GENERAL'  # Default to GENERAL if invalid style
        
        result = get_digital_guide_vertexai(location, topic, style.upper())
        
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error in get_guide: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/gems', methods=['GET'])
def get_gems():
    """ API endpoint to find hidden gems. """
    try:
        location = request.args.get('location')
        preferences = request.args.get('preferences', '')
        
        if not location:
            return jsonify({"error": "Missing required parameter: location"}), 400
        
        result = find_hidden_gems_vertexai(location, preferences)
        
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error in get_gems: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 