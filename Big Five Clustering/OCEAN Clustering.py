import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar
from sklearn.pipeline import Pipeline
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

# Reading in csv containing all test results from big 5 quiz
# Loaded in using pandas
data_raw = pd.read_csv('/Users/jaysamra/Downloads/IPIP-FFM-data-8Nov2018/data-final.csv', sep='\t')
data = data_raw.copy()
pd.options.display.max_columns = 150

data.drop(data.columns[50:107], axis=1, inplace=True)
data.drop(data.columns[51:], axis=1, inplace=True)

# Displaying total participants before pre-processing
print('Number of participants: ', len(data))
# Pandas to return first n rows to check data is correct
data.head()

# Cleaning data and removing null values to increase accuracy and optimise processing
print('DATA PRE-PROCESSING BEGINNING...')

# Boolean feedback to inform if there are null values present or not
print('ARE THERE MISSING VALUES? ', data.isnull().values.any())

#Displaying the number of missing values
print('HOW MANY MISSING VALUES? ', data.isnull().values.sum())

# Using pandas to remove all null values for 'data'
data.dropna(inplace=True)
print('DATA PRE-PROCESSING COMPLETED...')

#Displaying total participants after pre-processing is completed
print('PARTICIPANTS AFTER DATA CLEANING: ', len(data))

# OCEAN questions and results
# Displayed in graphs with questions in compilation

openQuestions = {'OPN1' : 'I have a rich vocabulary',
                 'OPN2' : 'I have difficulty understanding abstract ideas',
                 'OPN3' : 'I have a vivid imagination',
                 'OPN4' : 'I am not interested in abstract ideas',
                 'OPN5' : 'I have excellent ideas',
                 'OPN6' : 'I do not have a good imagination',
                 'OPN7' : 'I am quick to understand things',
                 'OPN8' : 'I use difficult words',
                 'OPN9' : 'I spend time reflecting on things',
                 'OPN10': 'I am full of ideas'}

conscientiousnessQuestions = {'CSN1' : 'I am always prepared',
                 'CSN2' : 'I leave my belongings around',
                 'CSN3' : 'I pay attention to details',
                 'CSN4' : 'I make a mess of things',
                 'CSN5' : 'I get chores done right away',
                 'CSN6' : 'I often forget to put things back in their proper place',
                 'CSN7' : 'I like order',
                 'CSN8' : 'I shirk my duties',
                 'CSN9' : 'I follow a schedule',
                 'CSN10' : 'I am exacting in my work'}


extroversionQuestions = {'EXT1' : 'I am the life of the party',
                 'EXT2' : 'I dont talk a lot',
                 'EXT3' : 'I feel comfortable around people',
                 'EXT4' : 'I keep in the background',
                 'EXT5' : 'I start conversations',
                 'EXT6' : 'I have little to say',
                 'EXT7' : 'I talk to a lot of different people at parties',
                 'EXT8' : 'I dont like to draw attention to myself',
                 'EXT9' : 'I dont mind being the center of attention',
                 'EXT10': 'I am quiet around strangers'}

agreeableQuestions = {'AGR1' : 'I feel little concern for others',
                 'AGR2' : 'I am interested in people',
                 'AGR3' : 'I insult people',
                 'AGR4' : 'I sympathize with others feelings',
                 'AGR5' : 'I am not interested in other peoples problems',
                 'AGR6' : 'I have a soft heart',
                 'AGR7' : 'I am not really interested in others',
                 'AGR8' : 'I take time out for others',
                 'AGR9' : 'I feel others emotions',
                 'AGR10': 'I make people feel at ease'}

neuroticismQuestions = {'EST1' : 'I get stressed out easily',
                 'EST2' : 'I am relaxed most of the time',
                 'EST3' : 'I worry about things',
                 'EST4' : 'I seldom feel blue',
                 'EST5' : 'I am easily disturbed',
                 'EST6' : 'I get upset easily',
                 'EST7' : 'I change my mood a lot',
                 'EST8' : 'I have frequent mood swings',
                 'EST9' : 'I get irritated easily',
                 'EST10': 'I often feel blue'}

