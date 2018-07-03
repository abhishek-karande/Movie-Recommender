import numpy as np
import pandas as pd

ratings=['userId','movieId','rating']
ratingsData=pd.read_csv('u.data',sep='\t',names=ratings,usecols=range(3))
movies=['movieId','title']
moviesData=pd.read_csv('u.item',sep='|',names=movies,encoding='latin-1',usecols=range(2))
ratingsData=pd.merge(moviesData,ratingsData)

movieRatings= ratingsData.pivot_table(index=["userId"],columns=['title'],values='rating')

searchTerm=movieRatings['Star Wars (1977)']

similarMovies=movieRatings.corrwith(searchTerm)
similarMovies=similarMovies.dropna()
df=pd.DataFrame()

movieStat=ratingsData.groupby('title').agg({'rating':[np.size, np.mean]})

popularMovies=movieStat['rating']['size']>=200
print(movieStat[popularMovies].sort([('rating','mean')],ascending=False))
df=movieStat[popularMovies].join(pd.DataFrame(similarMovies,columns=['similarity']))

print(df.sort_values(['similarity'],ascending=False).head())
