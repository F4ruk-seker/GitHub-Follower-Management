from models import GitHubUser
import requests
import config

# Headers
headers = {
    "Authorization": f"token {config.access_token}"
}

# Takipçi listesini almak
followers_url = f"https://api.github.com/users/{config.username}/followers"
followers_response = requests.get(followers_url, headers=headers)
followers = [GitHubUser(**githubuser) for githubuser in followers_response.json()]

# Takip edilen kullanıcı listesini almak
following_url = f"https://api.github.com/users/{config.username}/following"
following_response = requests.get(following_url, headers=headers)
following = [GitHubUser(**githubuser) for githubuser in following_response.json()]

print("\nTakip Ettiklerim:")
for followed_user in following:
    if followed_user.login not in [follow_user.login for follow_user in followers]:
        print(f'{followed_user.login} : {followed_user.html_url}')
