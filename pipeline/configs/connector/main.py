import requests
import json

def create_connection(file_config:str):
    DEBEZIUM_SERVER_CONS = f"http://debezium-{file_config}:8083/connectors"
    print(f"🔗 Creating connection for {file_config} ...")
    with open(f"./registers/{file_config}.json") as f:
        connector_config = json.load(f)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(DEBEZIUM_SERVER_CONS, json=connector_config, headers=headers)
    if response.status_code == 201:
        print("✅ Connector created successfully!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    response = requests.get(DEBEZIUM_SERVER_CONS)
    print("All connectors:", end=" ")
    print(response.json())
    print("-"*100)

if __name__ == "__main__":
    create_connection("postgres")
    create_connection("mongo")

