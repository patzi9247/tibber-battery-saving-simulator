import requests

def get_home_id(TIBBER_TOKEN):
    query = """
    {
    viewer {
        homes {
        id
        appNickname
        address {
            address1
            postalCode
            city
            country
        }
        }
    }
    }
    """

    response = requests.post(
        "https://api.tibber.com/v1-beta/gql",
        headers={"Authorization": f"Bearer {TIBBER_TOKEN}"},
        json={"query": query}
    )

    data = response.json()

    return_data = []

    for home in data["data"]["viewer"]["homes"]:
        tmp_data = {
            'home_id': home['id'],
            'home_name': home['appNickname'],
            'address': f"{home['address']['address1']}, {home['address']['postalCode']} {home['address']['city']}"
        }
        return_data.append(tmp_data)
    
    return return_data