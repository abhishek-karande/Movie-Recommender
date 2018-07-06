import numpy as np
import pandas as pd
#loading the Data
ratings=['userId','movieId','rating']
ratingsData=pd.read_csv('u.data',sep='\t',names=ratings,usecols=range(3))
movies=['movieId','title']
moviesData=pd.read_csv('u.item',sep='|',names=movies,encoding='latin-1',usecols=range(2))
ratingsData=pd.merge(moviesData,ratingsData)
#creating pivot table for movie ratings
movieRatings= ratingsData.pivot_table(index=["userId"],columns=['title'],values='rating')
#creating correalation matrix between each movie
corrmatrix=movieRatings.corr(method='pearson',min_periods=100)
#taking user id from end user ,we will recommend movies to this user id
uid=input("enter a user id between 1 and 943\n")
uid=int(uid)
#collecting movies and their ratings watched by user
userRating=movieRatings.loc[uid].dropna()
#printing movies and ratings watched by user
print("Some of the movies watched and rated by the given user are:",userRating.head())
simCandidates = pd.Series()
for i in range(0,len(userRating.index)):
    #print('adding similarities for ', userRating.index[i])
    #retrieving similar movies to current movie
    similarities=corrmatrix[userRating.index[i]].dropna()
    #scaling  w.r.t. user rated movie 
    similarities=similarities.map(lambda x: x* userRating[i])
    #add in list of similarities
    simCandidates=simCandidates.append(similarities)
#dropping the movies that are already watched by user
simCandidates=simCandidates.drop(userRating.index)
#groupping the results and summing the ratings to remove redundant recommendations
simCandidates=simCandidates.groupby(simCandidates.index).sum()
print('sorting...')
simCandidates.sort_values(inplace=True,ascending=False)

print("Recommendations for user with user id",uid,"are:")  
print(simCandidates.head())

