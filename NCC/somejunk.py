import requests

# Set your OAuth token or personal access token
token = "YOUR_TOKEN"

# Set the repository owner and name
owner = "OWNER"
repo = "REPO"

# Set the PR number
pull_number = 123

# Make the request
response = requests.patch(
    f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}",
    headers={"Authorization": f"token {token}"},
    json={"state": "closed"},
)

# Check the response status code
if response.status_code == 200:
    print("The PR status has been changed to closed.")
else:
    print("An error occurred while changing the PR status.")
