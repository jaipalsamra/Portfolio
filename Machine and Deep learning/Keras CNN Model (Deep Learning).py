import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, Dropout, BatchNormalization
from keras.optimizers import Adam
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the dataset and preprocess it
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
column_names = [
    'class', 'cap_shape', 'cap_surface', 'cap_color', 'bruises', 'odor',
    'gill_attachment', 'gill_spacing', 'gill_size', 'gill_color',
    'stalk_shape', 'stalk_root', 'stalk_surface_above_ring',
    'stalk_surface_below_ring', 'stalk_color_above_ring',
    'stalk_color_below_ring', 'veil_type', 'veil_color', 'ring_number',
    'ring_type', 'spore_print_color', 'population', 'habitat'
]

data = pd.read_csv(url, header=None, names=column_names)

# Map the target variable to 0 and 1
data.iloc[:, 0] = data.iloc[:, 0].map({'e': 0, 'p': 1})

# Perform one-hot encoding on the categorical features using pd.get_dummies()
data_encoded = pd.get_dummies(data, columns=data.columns[1:])

# Split the data into features (X) and target (y)
X = data_encoded.iloc[:, 1:]
y = data_encoded.iloc[:, 0]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

cnn_model = Sequential()
cnn_model.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
cnn_model.add(BatchNormalization())
cnn_model.add(Conv1D(64, kernel_size=3, activation='relu'))
cnn_model.add(BatchNormalization())
cnn_model.add(Flatten())
cnn_model.add(Dense(64, activation='relu'))
cnn_model.add(Dropout(0.5))
cnn_model.add(Dense(1, activation='sigmoid'))

cnn_model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Reshape data for CNN input
X_train_cnn = X_train.values.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test_cnn = X_test.values.reshape(X_test.shape[0], X_test.shape[1], 1)

cnn_model.fit(X_train_cnn, y_train, epochs=10, batch_size=32, validation_split=0.1)

y_pred_cnn = cnn_model.predict(X_test_cnn)
y_pred_cnn = (y_pred_cnn > 0.5).astype(int)

accuracy_cnn = accuracy_score(y_test, y_pred_cnn)
precision_cnn = precision_score(y_test, y_pred_cnn)
recall_cnn = recall_score(y_test, y_pred_cnn)
f1_cnn = f1_score(y_test, y_pred_cnn)

print("CNN Metrics:")
print("Accuracy:", accuracy_cnn)
print("Precision:", precision_cnn)
print("Recall:", recall_cnn)
print("F1 Score:", f1_cnn)

