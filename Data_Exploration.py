
##############################################################################
# Import modules and libraries #

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
from sklearn import metrics
from sklearn import preprocessing
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

##############################################################################


##############################################################################
# Data Clean-up #

wine_red = pd.read_csv('winequality-red.csv',sep=';')
wine_white = pd.read_csv('winequality-white.csv',sep=';')

# RED WINE DATA

wine_red.drop_duplicates(inplace=True)
#wine_red.dropna(inplace=True)

#No NA's
wine_red.isna().any()

wine_red.insert(6,'bound sulfur dioxide', wine_red['total sulfur dioxide'] - wine_red['free sulfur dioxide'])


wine_red_qualgroup = wine_red.groupby('quality')

wine_red_descr = wine_red_qualgroup.agg(['mean']).round(2).T#, 'std','sem']).round(2).T

wine_red_sugar_alc = (
                      wine_red.loc[:,['residual sugar','alcohol','quality']]
                          .groupby('quality')
                          .agg([np.mean,np.min,np.max])
                          .round(2)
                          .T
                      )
#print(wine_red_descr)


# WHITE WINE DATA

wine_white.drop_duplicates(inplace=True)
#wine_white.dropna(inplace=True)

#No NA's
wine_white.isna().any()

wine_white.insert(6,'bound sulfur dioxide', wine_white['total sulfur dioxide'] - wine_white['free sulfur dioxide'])

wine_white_qualgroup = wine_white.groupby('quality')

wine_white_descr = wine_white_qualgroup.agg(['mean']).round(2).T#, 'std','sem']).round(2).T

wine_white_sugar_alc = (
                      wine_white.loc[:,['residual sugar','alcohol','quality']]
                          .groupby('quality')
                          .agg([np.mean,np.min,np.max])
                          .round(2)
                          .T
                      )

##############################################################################


##############################################################################
# Target and Features Arrays #

target_red = wine_red.quality.astype('category')
target_red.cat.set_categories([3,4,5,6,7,8],inplace=True,ordered=True)

features_red = wine_red.drop('quality',axis=1)

target_white = wine_white.quality
features_white = wine_white.drop('quality',axis=1)

##############################################################################
# Feature Selection # Uses Scipy Module #

corr_matrix = wine_red.round(2).corr()

features_selected = []
feature_names = [x for x in features_red.columns]
for name in feature_names:
    coef,p = kendalltau(features_red[f'{name}'], target_red)
    if p < .01:
        features_selected.append(name)
        print(f'NAME:{name}, COEF:{coef}, P-VAL: {p}','\n')

corr_matrix2 = features_red.round(2).corr()

selected_features_red = features_red[features_selected]

f, ax = plt.subplots(figsize = (10,10))
cm_plot = sns.heatmap(corr_matrix, annot=True, linewidths=.8,fmt='.2f',ax=ax)

#CorrMatrix w/o Quality #

f, ax = plt.subplots(figsize = (10,10))
cm_plot = sns.heatmap(corr_matrix2, annot=True, linewidths=.8,fmt='.2f',ax=ax)

# Quality Distribution #

sns.barplot(wine_red.quality.unique(),wine_red.quality.value_counts())
plt.xlabel("Quality")
plt.ylabel("Frequency")
plt.title("Quality Distribution - Red Wine")
plt.show()


###############################################################################
# Models #

# 1) Multiple Logistic Regression
# 2) Random Forrest
# 3) PCA
# 4) SVM - Gaussian Kernel

feature_train,feature_test,target_train,target_test = train_test_split(features_red,
                                                      target_red,
                                                      test_size=0.3,
                                                      random_state=100) 

# Logistic Regression #

# w/ Feature Selection

pipe = make_pipeline(StandardScaler(), LogisticRegression())
pipe.fit(feature_train, target_train)

logreg_score_red = pipe.score(feature_test,target_test)

# w/o Feature Selection

pipe.fit(feature_train, target_train)  

logreg_score_red = pipe.score(feature_test,target_test)


feature_train,feature_test,target_train,target_test = train_test_split(selected_features_red,
                                                      target_red,
                                                      test_size=0.3,
                                                      random_state=100) 

pipe.fit(feature_train, target_train)  

sel_logreg_score_red = pipe.score(feature_test,target_test)

