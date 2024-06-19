import argparse
from commands.manage_user import sync_user


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('subdomain')
    args = parser.parse_args()

    result = sync_user(args.username, args.subdomain)
    print(result)


if __name__ == "__main__":
    main()