feature_descriptions = {
        'cap_shape': {'b': 'bell', 'c': 'conical', 'x': 'convex', 'f': 'flat', 'k': 'knobbed', 's': 'sunken'},
        'cap_surface': {'f': 'fibrous', 'g': 'grooves', 'y': 'scaly', 's': 'smooth'},
        'cap_color': {'n': 'brown', 'b': 'buff', 'c': 'cinnamon', 'g': 'gray', 'r': 'green', 'p': 'pink', 'u': 'purple', 'e': 'red', 'w': 'white', 'y': 'yellow'},
        'bruises': {'t': 'bruises', 'f': 'no'},
        'odor': {'a': 'almond', 'l': 'anise', 'c': 'creosote', 'y': 'fishy', 'f': 'foul', 'm': 'musty', 'n': 'none', 'p': 'pungent', 's': 'spicy'},
        'gill_attachment': {'a': 'attached', 'd': 'descending', 'f': 'free', 'n': 'notched'},
        'gill_spacing': {'c': 'close', 'w': 'crowded', 'd': 'distant'},
        'gill_size': {'b': 'broad', 'n': 'narrow'},
        'gill_color': {'k': 'black', 'n': 'brown', 'b': 'buff', 'h': 'chocolate', 'g': 'gray', 'r': 'green', 'o': 'orange', 'p': 'pink', 'u': 'purple', 'e': 'red', 'w': 'white', 'y': 'yellow'},
        'stalk_shape': {'e': 'enlarging', 't': 'tapering'},
        'stalk_root': {'b': 'bulbous', 'c': 'club', 'u': 'cup', 'e': 'equal', 'z': 'rhizomorphs', 'r': 'rooted', '?': 'missing'},
        'stalk_surface_above_ring': {'f': 'fibrous', 'y': 'scaly', 'k': 'silky', 's': 'smooth'},
        'stalk_surface_below_ring': {'f': 'fibrous', 'y': 'scaly', 'k': 'silky', 's': 'smooth'},
        'stalk_color_above_ring': {'n': 'brown', 'b': 'buff', 'c': 'cinnamon', 'g': 'gray', 'o': 'orange', 'p': 'pink', 'e': 'red', 'w': 'white', 'y': 'yellow'},
        'stalk_color_below_ring': {'n': 'brown', 'b': 'buff', 'c': 'cinnamon', 'g': 'gray', 'o': 'orange', 'p': 'pink', 'e': 'red', 'w': 'white', 'y': 'yellow'},
        'veil_type': {'p': 'partial', 'u': 'universal'},
        'veil_color': {'n': 'brown', 'o': 'orange', 'w': 'white', 'y': 'yellow'},
        'ring_number': {'n': 'none', 'o': 'one', 't': 'two'},
        'ring_type': {'c': 'cobwebby', 'e': 'evanescent', 'f': 'flaring', 'l': 'large', 'n': 'none', 'p': 'pendant', 's': 'sheathing', 'z': 'zone'},
        'spore_print_color': {'k': 'black', 'n': 'brown', 'b': 'buff', 'h': 'chocolate', 'r': 'green', 'o': 'orange', 'u': 'purple', 'w': 'white', 'y': 'yellow'},
        'population': {'a': 'abundant', 'c': 'clustered', 'n': 'numerous', 's': 'scattered', 'v': 'several', 'y': 'solitary'},
        'habitat': {'g': 'grasses', 'l': 'leaves', 'm': 'meadows', 'p': 'paths', 'u': 'urban', 'w': 'waste', 'd': 'woods'}
}

def map_code_to_description(value, feature):
    return feature_descriptions.get(feature, {}).get(value, value)

def predict_mushroom_edibility(cnn_model, data_encoded):
    user_input = []
    for feature in column_names[1:]:
        options = ', '.join([f"{map_code_to_description(code, feature)} ({code})" for code in feature_descriptions[feature]])
        while True:
            value = input(f"Please enter the {feature} ({options}): ")
            if value in feature_descriptions[feature]:
                user_input.append(value)
                break
            else:
                print("Invalid input. Please try again.")

    user_input_dict = {column_names[i+1]: [user_input[i]] for i in range(len(user_input))}
    user_input_df = pd.DataFrame(user_input_dict)

    user_input_dummies = pd.get_dummies(user_input_df)

    # Create a DataFrame with the missing columns
    missing_columns = {col: [0] for col in data_encoded.columns[1:] if col not in user_input_dummies.columns}
    missing_columns_df = pd.DataFrame(missing_columns)

    # Concatenate the original DataFrame with the missing columns DataFrame
    user_input_dummies = pd.concat([user_input_dummies, missing_columns_df], axis=1)
    user_input_dummies = user_input_dummies[data_encoded.columns[1:]]

    # Reshape the data for CNN input
    user_input_cnn = user_input_dummies.values.reshape(1, user_input_dummies.shape[1], 1)

    prediction_cnn = cnn_model.predict(user_input_cnn)
    prediction_cnn = (prediction_cnn > 0.5).astype(int)

    if prediction_cnn[0] == 0:
        print("The mushroom is predicted to be edible.")
    else:
        print("The mushroom is predicted to be poisonous.")


predict_mushroom_edibility(cnn_model, data_encoded)

