import json

import requests
import os

class Config:
    """
    Represents configuration settings for Minecraft.

    Attributes:
        minecraft_version (str): The version of Minecraft specified in the configuration.
    """

    def __init__(self, minecraft_version: str):
        """
        Initializes a Config object with the specified Minecraft version.

        Args:
            minecraft_version (str): The version of Minecraft to set in the configuration.
        """
        self.minecraft_version = minecraft_version


class Change:
    """
    Represents a change in a commit with its details.

    Attributes:
        commit (str): The commit identifier.
        summary (str): A summary or brief description of the commit.
        message (str): The full message associated with the commit.
    """

    def __init__(self, commit, summary, message):
        """
        Initializes a Change object with commit details.

        Args:
            commit (str): The commit identifier.
            summary (str): A summary or brief description of the commit.
            message (str): The full message associated with the commit.
        """
        self.commit = commit
        self.summary = summary
        self.message = message


class Download:
    """
    Represents downloadable content with its name and SHA-256 hash.

    Attributes:
        name (str): The name of the downloadable content.
        sha256 (str): The SHA-256 hash of the downloadable content.
    """

    def __init__(self, name, sha256):
        """
        Initializes a Download object with content details.

        Args:
            name (str): The name of the downloadable content.
            sha256 (str): The SHA-256 hash of the downloadable content.
        """
        self.name = name
        self.sha256 = sha256


class Build:
    """
    Represents a build with its details including changes and downloads.

    Attributes:
        build (str): The build identifier.
        time (str): Timestamp of the build creation.
        channel (str): The build's channel information.
        promoted (bool): Indicates whether the build is promoted.
        changes (list of Change): List of Change objects associated with the build.
        downloads (dict): Dictionary containing Download objects for different content types.
    """

    def __init__(self, build, time, channel, promoted, changes, downloads):
        """
        Initializes a Build object with build details.

        Args:
            build (str): The build identifier.
            time (str): Timestamp of the build creation.
            channel (str): The build's channel information.
            promoted (bool): Indicates whether the build is promoted.
            changes (list of dict): List of dictionaries containing Change details.
            downloads (dict): Dictionary containing downloadable content details.
        """
        self.build = build
        self.time = time
        self.channel = channel
        self.promoted = promoted
        self.changes = [Change(**change) for change in changes]
        self.downloads = {"application": Download(**downloads["application"]),
                          "mojang-mappings": Download(**downloads["mojang-mappings"])}


class Project:
    """
    Represents a project with its ID, name, version, and associated builds.

    Attributes:
        project_id (str): The unique identifier for the project.
        project_name (str): The name of the project.
        version (str): The version of the project.
        builds (list of Build): List of Build objects associated with the project.
    """

    def __init__(self, project_id, project_name, version, builds):
        """
        Initializes a Project object with project details.

        Args:
            project_id (str): The unique identifier for the project.
            project_name (str): The name of the project.
            version (str): The version of the project.
            builds (list of dict): List of dictionaries containing Build details.
        """
        self.project_id = project_id
        self.project_name = project_name
        self.version = version
        self.builds = [Build(**build) for build in builds]



def load_config() -> Config:
    """
    Loads the Minecraft version configuration from 'config.json' file.

    Attempts to read the Minecraft version from 'config.json' file. If the file exists,
    extracts the Minecraft version from the JSON data and returns a Config object with
    the Minecraft version populated. If the file does not exist, it creates a new
    'config.json' file with default data ('{"minecraftVersion": "1.20.1"}') and returns
    a Config object with the default Minecraft version.

    Returns:
        Config: A Config object containing the Minecraft version.
    """
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
