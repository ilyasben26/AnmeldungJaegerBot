def check_availability(data):
  city_available_map = {}

  for entry in data:
    city = entry['city']
    available = entry['available']
  
    if city not in city_available_map:
      city_available_map[city] = available
    else:
      city_available_map[city] = city_available_map[city] or available

  result = []
  for city, available in city_available_map.items():
    if available:
      result.append({'city': city, 'send_msg_flag': True})
    else:
      result.append({'city': city, 'send_msg_flag': False})

  return result


def get_city_emoji(city_name):
  city_emojis = {
    "Bremen": "🔑",
    "Berlin": "🌆",
  }
  return city_emojis.get(city_name, "🏙️")


def format_data(data):
  city_summaries = {}

  for entry in data:
    city = entry["city"]
    place = entry["place"]
    service = entry["service"]
    available = entry["available"]
    link = entry["link"]  

    if city not in city_summaries:
      city_summaries[city] = {"available_services": [], "places": {}}

    if place not in city_summaries[city]["places"]:
      city_summaries[city]["places"][place] = []

    city_summaries[city]["places"][place].append((service, available, link)) 

    if available:
      city_summaries[city]["available_services"].append(service)

  output = ""
  for city, city_data in city_summaries.items():
    city_role_mention = f"@{city}" if city_data[
      "available_services"] else ""
    city_emoji = get_city_emoji(city)
    output += f"# {city_emoji} {city_role_mention}\n"
    for place, services in city_data["places"].items():
      output += f"- ***{place}***:\n"
      for service, available, link in services: 
        if available:
          book_now = f"[book now]({link})"
          status = "✅"
        else:
          status = "❌"
          book_now = ""
        output += f" - {status} {service} {book_now}\n"
    output += "\n"

  return output

