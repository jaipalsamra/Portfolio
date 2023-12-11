import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  f1_score, confusion_matrix, accuracy_score, precision_score, recall_score

# Load the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
mushroom_df = pd.read_csv(url, header=None)

# Preprocess the data
for column in mushroom_df.columns:
    mushroom_df[column] = pd.factorize(mushroom_df[column])[0]
    
X = mushroom_df.iloc[:, 1:]
y = mushroom_df.iloc[:, 0]

# Train the random forest model using cross-validation
randForest = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=5, random_state=42)
scores = cross_val_score(randForest, X, y, cv=5, scoring='accuracy')
randForest.fit(X, y)

# Print the cross-validation scores
print("Cross-validation scores:", scores)
print("Average accuracy:", scores.mean())

# Create the test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Evaluate the model on the test set
y_pred = randForest.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Compute the confusion matrix
ConMat = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(ConMat)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# Function to preprocess user input
def inputP(user_input):
    cleanInput = []
    for feature in user_input:
        cleanInput.append(pd.factorize(feature)[0][0])
    return cleanInput

# Function to predict if a mushroom is edible or not
def edibilityPrediction(user_input):
    cleanInput = inputP(user_input)
    prediction = randForest.predict([cleanInput])
    
    if prediction[0] == 0:
        return "Edible"
    else:
        return "Poisonous"

def get_user_input():
    questions = [
        {
            "question": "Cap shape (bell=b, conical=c, convex=x, flat=f, knobbed=k, sunken=s): ",
            "options": ['b', 'c', 'x', 'f', 'k', 's']
        },
        {
            "question": "Cap surface (fibrous=f, grooves=g, scaly=y, smooth=s): ",
            "options": ['f', 'g', 'y', 's']
        },
        {
            "question": "Cap color (brown=n, buff=b, cinnamon=c, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y): ",
            "options": ['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y']
        },
        {
            "question": "Bruises? (bruises=t, no=f): ",
            "options": ['t', 'f']
        },
        {
            "question": "Odor (almond=a, anise=l, creosote=c, fishy=y, foul=f, musty=m, none=n, pungent=p, spicy=s): ",
            "options": ['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's']
        },
        {
            "question": "Gill attachment (attached=a, descending=d, free=f, notched=n): ",
            "options": ['a', 'd', 'f', 'n']
        },
        {
            "question": "Gill spacing (close=c, crowded=w, distant=d): ",
            "options": ['c', 'w', 'd']
        },
        {
            "question": "Gill size (broad=b, narrow=n): ",
            "options": ['b', 'n']
        },
        {
            "question": "Gill color (black=k, brown=n, buff=b, chocolate=h, gray=g, green=r, orange=o, pink=p, purple=u, red=e, white=w, yellow=y): ",
            "options": ['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y']
        },
        {
            "question": "Stalk shape (enlarging=e, tapering=t): ",
            "options": ['e', 't']
        },
        {
            "question": "Stalk root (bulbous=b, club=c, cup=u, equal=e, rhizomorphs=z, rooted=r, missing=?): ",
            "options": ['b', 'c', 'u', 'e', 'z', 'r', '?']
        },
        {
            "question": "Stalk surface above ring (fibrous=f, scaly=y, silky=k, smooth=s): ",
            "options": ['f', 'y', 'k', 's']
        },
        {
            "question": "Stalk surface below ring (fibrous=f, scaly=y, silky=k, smooth=s): ",
            "options": ['f', 'y', 'k', 's']
        },
        
        {
            "question": "Stalk color above ring (brown=n, buff=b, cinnamon=c, gray=g, orange=o, pink=p, red=e, white=w, yellow=y): ",
            "options": ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y']
        },
        {
            "question": "Stalk color below ring (brown=n, buff=b, cinnamon=c, gray=g, orange=o, pink=p, red=e, white=w, yellow=y): ",
            "options": ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y']
        },
        {
            "question": "Veil type (partial=p, universal=u): ",
            "options": ['p', 'u']
        },
        {
            "question": "Veil color (brown=n, orange=o, white=w, yellow=y): ",
            "options": ['n', 'o', 'w', 'y']
        },
        {
            "question": "Ring number (none=n, one=o, two=t): ",
            "options": ['n', 'o', 't']
        },
        {
            "question": "Ring type (cobwebby=c, evanescent=e, flaring=f, large=l, none=n, pendant=p, sheathing=s, zone=z): ",
            "options": ['c', 'e', 'f', 'l', 'n', 'p', 's', 'z']
        },
        {
            "question": "Spore print color (black=k, brown=n, buff=b, chocolate=h, green=r, orange=o, purple=u, white=w, yellow=y): ",
            "options": ['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y']
        },
        {
            "question": "Population (abundant=a, clustered=c, numerous=n, scattered=s, several=v, solitary=y): ",
            "options": ['a', 'c', 'n', 's', 'v', 'y']
        },
        {
            "question": "Habitat (grasses=g, leaves=l, meadows=m, paths=p, urban=u, waste=w, woods=d): ",
            "options": ['g', 'l', 'm', 'p', 'u', 'w', 'd']
        }
    ]
    
    user_input = []
    for q in questions:
        while True:
            answer = input(q["question"])
            if answer in q["options"]:
                user_input.append(answer)
                break
            else:
                print("Invalid input. Please try again.")
    
    return user_input

# Get user input and predict edibility
user_input = get_user_input()
result = edibilityPrediction(user_input)
print("\nThis mushroom is:", result)




