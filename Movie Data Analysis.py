#MOVIE DATA ANALYSIS


#Importing the modules to be used 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#Part One: Loading and Inspecting Data
#1. Loading and reading the 'imdb.xlsx' file
xl = pd.ExcelFile('imdb.xlsx')
#Loading each sheet onto a separate dataframe 
df = xl.parse('imdb')
df_countries = xl.parse('countries')
df_directors = xl.parse('directors')


#2. General Inspections of the File 
#2.1 Inspecting the shape (rows x coloumns) of first sheet
shape = df.shape
print('Number of coloumns:', shape[1])
print('Number of rows:', shape[0])
print('')

#2.2 Inspecting the coloumn headers of the first sheet
print('Coloumn headers in the sheet \'imdb\':')
for column in list(df.columns):
    print(column)
print('')

#2.3 Display the first 10 rows of data in the sheet 'imdb'
print('The first 10 enteries off the \'imdb\' sheet:')
print(df.head(10))
print('')



#Part Two: Data Merging, Updating, & Querying
#1. Joining the three Dataframes: df, df_countries, and df_directors (with an 'inner' join)
#Merging dataframe df with df_directors
df = pd.merge(left=df,
              right=df_directors,
              how='inner',
              left_on='director_id',
              right_on='id')

#Merging dataframe df with df_countries
df = pd.merge(left=df,
              right=df_countries,
              how='inner',
              left_on='country_id',
              right_on='id')

#removing unnecessary columns
del df['id_x']
del df['id_y']

#removing duplicate items (in case merging resulted in duplication)
df = df.drop_duplicates().reset_index(drop=True)

#Rearranging the coloumns order
rearranged_coloumns = ['movie_title', 'title_year', 'imdb_score', 'duration', 'gross', 'content_rating',
                       'director_name', 'director_id', 'country', 'country_id']
                       
df = df.reindex(columns=rearranged_coloumns)

#printing the first 5 enteries to see data after merging and updating
print('Dataframe after merging/updating:', df.head())
print('')


#2. Display the  first ten rows in the coloumn 'movie title'
#storing the first 10 enteries off 'movie_title' into a dataframe
first10_titles = df['movie_title'].head(10)
print('first 10 movies on the list:\n', first10_titles)
print('')


#2.2. Remove the extra character at the end of each movie title & report the first ten movie titles
df['movie_title'] = df['movie_title'].str.replace('Ê', '')

#Displaying the first 10 movie titles
print('First 10 movies titles after fixing:')
print(df['movie_title'].head(10))
print('')


#3. Who is the director with the most movies?
#reporting the frequency of directors listed 
director_freq = df['director_name'].value_counts()      
print('The director most featured and the frequency:\n', director_freq.head(1))
print('')


#4. Report all of this director's movies and their movie rating scores
most_featured = director_freq.head(1)      #get first entry
most_featured = most_featured.index[0]     #get the director name

#filtering dataframe by the director name
director_filter = df['director_name'] == most_featured
all_movies_ratings = df[director_filter][['movie_title', 'imdb_score']]   
all_movies_ratings.reset_index(inplace=True)    

#reporting the most featured director's movies
print('{}\'s movies and their imdb ratings are:'.format(most_featured))
print(all_movies_ratings)
print('')


#5. Recommend a random movie that has a rating of 8.5 or above. 
# Report the title and imdb score of your recommendation.

#filtering dataframe by rating score
RatingFilter = df['imdb_score'] >= 8.5     
df_TopMovies = df[RatingFilter]

#Reporting a random movie (via a randomly generated index)
import random
random_index = random.randint(0, len(df_TopMovies) - 1)         #get a random index
random_movie = df_TopMovies[random_index: random_index+1]         #select movie by random index
random_movie = random_movie[['movie_title', 'imdb_score']]        #get the movie title and rating score only 
print('Here is your recommendation of a highly rated movie:\n', random_movie)
print('')



#Part Three: Grouping and Summarizing Data (statistical analysis)
#1. Get the summary statistics (mean, std, percentile, etc.) for movies rating scores and gross amount
pd.options.display.float_format = '{:.2f}'.format          #to display numeric values in full without converting them to float
score_gross_description = df[['imdb_score', 'gross']].describe()
print('This table provides summary statistics for movies rating scores and gross amounts:\n', score_gross_description)
print('')


#2. What is the average score rating of the director Christopher Nolan's movies?
#filtering by director name, 'Christopher Nolan'
chris_nolan = df['director_name'] == 'Christopher Nolan'
nolan_mean = df[chris_nolan]['imdb_score'].mean()
print('The average rating score of a Christopher Nolan movie is:', nolan_mean)
print('')


#3. What is the average score rating for each director featured?
#Grouping directors by name and reporting the mean rating for each
directors = df.groupby('director_name').agg([np.mean])['imdb_score']
print('The following table lists each director featured and their average rating score:')
print(directors)
print('')

#Sorting 'directors' by mean rating score (from highest to lowest)
directors_sorted = directors.sort_values('mean', ascending=False)
print('Directors and their average rating score from the highest to lowest:')
print(directors_sorted)
print('')

