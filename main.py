from reporter import write_html_report
from models import GitHubUser
from webbrowser import open_new_tab
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

    follower_logins = {follower.login for follower in followers}
    following_logins = {followed.login for followed in following}

    class Report:
        not_following_back = [user for user in following if user.login not in follower_logins]
        not_followed_back = [user for user in followers if user.login not in following_logins]

    return Report


def main():
    report = compare_followers_and_following(config.username)
    report_output_dir = write_html_report(**report.__dict__)
    open_new_tab(report_output_dir)


if __name__ == '__main__':
    main()
