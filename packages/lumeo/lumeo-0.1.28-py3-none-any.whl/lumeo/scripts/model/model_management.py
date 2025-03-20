import argparse
import getpass
import json
import requests
import subprocess


# Connects to all gateways in the JSON file over SSH.
# Runs the specified command inside the gateway container for each combination of gateway and model in the config.
# MODEL_ID argument is replaced with the actual model ID from the config file.
#
# Examples:
# $ pipx run --spec . --no-cache lumeo-model-management config.json engine-cache list --model-id MODEL_ID
# $ pipx run --spec . --no-cache lumeo-model-management config.json engine-cache create --model-id MODEL_ID
# $ pipx run --spec . --no-cache lumeo-model-management config.json engine-cache create --model-id MODEL_ID --force
#
# JSON format:
# {
#   "gateways": [
#     {
#       "ssh": "root@gateway_host",
#       "container_name": "lumeo-gateway-container"
#     }
#   ],
#   "models": [
#     {
#       "id": "00000000-0000-0000-0000-000000000000"
#     }
#   ]
# }
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="JSON file with gateways and models")
    parser.add_argument("command", help="Command to run for each gateway/model combination", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    environment, api_token = login()

    for gateway in config["gateways"]:
        for model in config["models"]:
            print(f"###")
            print(f"### Running command on {gateway['ssh']}. Model ID: {model['id']}")
            print(f"###")

            # Print lumeod version
            subprocess.run(["ssh", gateway["ssh"],
                            "docker", "exec",
                            gateway["container_name"],
                            "lumeod", "--version"])

            # Run the `create-engine-cache` command inside the gateway container.
            lumeod_command = ["ssh", gateway["ssh"],
                              "docker", "exec",
                              "--env", "LUMEO_ENVIRONMENT=" + environment,
                              "--env", "LUMEO_API_KEY=" + api_token,
                              "--env", "RUST_LOG=info",
                              gateway["container_name"],
                              "lumeod", "model"]

            # Replace occurrences of `MODEL_ID` argument with the actual model ID.
            # Make a copy of the command to avoid modifying the original list.
            execution_command = args.command.copy()
            for i, arg in enumerate(execution_command):
                if arg == "MODEL_ID":
                    execution_command[i] = model["id"]

            lumeod_command.extend(execution_command)

            subprocess.run(lumeod_command)


# It asks for the username and password, and returns the JWT token.
def login():
    environment = input("Lumeo environment (d/s/p): ")

    if environment in ["development", "dev", "d"]:
        base_url = "https://api-dev.lumeo.com"
        environment = "development"
    elif environment in ["staging", "s"]:
        base_url = "https://api-staging.lumeo.com"
        environment = "staging"
    elif environment in ["production", "prod", "p"]:
        base_url = "https://api.lumeo.com"
        environment = "production"
    else:
        print(f"Invalid environment: {environment}")
        return None

    email = input("Email: ")
    password = getpass.getpass("Password: ")

    response = requests.post(f"{base_url}/v1/internal/auth/login", json={
        "email": email,
        "password": password
    })

    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        return None

    return environment, response.json()["token"]


if __name__ == "__main__":
    main()
