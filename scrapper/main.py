from dynamodb import Dynamodb
from scrapper import scrapper
from utils import get_conf

def main():
    db = Dynamodb(
        url=get_conf("dynamodb_host"),
        region=get_conf("dynamodb_region")
    )

    clubs = {}
    # Scrap data
    for competition in get_conf("competitions").keys():
        print("Scraping {}".format(competition))
        matches, clubs = scrapper(competition, clubs)

        # Insert data into DynamoDB
        print("{} matches to insert".format(len(matches)))
        db.batch_insert(matches, "matches")

    print("{} clubs to insert".format(len(clubs)))
    db.batch_insert(clubs.values(), "clubs")

if __name__ == "__main__":
    main()
