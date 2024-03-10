import os
import gistyc
import requests
from dataclasses import dataclass
import re

@dataclass
class GistInfo:
    gist_id: str
    filename: str
    url: str
    model_name: str
    model_id: str
    model: str
    agieval: float
    gpt4all: float
    truthfulqa: float
    bigbench: float
    average: float


def update_gist(content, gist_id, access_token):
    """
    Update the content of a GitHub Gist.
    
    Args:
    content (str): The new content of the gist.
    gist_id (str): The ID of the gist to update.
    access_token (str): GitHub personal access token with gist permissions.
    """
    api_url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "files": {
            "YALL - Yet Another LLM Leaderboard.md": {
                "content": content
            }
        }
    }

    response = requests.patch(api_url, json=data, headers=headers)

    if response.status_code == 200:
        print("Gist updated successfully.")
    else:
        print("Failed to update gist. Status code:", response.status_code)
        print("Response:", response.json())


def create_yall():
    # Get token
    GITHUB_API_TOKEN = os.environ.get("GITHUB_TOKEN")
    YALL_GIST_ID = os.environ.get("YALL_GIST_ID")
    
    # Retrieve all gists
    gist_api = gistyc.GISTyc(auth_token=GITHUB_API_TOKEN)
    data = gist_api.get_gists()
    
    # List to store the GistInfo objects
    gist_infos = []
    
    for data_dict in data:
        if 'files' in data_dict and data_dict['files']:
            file_info = next(iter(data_dict['files'].values()))
            filename = file_info['filename']
            if filename.endswith("-Nous.md"):
                raw_url = file_info['raw_url']
                response = requests.get(raw_url)
                if response.status_code == 200:
                    if "Error: File does not exist" not in response.text:
                        # Parse the markdown table
                        lines = response.text.split('\n')
                        if len(lines) >= 3:
                            values = lines[2].split('|')[1:-1]
    
                            # Extract model name and model id using regular expression
                            model_match = re.search(r'\[([^\]]+)\]\(https://huggingface.co/([^/]+)/([^)]+)\)', values[0].strip())
                            if model_match:
                                model_name = model_match.group(1)
                                model_id = f"{model_match.group(2)}/{model_match.group(3)}"
                                print(values[0].strip())
                                print(model_name)
                                print(model_id)
                                print("=============")
                            else:
                                model_name = model_id = 'Unknown'
    
    
                        # Parse the markdown table
                        lines = response.text.split('\n')
                        if len(lines) >= 3:
                            values = lines[2].split('|')[1:-1]
    
                            # Create a GistInfo object and add it to the list
                            gist_info = GistInfo(
                                gist_id=data_dict['id'],
                                filename=filename,
                                url=data_dict['html_url'],  # Assuming html_url is the URL of the gist
                                model_name=model_name,
                                model_id=model_id,
                                model=values[0].strip(),
                                agieval=float(values[1].strip()),
                                gpt4all=float(values[2].strip()),
                                truthfulqa=float(values[3].strip()),
                                bigbench=float(values[4].strip()),
                                average=float(values[5].strip()),
                            )
                            gist_infos.append(gist_info)
    
    # Sort the list by average
    gist_infos = sorted(gist_infos, key=lambda x: x.average, reverse=True)
    
    # Create markdown table
    markdown_table = "| Model | Average | AGIEval | GPT4All | TruthfulQA | Bigbench |\n"
    markdown_table += "|---|---:|---:|---:|---:|---:|\n"
    
    for gist in gist_infos:
        model_link = f"[{gist.model_id}](https://huggingface.co/{gist.model_id})"
        markdown_table += f"| {model_link} [📄]({gist.url}) | {gist.average} | {gist.agieval} | {gist.gpt4all} | {gist.truthfulqa} | {gist.bigbench} |\n"
    
    # Update YALL's gist
    update_gist(content=markdown_table, gist_id=YALL_GIST_ID, access_token=GITHUB_API_TOKEN)

    return markdown_table