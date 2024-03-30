'''
    Josue Antonio
    DS 2500
    HW 1
    5/15 - Summer 1 2023
    boardgames.py
'''

import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

GAMES = 'bgg.csv'
INFINITY = 1000000

def read_csv(filename):
    ''' Fn: read_csv
        Param: filename string
        Returns: nested dictionary 
        Does: reads every line of csv file storing them in nested dictionary
              while ignoring entries with 'minplayers' greater than 1
    '''
    data, header = {}, []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        header = next(reader)
        for row in reader:
            if int(row[1]) == 0 or int(row[1]) == 1:
                minplaytime = int(row[2])
                maxplaytime = int(row[3])
                minage = int(row[4])
                average = float(row[5])
                avgweight = float(row[6])
                data[row[0]] = {header[2]: minplaytime, header[3]: maxplaytime,
                                header[4]: minage, header[5]: average,
                                header[6]: avgweight}
    return data

def euclidean_dist(dic, game1, game2):
    '''
        Fn: euclidean_dist
        Param: dictionary, game1 string, game2 string
        Returns euclidean distance between both games
        Does: computes euclidean distance between given games based on
              their stored numeric attributes
    '''
    dist = 0
    for attribute in dic[game1]:
        dist += (dic[game2][attribute] - dic[game1][attribute]) ** 2
    return dist ** 0.5
    
def most_similar_game(dic, title):
    '''
        Fn: most_similar_game
        Param: dictionary, game title string
        Returns: game most similar to given title based on euclidean distance, 
                 and respective distance between given title and closest game
    '''
    similar_distance = INFINITY
    similar_game = ''
    for game in dic:
        if euclidean_dist(dic, title, game) < similar_distance and title != game:
            similar_distance = euclidean_dist(dic, title, game)
            similar_game = game
    return similar_game, similar_distance

def plot_bar(dic, attribute_key, attribute_name):
    '''
        Fn: plot_bar
        Param: dictionary, attribute key (string), attribute name (string)
        Returns: nothing
        Does: generates bar plot showing number of games for given attribute
    '''
    round_attributes = [round(dic[title][attribute_key]) for title in dic]
    attribute_counts = {x : round_attributes.count(x) for x in round_attributes}
    plt.figure(figsize=(10, 6), dpi=500)
    plt.bar(attribute_counts.keys(), attribute_counts.values(), color = 'navy')
    # without xticks there were some missing labels (2, 8, 9)
    plt.xticks([0, 2, 3, 4, 5, 6, 7, 8, 9], [0, 2, 3, 4, 5, 6, 7, 8, 9])
    plt.title("Number of Games per " + attribute_name)
    plt.xlabel(attribute_name)
    plt.ylabel("Number of Games")
    plt.show()
    
def plot_regression(dic, attribute1_key, attribute1_name, attribute2_key, attribute2_name):
    '''
        Fn: plot_regression
        Param: dictionary, dic keys for two attributes, name of two attributes
        Returns: nothing
        Does: generates scatter plot of attribute1 vs. attribute2 with a
              line of best fit, and display correlation coefficient between 
              attributes
    '''
    attributes1 = [dic[title][attribute1_key] for title in dic]
    attributes2 = [dic[title][attribute2_key] for title in dic]
    plt.figure(figsize=(8,4), dpi=500)
    sns.regplot(x = attributes1, y = attributes2, 
                scatter_kws={'s':9, "color":"navy"}, marker = ".",
                line_kws={"color": "black", "lw":2, "label":"line of best fit"})
    plt.title(attribute1_name + " vs. " + attribute2_name)
    plt.xlabel(attribute1_name)
    plt.ylabel(attribute2_name)
    plt.grid()
    plt.legend()
    plt.show()
    print("The correlation coefficient is:", 
          round(np.corrcoef(attributes1, attributes2)[0,1], 4)) 

def main():
    # Gather data - read data to store in dictionary
    data = read_csv(GAMES)
    
    # Make a recommendation  - given user input, recommend most similar game
    title = input("Enter your favorite title:\n")
    similar_game, similar_distance = most_similar_game(data, title)
    print("\nThe game most similar to", title, "is", similar_game,
          "with an euclidean distance of",
          round(similar_distance, 4), "\n")
    
    # Communication - bar plot of game count for all user ratings, 
    #                 regression plot of game weight vs. user rating
    plot_bar(data, "average", "User Rating")
    plot_regression(data, "avgweight", "Game Weight", "average", "User Rating")
    
    # Correlation coefficient: 0.52
    # it falls close to the positive end of spectrum (-1 to 1), indicating
    # a positive relationship between the game weight and average user rating
    
'''
    Part D)
    If I were the head of marketing for a boardgame company, I would recommend our company to 
    develop a moderate to heavy-weight game. My recommended target weight would be anywhere 
    from 3 to 3.5 for 3 reasons. The first one being that there is a positive correlation (of ~0.5) 
    between the user rating and game weight as seen in the regression plot, and the line of best fit.
    Thus, it would be a good bet to think that a game with a somewhat high weight would result in a 
    high rated game. Moreover, if you look at the regression plot closely you can see that there's a 
    significant number of points (more than in any other region) above the 8 rating mark, in the 3-3.5 
    game weight range. Lastly, I wouldn't pick a game with weight above 3.5 or 4 because it's likely
    that it would cost around $300 which would be very expensive for the company, especially since
    my company would still be attempting to break the world of solo board games.
       
'''
if __name__ == "__main__":
    main()