# OCEAN group names and columns for graph display
EXT = [column for column in data if column.startswith('EXT')]
EST = [column for column in data if column.startswith('EST')]
AGR = [column for column in data if column.startswith('AGR')]
CSN = [column for column in data if column.startswith('CSN')]
OPN = [column for column in data if column.startswith('OPN')]

# Defining a function to visualize the questions and answers distribution
def graphQuest(groupname, questions, color):
    # Defining fixed size for each graph
    plt.figure(figsize=(40,60))
    for i in range(1, 11):
        plt.subplot(10,5,i)
        # Plotting histogram with relevant attributes
        plt.hist(data[groupname[i-1]], bins=14, color= color, alpha=.5)
        # Displaying questions for each graph as title
        plt.title(questions[groupname[i-1]], fontsize=18)

# Printing open Q&A graph
graphQuest(OPN, openQuestions, 'green')
# Printing conscientiousness Q&A graph
graphQuest(CSN, conscientiousnessQuestions, 'red')
# Printing extroversion Q&A graph
graphQuest(EXT, extroversionQuestions, 'blue')
# Printing agreeableness Q&A graph
graphQuest(AGR, agreeableQuestions, 'brown')
# Printing neuroticism Q&A graph
graphQuest(EST, neuroticismQuestions, 'purple')

# Generating elbow curve for k-means
# Elbow curve defines the number of clusters to use
df = data.drop('country', axis=1)
columns = list(df.columns)
# Scaled to a given range
scaler = MinMaxScaler(feature_range=(0,1))
df = scaler.fit_transform(df)
df = pd.DataFrame(df, columns=columns)
# Sample of data set 5000
df_sample = df[:5000]

# Creating and printing the elbow curve
kmeans = KMeans()
visualizer = KElbowVisualizer(kmeans, k=(2,15))
visualizer.fit(df_sample)
visualizer.poof()

df_model = data.drop('country', axis=1)

# Defining 5 clusters
# Based on OCEAN and elbow results
kmeans = KMeans(n_clusters=5)
k_fit = kmeans.fit(df_model)

# Predicting the Clusters
pd.options.display.max_columns = 10
predictions = k_fit.labels_
df_model['Clusters'] = predictions
df_model.head()

# count of people in each group
print('Number of people in clusters: ', df_model.Clusters.value_counts())

# PCA and scatter plot generation
pca = PCA(n_components=2)
pca_fit = pca.fit_transform(df_model)
# Labelling axis for PCA
df_pca = pd.DataFrame(data=pca_fit, columns=['PCA1', 'PCA2'])
df_pca['Clusters'] = predictions
df_pca.head()
# defining size for PCA generation
plt.figure(figsize=(10,10))
# Setting graph visuals
sns.scatterplot(data=df_pca, x='PCA1', y='PCA2', hue='Clusters', palette='Set2', alpha=0.8)
# Title for graph
plt.title('PCA CLUSTERS');


def graphQuest(data, questions, color):
    x = list(range(1, len(questions) + 1))
    y = [data[key] for key in questions.keys()]
    
    x = list(range(1, len(questions) + 1))
    y = [data[key] for key in questions.keys()]

    plt.scatter(x, y, c=color)
    plt.xlabel('Question Number')
    plt.ylabel('Score')
    plt.xticks(x)
    plt.ylim(1, 5)  # Assuming scores range from 1 to 5
    plt.grid()


