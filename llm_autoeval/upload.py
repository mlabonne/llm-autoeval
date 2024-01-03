import requests


def upload_to_github_gist(text, gist_name, gh_token):
    # Create the gist content
    gist_content = {
        "public": False,  # set to True if you want it to be a public gist
        "files": {
            f"{gist_name}": {  # Change the file extension to .txt for plain text
                "content": text
            }
        },
    }

    # Headers for the request
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Make the request
    response = requests.post(
        "https://api.github.com/gists", headers=headers, json=gist_content
    )

    if response.status_code == 201:
        print(f"Uploaded gist successfully! URL: {response.json()['html_url']}")
    else:
        print(
            f"Failed to upload gist. Status code: {response.status_code}. Response: {response.text}"
        )
