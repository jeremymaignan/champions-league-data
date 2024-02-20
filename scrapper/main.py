from dynamodb import Dynamodb
from scrapper import scrapper
from utils import get_conf

def main():
    db = Dynamodb(
        url=get_conf("dynamodb_host"),
        region=get_conf("dynamodb_region")
    )

    # Scrap data
    for competition in get_conf("competitions").keys():
        print("Scraping {}".format(competition))
        games, clubs = scrapper(competition)
        print("{} games to insert".format(len(games)))

        # Insert data into DynamoDB
        db.batch_insert(games, "games")
        db.batch_insert(clubs, "clubs")

if __name__ == "__main__":
    main()