class PersonalityQuiz:
    def __init__(self, master):
        self.master = master
        self.master.title("Personality Prediction")

        self.questions = {
            'OPN': openQuestions,
            'CSN': conscientiousnessQuestions,
            'EXT': extroversionQuestions,
            'AGR': agreeableQuestions,
            'EST': neuroticismQuestions
        }

        self.answers = {}
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_bar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        question_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=question_frame, anchor=tk.NW)
        
        # Add the answer key to the top right corner
        answer_key_text = ("Answer Key:\n"
                     "1: Strongly Disagree\n"
                     "2: Disagree\n"
                     "3: Neutral\n"
                     "4: Agree\n"
                     "5: Strongly Agree")
        answer_key_label = ttk.Label(question_frame, text=answer_key_text, background='wheat', relief="groove", padding=(10, 5))
        answer_key_label.grid(row=0, column=2, sticky=tk.NE, padx=10, pady=10)
        

        for i, domain in enumerate(self.questions.keys()):
            domain_label = ttk.Label(question_frame, text=f"{domain} Questions:", font=('Arial', 12, 'bold'))
            domain_label.grid(row=i * 11, column=0, sticky=tk.W, pady=10)

            for j, (question_id, question_text) in enumerate(self.questions[domain].items()):
                question_label = ttk.Label(question_frame, text=f"{question_id}. {question_text}", wraplength=600, anchor=tk.W, justify=tk.LEFT)
                question_label.grid(row=i * 11 + j + 1, column=0, sticky=tk.W)

                answer_var = tk.StringVar()
                entry = ttk.Entry(question_frame, textvariable=answer_var)
                entry.grid(row=i * 11 + j + 1, column=1, padx=10, pady=2)

                self.answers[question_id] = answer_var

        submit_button = ttk.Button(question_frame, text="Submit", command=self.submit)
        submit_button.grid(row=len(self.questions) * 11 + 1, column=0, pady=20)
        
        self.show_plots_button = tk.Button(question_frame, text="Show Plots", command=self.show_plots)
        self.show_plots_button.grid(row=56, column=1)  # Adjust the row and column values as needed

     
    def show_plots(self):
            # Create the Tkinter window
            window = tk.Toplevel(self.master)
            window.title("Personality Test Plots")

            # Calculate the personality scores
            personality_scores = self.predict_personality_scores()
            
            print("Openness questions data:", {key: personality_scores[i] for i, key in enumerate(openQuestions)})
            print("Conscientiousness questions data:", {key: personality_scores[i] for i, key in enumerate(conscientiousnessQuestions)})
            print("Extroversion questions data:", {key: personality_scores[i] for i, key in enumerate(extroversionQuestions)})
            print("Agreeableness questions data:", {key: personality_scores[i] for i, key in enumerate(agreeableQuestions)})
            print("Neuroticism questions data:", {key: personality_scores[i] for i, key in enumerate(neuroticismQuestions)})
            all_questions = list(itertools.chain(openQuestions, conscientiousnessQuestions, extroversionQuestions, agreeableQuestions, neuroticismQuestions))

            # Create the FigureCanvasTkAgg objects for each plot
            fig1 = plt.figure()
            graphQuest({key: personality_scores[i] for i, key in enumerate(openQuestions)}, openQuestions, 'green')
            canvas1 = FigureCanvasTkAgg(fig1, master=window)
            canvas1.draw()
            plt.close(fig1)
            canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            fig2 = plt.figure()
            graphQuest({key: personality_scores[len(openQuestions) + i] for i, key in enumerate(conscientiousnessQuestions)}, conscientiousnessQuestions, 'red')
            canvas2 = FigureCanvasTkAgg(fig2, master=window)
            canvas2.draw()
            plt.close(fig2)
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            fig3 = plt.figure()
            graphQuest({key: personality_scores[len(openQuestions) + len(conscientiousnessQuestions) + i] for i, key in enumerate(extroversionQuestions)}, extroversionQuestions, 'blue')
            canvas3 = FigureCanvasTkAgg(fig3, master=window)
            canvas3.draw()
            plt.close(fig3)
            canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            fig4 = plt.figure()
            graphQuest({key: personality_scores[len(openQuestions) + len(conscientiousnessQuestions) + len(extroversionQuestions) + i] for i, key in enumerate(agreeableQuestions)}, agreeableQuestions, 'orange')
            canvas4 = FigureCanvasTkAgg(fig4, master=window)
            canvas4.draw()
            plt.close(fig4)
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            fig5 = plt.figure()
            graphQuest({key: personality_scores[len(all_questions) - len(neuroticismQuestions) + i] for i, key in enumerate(neuroticismQuestions)}, neuroticismQuestions, 'purple')
            canvas5 = FigureCanvasTkAgg(fig5, master=window)
            canvas5.draw()
            plt.close(fig5)
            canvas5.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Start the Tkinter main loop
            window.mainloop()
        


    def submit(self):
        # Process and validate answers
        valid_answers = True
        for key, value in self.answers.items():
            try:
                int_val = int(value.get())
                if int_val < 1 or int_val > 5:
                    valid_answers = False
                    break
            except ValueError:
                valid_answers = False
                break

        if valid_answers:
            user_data = {key: [int(value.get())] for key, value in self.answers.items()}
            user_df = pd.DataFrame(user_data)
            # Process answers and predict personality scores
            personality_scores = self.predict_personality_scores()
            descriptions = self.describe_personality(personality_scores)
            result_text = "\n".join([f"{trait}: {score}\n{desc}" for trait, score, desc in zip(['Openness', 'Conscientiousness', 'Extroversion', 'Agreeableness', 'Neuroticism'], personality_scores, descriptions)])
            messagebox.showinfo("Results", f"Your predicted personality scores are:\n\n{result_text}")
            # Load your dataset with responses from other users
            other_users_df = pd.read_csv("user_answers.csv")

            # Show user cluster
            self.show_user_cluster(user_df, other_users_df)
            
            # Call the show_plots function after your data processing code
            self.show_plots()

            # Close the main window
            self.master.withdraw()

        else:
            messagebox.showerror("Invalid answers", "Please make sure all your answers are numbers between 1 and 5.")
            
            

    def predict_personality_scores(self):
        user_data = np.zeros((1, 50))
        for i, (key, value) in enumerate(self.answers.items()):
            user_data[0, i] = int(value.get())

        # Calculate the mean for each trait
        scores = np.mean(user_data.reshape(-1, 10, 5), axis=1)
        return scores.ravel()

    def describe_personality(self, scores):
        descriptions = [
            "Openness: You are creative, curious, and open to new experiences." if scores[0] > 3 else "Openness: You are consistent, cautious, and prefer familiarity.",
            "Conscientiousness: You are organized, responsible, and hardworking." if scores[1] > 3 else "Conscientiousness: You are spontaneous, flexible, and more easygoing.",
            "Extroversion: You are outgoing, energetic, and enjoy socializing." if scores[2] > 3 else "Extroversion: You are reserved, quiet, and prefer solitude.",
            "Agreeableness: You are friendly, empathetic, and cooperative." if scores[3] > 3 else "Agreeableness: You are more analytical, detached, and less concerned with others' feelings.",
            "Neuroticism: You are more emotionally unstable, anxious, and sensitive." if scores[4] > 3 else "Neuroticism: You are emotionally stable, calm, and less reactive to stress."
        ]
        return descriptions
    
    def show_user_cluster(self, user_df, other_users_df):
    # Fit the PCA and KMeans models on your dataset
        pca = PCA(n_components=2)
        pca_fit = pca.fit_transform(other_users_df)

        kmeans = KMeans(n_clusters=5)
        predictions = kmeans.fit_predict(other_users_df)

        # Create a pipeline to scale and predict the user's cluster
        pipeline = Pipeline([
            ('scaler', MinMaxScaler(feature_range=(0, 1))),
            ('kmeans', kmeans)
            ])
        user_cluster = pipeline.predict(user_df)[0]

        # Create the figure and axis for the plot
        fig, ax = plt.subplots()

        # Plot the clusters
        ax.scatter(pca_fit[:, 0], pca_fit[:, 1], c=predictions, cmap='viridis', alpha=0.6)
        user_pca = pca.transform(user_df)
        ax.scatter(user_pca[:, 0], user_pca[:, 1], c='red', marker='x', s=100, label="Your Result")
        ax.set_xlabel("PCA 1")
        ax.set_ylabel("PCA 2")
        ax.legend()
        ax.set_title("Personality Clusters")
        plt.show()

        # Create a new Tkinter Toplevel window to display the plot
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Personality Clusters")

        # Create a FigureCanvasTkAgg object to display the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

       
if __name__ == "__main__":
    root = tk.Tk()
    PersonalityQuiz(root)
    root.mainloop()
