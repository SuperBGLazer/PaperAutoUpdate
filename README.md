# PaperAutoUpdate

PaperAutoUpdate is a Python script designed to automate the process of updating a PaperMC server. It simplifies the task of keeping your Paper server software up-to-date by fetching the latest version and applying the necessary updates.
Usage

To get started, run the following command:

```bash
python update.py
```

This will initiate the update process, fetching the latest PaperMC version and applying the necessary updates to your server.

## Installation Steps (Ubuntu)

1. Clone the repository to your local machine:

```bash
git clone https://github.com/SuperBGLazer/PaperAutoUpdate.git
```

2. Navigate to the project directory:

```bash
cd PaperAutoUpdate
```

3. Ensure you have Python installed. If not, you can install it using:

```bash
sudo apt-get update
sudo apt-get install python3
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Create/edit the config.json file to match your server configuration:

```json
{
    "minecraftVersion": "1.20.1"
}
```

6. Run the update script:

```bash
python update.py
```

## Disclaimer

Please note that this script is designed to work specifically with PaperMC servers. Make sure to backup your server data before running the update to avoid any potential data loss.
Contribution

Feel free to contribute to this project by creating issues or submitting pull requests. Your feedback and contributions are highly appreciated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.