#Report the director with the highest average rating score 
print('Director with the highest average rating score:', directors_sorted.index[0])
print('')


#4.Report the non-USA movies directed by Hayao Miyazaki and released after 1960
#filtering data by country (id), release year, and director name
foreign_movies = df['country_id'] != 1
year_filter = df['title_year'] > 1960
director_filter = df['director_name'] == 'Hayao Miyazaki'

#Reporting non-USA movies made after 1960 by Hayao Miyazaki
miyazaki = df[foreign_movies & year_filter & director_filter]
print('Movies directed by Hayao Miyazaki after 1960:')
print(miyazaki)
print('')


#5. What is the total runtime of the movie Gladiator?
#filtering data for only the movie 'Gladiator'
gladiator_filter = df['movie_title'] == 'Gladiator'
gladiator_duration = df[gladiator_filter]['duration']
print('Gladiator\'s runtime is:', gladiator_duration.values[0], 'minutes.')
print('')


#6. Create a Pivot Table that shows the median rating for each director,
#grouped by their respective countries.

#Creating the pivot table
pivot_tab = pd.pivot_table(df,
                           index=['country', 'director_name'],          #grouping data by country followed by director
                           values=['imdb_score'],                      #specifying the coloumn to statistically analyze ('imdb_score')
                           aggfunc=np.median)                         #specifying the type of analysis (median)

#Displaying the pivot table
print('Median rating for each director by their respective countries:')
print(pivot_tab)
print('')



#Part Four: Data Visualization
#1. Is how much a movie makes an indication of how good it is?
#Compare movies gross values to their rating scores using
#a scatterplot to determine the relationship between them. 

#Comparing gross to rating scores directly
ratings = df['imdb_score']
gross_amount = df['gross']
#dividing gross amount by 1,000,000
gross_amount = gross_amount.apply(lambda val: val/1000000)      

#setting the figure size
plt.figure(figsize=(10, 7))    # figsize=(width,height) in inches

#Creating a scatterplot to compare gross amount to rating scores
plt.scatter(gross_amount, ratings,
            s=30,                   #specifying the size of the marker
            marker='o',             #specifying the shape of the marker 
            c='#425ec2',            #specifying the color of the marker
            alpha=0.70)             #specifying the degree of transparency 

#Adding title and axis labels
plt.title('The relationship between movies gross amounts and rating scores')
plt.xlabel('Gross Amount (divided by 1,000,000)')
plt.ylabel('Rating Score')

#adjusting the tick marks for the x-axis 
plt.xticks(range(0, 651, 50))

#Displaying the scatter plot
plt.show()


#1.2. Did this relationship change over time? Compare pre-2000 movies vs. post-2000 movies.

#Filtering data by year of release 
before2000_filter = df['title_year'] < 2000
after2000_filter = df['title_year'] >= 2000
df_pre2000 = df[before2000_filter]
df_post2000 = df[after2000_filter]

#setting the figure size
plt.figure(figsize=(9, 6))

#Creating a scatterplot for pre-2000 movies
plt.scatter(df_pre2000['gross'].apply(lambda val: val/1000000),
            df_pre2000['imdb_score'],
            label='Pre-2000 movies',
            s=30,
            marker='o',
            c='b',
            alpha=0.8)

#Creating a scatterplot for post-2000 movies
plt.scatter(df_post2000['gross'].apply(lambda val: val/1000000),
            df_post2000['imdb_score'],
            label='Post-2000 movies',
            s=35,
            marker='D',
            c='g',
            alpha=0.85)

#adjusting the tick marks for the x-axis 
plt.xticks(range(0, 651, 50))

#Adding title and axis labels
plt.title('The relationship between movies gross amounts and rating scores')
plt.xlabel('Movie Gross Amount (divided by 1,000,000)')
plt.ylabel('Movie Rating Score')
#Adding a legend
plt.legend(title='Year of release:', loc='best')
#Displaying the scatter plot
plt.show()


#2. Create a histogram that shows the rating score distribution vs. frequency of rating scores 
# for R-Rated movies and PG-13 ones.

#Filtering the data by content rating 
r_rated_filter = df['content_rating'] == 'R'
pg13_rated_filter = df['content_rating'] == 'PG-13'
df_R = df[r_rated_filter]
df_PG13 = df[pg13_rated_filter]

#Setting the figure size
plt.figure(figsize=(10, 7))

#Creating a histogram to compare rating score distribution between R-rated and PG-13 rated movies
#Plotting R-rated movies 
plt.hist(df_R['imdb_score'],
         label='R-rated',
         color='#074eb0',
         alpha=0.75,
         linewidth=1, edgecolor='k',
         bins='auto')

#plotting PG-13 rated movies
plt.hist(df_PG13['imdb_score'],
         label='PG-13 rated',
         color='#faa938',
         alpha=0.9,
         linewidth=1, edgecolor='k',
         bins='auto')

#Adding titles and labels
plt.title('Rating score distribution for R-rated vs. PG13-rated movies')
plt.xlabel('Rating Score')
plt.ylabel('Frequency of Rating Score')
#Adding a legend
plt.legend(loc='best', title='Content Rating:')

#Displaying the histogram
plt.show()
