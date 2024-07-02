import re
from .extract_locations import extract_locations, get_lat_long
from transformers import pipeline, TFAutoModelForSequenceClassification, AutoTokenizer

# Expanded lists of stations and keywords
stations_western = [
    "Churchgate", "Marine Lines", "Grant Road", "Charni Road", "Mumbai Central", "Mahalaxmi", 
    "Lower Parel", "Elphinstone Road", "Dadar", "Matunga Road", "Mahim", "Bandra", "Khar Road",
    "Santacruz", "Vile Parle", "Andheri", "Jogeshwari", "Goregaon", "Malad", "Kandivali", 
    "Borivali", "Dahisar", "Mira Road", "Bhayandar", "Naigaon", "Vasai Road", "Nalasopara", "Virar"
]
stations_eastern = [
    "CST", "Masjid", "Sandhurst Road", "Byculla", "Chinchpokli", "Currey Road", "Parel", 
    "Dadar", "Matunga", "Sion", "Kurla", "Vidyavihar", "Ghatkopar", "Vikhroli", "Kanjurmarg", 
    "Bhandup", "Nahur", "Mulund", "Thane", "Kalwa", "Mumbra", "Diva", "Kopar", "Dombivli", "Thakurli", 
    "Kalyan", "Shahad", "Ambivli", "Titwala", "Khadavli", "Vasind", "Asangaon", "Atgaon", "Kasara"
]
stations_harbour = [
    "CST", "Masjid", "Sandhurst Road", "Dockyard Road", "Reay Road", "Cotton Green", "Sewri", "Wadala Road",
    "GTB Nagar", "Chunabhatti", "Kurla", "Tilak Nagar", "Chembur", "Govandi", "Mankhurd", "Vashi", 
    "Sanpada", "Juinagar", "Nerul", "Seawoods", "Belapur", "Kharghar", "Mansarovar", "Khandeshwar", "Panvel"
]

keyaddwords = [
    "Park", "Chowk", "Marg", "Bridge", "Tower", "Building", "Road", "Nagar", "Compound", "Cinema",
    "Talkies", "Link", "Market", "Street", "Colony", "Apartment", "School", "College", "Crossroad", 
    "Intersection", "Ground", "Drive", "Highway", "St", "Gully", "Rasta", "Station", "Udyan", "Signal", 
    "Mohalla", "Chawl", "Shop", "Bar", "Express", "Lake", "River", "Estate", "Rail", "Church", 
    "Masjid", "Temple", "Mandir", "Society", "Hotel", "Subway", "Flyover", "Underpass", "Pole", "Circle",
    "Gardens", "Lane", "Plaza", "Square", "Boulevard", "Avenue", "Court", "Terrace", "Heights", "Meadow", 
    "Terrace", "Garden", "Grove", "Meadow", "View", "Way", "Crescent", "Trail", "Place", "Parkway", 
    "Broadway", "Mall", "Esplanade", "Crescent", "Walk", "Driveway", "Turn", "Rise", "Path", "Close", 
    "Court", "Field", "Mount", "Court", "Glade", "Croft", "Mews", "Dell", "Valley"
]

all_keywords = stations_western + stations_eastern + stations_harbour + keyaddwords
pattern = re.compile(r"\b(?:{})\b".format("|".join(all_keywords)), re.IGNORECASE)

# Initialize the sentiment analysis pipeline
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, framework="tf")

def process_tweet(tweet):
    locations = extract_locations(tweet, pattern)
    location_coords = {loc: get_lat_long(loc) for loc in locations}
    
    sentiment = sentiment_pipeline(tweet)[0]
    
    return [{"text": tweet, "locations": [loc for loc in locations if location_coords[loc]], "sentiment": sentiment}]
