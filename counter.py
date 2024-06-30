import requests

TOKEN = 'YOUR TOKEN'
HEADERS = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}

def get_dms():
    url = "https://discord.com/api/v9/users/@me/channels"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to get DMs: {response.status_code}, {response.text}")
    return response.json()

def get_message_count(channel_id, limit=100):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    params = {
        'limit': limit
    }
    message_count = 0
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to get messages: {response.status_code}, {response.text}")
        batch = response.json()
        if not batch:
            break
        message_count += len(batch)
        if len(batch) < limit:
            break
        params['before'] = batch[-1]['id']
    return message_count

def main():
    try:
        dms = get_dms()
        dm_message_counts = []

        for dm in dms:
            if dm['type'] == 1:  # DM type 1 indicates a direct message
                channel_id = dm['id']
                recipient = dm['recipients'][0]['username']
                message_count = get_message_count(channel_id)
                print(f"DM with {recipient} (Channel ID: {channel_id}) scanned. Message count: {message_count}")

                dm_message_counts.append((recipient, message_count))

                print("=" * 50)  # Divider after each scanned DM

        print("All DMs have been scanned.")
        print("=" * 50)  # Divider before the sorted list

        # Sort by message count in descending order
        dm_message_counts.sort(key=lambda x: x[1], reverse=True)

        # Output the sorted list
        for idx, (recipient, count) in enumerate(dm_message_counts, start=1):
            print(f"{idx}. {recipient}: {count} messages")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
