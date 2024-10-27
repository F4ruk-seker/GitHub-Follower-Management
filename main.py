from reporter import write_html_report
from models import GitHubUser
import requests
import config


def fetch_github_users(url):
    headers = {
        "Authorization": f"token {config.access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [GitHubUser(**user_data) for user_data in response.json()]
    else:
        raise f"Error fetching data from {url}: {response.status_code}"


def compare_followers_and_following(username):
    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"

    followers = fetch_github_users(followers_url)
    following = fetch_github_users(following_url)

    follower_logins = [follower.login for follower in followers]
    following_logins = [followed.login for followed in following]

    # Users you follow but are not following you
    print("\nTakip Ettiklerim (beni takip etmeyenler):")
    for followed_user in following:
        if followed_user.login not in follower_logins:
            print(f'{followed_user.login} : {followed_user.html_url}')

    # Users who follow you but you don't follow
    print("\nBeni Takip Edenler (benim takip etmediklerim):")
    for follower_user in followers:
        if follower_user.login not in following_logins:
            print(f'{follower_user.login} : {follower_user.html_url}')


if __name__ == '__main__':
    compare_followers_and_following(config.username)
