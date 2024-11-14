import csv
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

# This class loads in data from different time periods and different regions
# and compares queries across two sets, returning either dice coefficients
# or cosine similarities.
# Authors: Abigail Pitcairn and Behrooz Mansouri
# Version: 11.14.2024

topics = ["ART", "BEAUTY", "BOOKS", "BUS", "COMP", "FOOD", "HEALTH", "HOBBIES", "JOBS",
          "NEWS", "ONLINE", "PEOPLE", "SHOP", "SPORT", "TRAVEL"]


def read_trend_file_to_set(csv_file_path):
    """
    This method takes in the file path to a trend file and return only the set of queries annotated as top
    @param csv_file_path: file path to trend file
    @return: set of queries in top
    """
    queries = []
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        csvFile = csv.reader(file)
        next(csvFile)
        next(csvFile)
        for line in csvFile:
            if len(line) < 2:
                break
            queries.append(line[0].lower())
    return list(set(queries))


def dice_coefficient(list1, list2):
    """
    This method takes in two set of queries and return their dice coefficient
    @param list1: query terms 1
    @param list2: query terms 2
    @return: dice coefficient
    """
    set1 = set(list1)
    set2 = set(list2)

    intersection = set1.intersection(set2)

    return 2 * len(intersection) / (len(set1) + len(set2))


def get_avg_max_cosine(list1, list2):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings1 = model.encode(list1, convert_to_tensor=True)
    embeddings2 = model.encode(list2, convert_to_tensor=True)
    similarities = util.semantic_search(embeddings1, embeddings2)
    sum = 0.0
    for item in similarities:
        max_score = item[0]['score']
        sum += max_score
    return sum / len(similarities)


def compare_dice_coefficients(time, region1, region2):
    for topic in topics:
        set1 = f"Data/{time}/{region1}/{region1}-{topic}.csv"
        queries1 = read_trend_file_to_set(set1)
        set2 = f"Data/{time}/{region2}/{region2}-{topic}.csv"
        queries2 = read_trend_file_to_set(set2)
        print(topic + f"\t\tDice: {dice_coefficient(queries1, queries2)}")

def compare_cosines(time, region1, region2):
    for topic in topics:
        set1 = f"Data/{time}/{region1}/{region1}-{topic}.csv"
        queries1 = read_trend_file_to_set(set1)
        set2 = f"Data/{time}/{region2}/{region2}-{topic}.csv"
        queries2 = read_trend_file_to_set(set2)
        print(topic + f"\t\tAvg. Cosine: {get_avg_max_cosine(queries1, queries2)}")
