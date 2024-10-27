from reporter import write_html_report
from models import GitHubUser
from webbrowser import open_new_tab
from requests import api
import config


def fetch_github_users(url: str) -> list[GitHubUser] | None:
    headers = {
        "Authorization": f"token {config.access_token}"
    }
    response = api.get(url, headers=headers)
    if response.status_code == 200:
        return [GitHubUser(**user_data) for user_data in response.json()]
    else:
        raise f"Error fetching data from {url}: {response.status_code}"


def compare_followers_and_following(username: str) -> dict[str, list]:
    followers_url: str = f"https://api.github.com/users/{username}/followers"
    following_url: str = f"https://api.github.com/users/{username}/following"

    followers: list[GitHubUser] | None = fetch_github_users(followers_url)
    following: list[GitHubUser] | None = fetch_github_users(following_url)

    follower_logins: set = {follower.login for follower in followers}
    following_logins: set = {followed.login for followed in following}

    return {
        'not_following_back': [user for user in following if user.login not in follower_logins],
        'not_followed_back': [user for user in followers if user.login not in following_logins]
    }


def main():
    report: dict = compare_followers_and_following(config.username)
    report_output_dir: str = write_html_report(report)

    open_new_tab(report_output_dir)  # -> None


if __name__ == '__main__':
    main()
