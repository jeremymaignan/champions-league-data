from dynamodb import DynamoDB
from scrapper import scrapper
import os
from dotenv import load_dotenv

competitions = {
    "Champions League": {
        "id": 1,
        "from": 1955,
        "name": "Champions League"
    },
    "Europa League": {
        "id": 14,
        "from": 1971,
        "name": "Europa League"
    },
    "Europa Conference League": {
        "id": 2019,
        "from": 2021,
        "name": "Europa Conference League"
    }
}

def main():
    load_dotenv()

    db = DynamoDB(
        url=os.getenv("DYNAMODB_HOST"),
        region=os.getenv("DYNAMODB_REGION")
    )

    clubs = {}
    # Scrap data
    for name, competition in competitions.items():
        print("Scraping {}".format(name))
        matches, clubs = scrapper(competition, clubs)

        # Insert data into DynamoDB
        print("{} matches to insert".format(len(matches)))
        db.batch_insert(matches, "matches")

    print("{} clubs to insert".format(len(clubs)))
    db.batch_insert(clubs.values(), "clubs")

if __name__ == "__main__":
    main()
