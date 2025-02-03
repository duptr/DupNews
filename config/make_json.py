import os
import json

# Make sure that your categories are specific.
# (For example, when looking for news about Israel, news about "Israel Adesanya" should not appear among them).
# Also, ensure the freshness of your RSS sources."
# A few example topics and RSS sources are shown in the comment lines.
config = {
    "topics": [ 
        
        #"Gazze","Gaza", "USA","Turkey","Syria","Israel"
        #"politics","War","Military","Sanctions","Diplomacy"
                
                ],
    "rss_urls": [
        
        #"https://www.aljazeera.com/xml/rss/all.xml",
        #"https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        #"https://www.theguardian.com/world/rss"
    ]
}

# Get the directory where the make_config_json file is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the config.json file
config_file_path = os.path.join(current_dir, 'config.json')

# Create and save the config.json file
with open(config_file_path, 'w') as config_file:
    json.dump(config, config_file, indent=4)

print(f"Config file created at: {config_file_path}")