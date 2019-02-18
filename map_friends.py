import folium
import twitter2

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def main():
    acc = input('Enter account name:')
    data = twitter2.read_data(twitter2.get_json_data(acc))
    useful_data = parse_data(data)
    map1 = folium.Map()
    map1.add_child(add_second_layer(useful_data))
    map1.add_child(folium.LayerControl())
    map1.save('Map_twitter.html')


def parse_data(data):
    new_dict = dict()
    for item in data['locations']:
        if item[1] in new_dict.keys():
            new_dict[item[1]].append(item[0])
        else:
            new_dict[item[1]] = [item[0]]
    return new_dict


def get_coordinates(location):
    geolocator = Nominatim(user_agent="web_map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
    coordinate = geolocator.geocode(location)
    return [coordinate.latitude, coordinate.longitude]


def add_second_layer(data):
    fg = folium.FeatureGroup(name="Name")
    for each in data:
        try:
            fg.add_child(folium.Marker(location=get_coordinates(each), popup=data[each], icon=folium.Icon(icon='cloud')))
        except:
            continue
    return fg

# if __name__ == '__main__':
#     main()

