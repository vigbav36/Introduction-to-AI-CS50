import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import random

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open("shopping.csv") as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []
        months = ["Jan","Feb","Mar","Apr","May","June","Jul","Aug","Sep","Oct","Nov","Dec"]

        for row in reader:
            for i in range (len(row)-1):

                if row[i] == "TRUE" :
                     row[i] = 1
                if row[i] == "FALSE": 
                    row[i] = 0
                if row[i] in months: 
                    row[i] = months.index(row[i])
                if row[i] == "Returning_Visitor": 
                    row[i] = 1
                if row[i] == "New_Visitor" or row[i] == "Other": 
                    row[i] = 0

                if i==0 or i==2 or i==4 or i==10 or i==11 or i==12 or i==13 or i==14 or i==15 or i==16:
                    row[i] = int(row[i])
                else:
                     row[i] = float(row[i])

            evidence.append([cell for cell in row[:17]])
            labels.append(1 if row[17] == "TRUE" else 0)

        return(evidence,labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_positive = 0
    incorrect_positive = 0
    total_positive = 0
    correct_negative = 0
    incorrect_negative = 0
    total_negative = 0
    sensitivity = 1.0
    specificity = 1.0

    for i in range (len(labels)):
        if labels[i] == 1 :
            total_positive+=1
            if labels[i] == predictions[i]:
                correct_positive+=1
            else:
                incorrect_positive+=1
        else:
            total_negative+=1
            if labels[i] == predictions[i]:
                correct_negative+=1
            else:
                incorrect_negative+=1
    
    sensitivity = float(correct_positive)/float(total_positive)
    
    specificity = float(correct_negative)/float(total_negative)

    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
