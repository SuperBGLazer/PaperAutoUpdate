import json

import requests
import os


class Config:
    def __init__(self, minecraft_version: str):
        self.minecraft_version = minecraft_version

class Change:
    def __init__(self, commit, summary, message):
        self.commit = commit
        self.summary = summary
        self.message = message


class Download:
    def __init__(self, name, sha256):
        self.name = name
        self.sha256 = sha256


class Build:
    def __init__(self, build, time, channel, promoted, changes, downloads):
        self.build = build
        self.time = time

        self.channel = channel
        self.promoted = promoted
        self.changes = [Change(**change) for change in changes]
        self.downloads = {"application": Download(**downloads["application"]),
                          "mojang-mappings": Download(**downloads["mojang-mappings"])}


class Project:
    def __init__(self, project_id, project_name, version, builds):
        self.project_id = project_id
        self.project_name = project_name
        self.version = version
        self.builds = [Build(**build) for build in builds]


def load_config() -> Config:
    try:
        with open("config.json", "r") as f:
            json_data = json.load(f)
            f.close()

        return Config(minecraft_version=json_data["minecraftVersion"])
    except FileNotFoundError:
        with open("config.json", "w") as f:
            json.dump({"minecraftVersion": "1.20.1"}, f)
            f.close()
        return Config(minecraft_version="1.20.1")


def main():

    config = load_config()

    # Fetch JSON data from the API
    url = f"https://api.papermc.io/v2/projects/paper/versions/{config.minecraft_version}/builds"
    response = requests.get(url)
    json_data = response.json()

    # Create project object
    project = Project(**json_data)

    # Get the last build
    last_build = project.builds[-1]

    current_build = None


    try:
        # Get the current build from build.txt and if it's the same as the last build, exit
        with open("build.txt", "r") as f:
            current_build = f.read()
            if current_build == str(last_build.build):
                return
            else:
                current_build = int(current_build)
                f.close()
    except FileNotFoundError:
        pass

    # Delete the old jar
    try:
        os.remove("paper.jar")
        print("Deleted old jar")
    except FileNotFoundError:
        pass


    # Download the latest build
    print("Downloading latest build...")
    url = (f"https://api.papermc.io/v2/projects/paper/versions/{config.minecraft_version}/builds/{last_build.build}/downloads/"
           f"paper-1.20.1-{last_build.build}.jar")
    response = requests.get(url)
    with open("paper.jar", "wb") as f:
        f.write(response.content)
        f.close()

    print("Downloaded latest build")

    # Update build.txt
    with open("build.txt", "w") as f:
        f.write(str(last_build.build))
        f.close()

    print("Updated build.txt")




if __name__ == "__main__":
    main()
