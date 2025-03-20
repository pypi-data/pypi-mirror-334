""" 
Methods availables:
    info_lib() -> Informations of importants libs to Data Analysis 
    concepts_analysis()  -> Function to check how type of Hypotesis test based on variables. 
"""

import pandas as pd
from IPython.display import display, Markdown


def info_lib():

    libraries_info = [
    ("import pandas as pd", "Used for data manipulation and analysis, providing data structures like DataFrames.", "df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})"),
    ("import numpy as np", "Supports large, multi-dimensional arrays and matrices, along with mathematical functions.", "arr = np.array([1, 2, 3, 4])"),
    ("import pylab as pl", "Combines features of numpy, scipy, and matplotlib for easy scientific computations.", "pl.plot([1, 2, 3], [4, 5, 6])"),
    
    # Plotting libraries
    ("import matplotlib.pyplot as plt", "A popular library for creating static, animated, and interactive visualizations.", "plt.plot([1, 2, 3], [4, 5, 6]); plt.show()"),
    ("import seaborn as sns", "Built on matplotlib, it provides a high-level interface for statistical graphics.", "sns.scatterplot(x=[1,2,3], y=[4,5,6])"),
    
    # Stats and machine learning libraries
    ("import statsmodels.api as sm", "Provides statistical models and tests for data analysis.", "model = sm.OLS(y, X).fit()"),
    ("import scipy.stats as stats", "Contains statistical functions for probability distributions and hypothesis testing.", "t_stat, p_val = stats.ttest_ind(data1, data2)"),
    ("from scipy import stats", "Provides access to statistical tests and probability functions.", "p_value = stats.ttest_rel(data1, data2)"),
    ("from scipy.stats import mannwhitneyu", "Performs the Mann-Whitney U test for independent samples.", "stat, p = mannwhitneyu(data1, data2)"),
    ("from scipy.stats import chi2_contingency", "Performs a Chi-square test for independence on a contingency table.", "chi2, p, dof, expected = chi2_contingency(table)"),
    
    ("from sklearn.model_selection import train_test_split", "Splits dataset into training and testing sets.", "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)"),
    ("from sklearn.model_selection import KFold", "Splits dataset into K consecutive folds for cross-validation.", "kf = KFold(n_splits=5, shuffle=True, random_state=42)"),
    ("from sklearn.model_selection import cross_val_score", "Performs cross-validation and returns model scores.", "scores = cross_val_score(model, X, y, cv=5)"),
    
    ("from sklearn.preprocessing import StandardScaler", "Standardizes features by removing mean and scaling to unit variance.", "scaler = StandardScaler().fit(X_train)"),
    ("from sklearn.preprocessing import LabelEncoder", "Encodes categorical labels as integers.", "le = LabelEncoder(); y_encoded = le.fit_transform(y)"),
    ("from sklearn.preprocessing import label_binarize", "Binarizes labels for multi-class classification.", "y_bin = label_binarize(y, classes=[0, 1, 2])"),
    
    ("from sklearn.linear_model import LinearRegression", "Performs linear regression modeling.", "model = LinearRegression().fit(X, y)"),
    ("from sklearn.linear_model import LogisticRegression", "Performs logistic regression for classification tasks.", "model = LogisticRegression().fit(X_train, y_train)"),
    
    ("from sklearn.tree import DecisionTreeClassifier", "Implements decision tree classification.", "clf = DecisionTreeClassifier().fit(X_train, y_train)"),
    ("from sklearn.tree import DecisionTreeRegressor", "Implements decision tree regression.", "reg = DecisionTreeRegressor().fit(X_train, y_train)"),

    # Metrics and statistical analysis
    ("from sklearn.metrics import confusion_matrix", "Computes the confusion matrix to evaluate classification performance.", "cm = confusion_matrix(y_true, y_pred)"),
    ("from sklearn.metrics import accuracy_score", "Calculates the accuracy of a classification model.", "accuracy = accuracy_score(y_true, y_pred)"),
    ("from sklearn.metrics import precision_score", "Calculates the precision (positive predictive value) of a model.", "precision = precision_score(y_true, y_pred)"),
    ("from sklearn.metrics import recall_score", "Calculates the recall (sensitivity) of a model.", "recall = recall_score(y_true, y_pred)"),
    ("from sklearn.metrics import roc_auc_score", "Computes the Area Under the Receiver Operating Characteristic Curve (ROC AUC).", "auc = roc_auc_score(y_true, y_prob)"),
    ("from sklearn.metrics import roc_curve", "Computes Receiver Operating Characteristic (ROC) curve points.", "fpr, tpr, thresholds = roc_curve(y_true, y_prob)"),
    ("from sklearn.metrics import classification_report", "Generates a summary report of precision, recall, and f1-score.", "report = classification_report(y_true, y_pred)"),
    ("from sklearn.metrics import f1_score", "Computes the harmonic mean of precision and recall.", "f1 = f1_score(y_true, y_pred)"),
    ("from sklearn.metrics import mean_absolute_error", "Computes the Mean Absolute Error (MAE) between actual and predicted values.", "mae = mean_absolute_error([3, -0.5, 2], [2.5, 0.0, 2])"),
    ("from sklearn.metrics import r2_score", "Computes the R-squared value, a measure of model performance.", "r2 = r2_score([3, -0.5, 2], [2.5, 0.0, 2])"),
    ("from sklearn.metrics import mean_squared_error", "Computes the Mean Squared Error (MSE) for regression models.", "mse = mean_squared_error([3, -0.5, 2], [2.5, 0.0, 2])"),
    ("from sklearn.feature_selection import RFE","Performs Recursive Feature Elimination (RFE) to select the most relevant features for a model.", "rfe = RFE(model, n_features_to_select=20) rfe.fit(X_train, y_train)  # Fit the RFE model col = X_train.columns[rfe.support_]  # Identify selected columns model.fit(X_train[col], y_train)  # Train a new model with selected features"),
    # Dimensionality Reduction
    ("from sklearn.decomposition import PCA", "Performs Principal Component Analysis (PCA) for dimensionality reduction.", "pca = PCA(n_components=2).fit_transform(X)"),
    
    # Preprocessing
    ("from sklearn.preprocessing import StandardScaler", "Standardizes features by removing the mean and scaling to unit variance.", "scaler = StandardScaler().fit(X_train); X_scaled = scaler.transform(X_train)"),
    
    # Time Management
    ("import time", "Provides functions for working with time, including measuring execution time.", "start_time = time.time(); elapsed_time = time.time() - start_time"),
    
    # Discriminant Analysis
    ("from sklearn.discriminant_analysis import LinearDiscriminantAnalysis", "Performs Linear Discriminant Analysis (LDA) for classification.", "lda = LinearDiscriminantAnalysis(n_components=2).fit(X_train, y_train)"),
    
    # Nearest Neighbors
    ("from sklearn.neighbors import KNeighborsClassifier", "Implements k-Nearest Neighbors (KNN) classification.", "knn = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)"),
    
    # Clustering
    ("from sklearn.cluster import KMeans", "Performs k-means clustering.", "kmeans = KMeans(n_clusters=3, random_state=42).fit(X)"),
    
    # Perceptron and SGD
    ("from sklearn.linear_model import Perceptron", "Implements the Perceptron algorithm for binary classification.", "perceptron = Perceptron().fit(X_train, y_train)"),
    ("from sklearn.linear_model import SGDClassifier", "Implements a linear classifier with Stochastic Gradient Descent (SGD).", "sgd = SGDClassifier().fit(X_train, y_train)"),
    
    # Outlier Detection
    ("from statsmodels.stats.outliers_influence import variance_inflation_factor", "Calculates the Variance Inflation Factor (VIF) to detect multicollinearity.", "vif = variance_inflation_factor(X.values, i)"),
    ("from sklearn.neighbors import LocalOutlierFactor", "Detects outliers using the Local Outlier Factor (LOF) method.", "lof = LocalOutlierFactor(n_neighbors=20).fit_predict(X)"),
    
    # Hyperparameter Tuning
    ("from sklearn.model_selection import GridSearchCV", "Performs exhaustive grid search to optimize hyperparameters.", "grid = GridSearchCV(model, param_grid, cv=5).fit(X_train, y_train)"),
    ("from sklearn.model_selection import RandomizedSearchCV", "Performs randomized search over hyperparameters for optimization.", "random_search = RandomizedSearchCV(model, param_distributions, n_iter=50).fit(X_train, y_train)"),
    
    # Ensemble Learning
    ("from sklearn.ensemble import RandomForestClassifier", "Implements a Random Forest classifier, an ensemble of decision trees.", "rf = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)"),
    
    # Text Processing
    ("from sklearn.metrics.pairwise import cosine_similarity", "Computes cosine similarity between vectors, often used in NLP.", "similarity = cosine_similarity(vector1, vector2)"),
    ("from sklearn.feature_extraction.text import TfidfVectorizer", "Converts text into a TF-IDF weighted vector representation.", "vectorizer = TfidfVectorizer().fit_transform(corpus)"),
    
    # Natural Language Processing (NLP)
    ("from nltk.stem import WordNetLemmatizer, PorterStemmer", "Performs word lemmatization and stemming for text preprocessing.", "lemmatizer = WordNetLemmatizer(); stemmer = PorterStemmer()"),
    ("from nltk.tokenize import word_tokenize", "Tokenizes text into individual words.", "tokens = word_tokenize(text)"),
    ("from nltk.corpus import stopwords", "Provides stopwords to filter out common words in text processing.", "stop_words = set(stopwords.words('english'))"),
    ("import re", "Provides regular expressions for pattern matching and text processing.", "clean_text = re.sub(r'[^a-zA-Z]', ' ', text)"),
    ("from nltk.tokenize import WhitespaceTokenizer, TreebankWordTokenizer", "Different tokenizers for splitting text into words.", "tokens = WhitespaceTokenizer().tokenize(text)"),
    
    # Feature Extraction
    ("from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer", "Converts text into numerical features using CountVectorizer and TfidfVectorizer.", "vectorizer = CountVectorizer().fit_transform(corpus)"),
    
    # Model Evaluation
    ("from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, classification_report, f1_score", "Computes various evaluation metrics for classification models.", "accuracy = accuracy_score(y_true, y_pred)"),
    ("from sklearn.metrics import roc_auc_score, ConfusionMatrixDisplay, RocCurveDisplay", "Computes ROC AUC score and displays confusion matrix and ROC curve.", "roc_auc = roc_auc_score(y_true, y_prob)"),
    
    # Data Splitting and Cross-Validation
    ("from sklearn.model_selection import train_test_split, cross_val_score", "Splits data into training and testing sets, performs cross-validation.", "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)"),
    
    # Visualization
    ("import matplotlib.pylab as plt", "Provides plotting functions for data visualization.", "plt.plot([1, 2, 3], [4, 5, 6]); plt.show()"),
    ("import seaborn as sns", "Offers high-level visualization tools built on matplotlib.", "sns.scatterplot(x=[1,2,3], y=[4,5,6])"),
    
    # Warnings Handling
    ("import warnings", "Suppresses warnings to keep output clean.", 'warnings.filterwarnings("ignore")')
    ]
    
    libraries_stats = pd.DataFrame(libraries_info, columns=['Library','Description','Code exemplo'])
    
    return display(Markdown(libraries_stats.to_markdown()))


def concepts_analysis():

    concept_list = [
        ('Univariate Analysis','Categorical','Frequency, Mode, Level','Bar Char or Pie Chart','N/A'),
        ('Univariate Analysis','Numerical','Central Tendency(mean,median,mode) and measure of position (min, Q1, median, Q3, max), measure of depression: std, var, skewness, cof','Histogram, density graph, Box, plot','N/A'),
        ('Bivariate Analysis','Continous Vs. Continous','N/A','Pearson correlation or Spearman and regression', 'Scatter plot, Line graph(time)'),
        ('Bivariate Analysis','Categorical Vs. Categorical','Contigency table (two-way)','Stacked bar chart, Grouped bar chart', 'Chi-square test'),
        ('Bivariate Analysis','Continous Vs. Categorical', 'Grooup by categorical column and aggregate for numerical column', 'Grouped nox plot','T-test: If categorical variable has only 2 levels. ANOVA: If categorical variable has more than two levels. **For both tests just apply if all assumptions are satisfied')
    ]    
    concept_list =  pd.DataFrame(concept_list, columns=['Type of test','Type of data','Summarization','Visualization','Test of Independece'])
   
    return display(Markdown(concept_list.to_markdown(index=False)))

def general_concepts():

    # concept, description, exemplo if applicable
    general_concepts = [("Machine Learning","A.	Machine learning is a field of study in artificial intelligence that involves the development of algorithms and statistical models that enable computers to learn from data without being explicitly programmed. It is a process by which a computer program can improve its performance on a specific task over time by continuously learning from new data. In machine learning, a computer system is fed with a large amount of data and it is trained to identify patterns and relationships in the data, using various statistical and mathematical algorithms. Once the machine learning model has been trained, it can be used to make predictions or decisions based on new, unseen data. Machine learning is used in a wide range of applications, such as image and speech recognition, natural language processing, fraud detection, and recommendation systems, among others. It is an important tool for businesses, researchers, and organizations that need to make sense of large amounts of data and extract meaningful insights from it."),
                ("Cramer V", "In the same way Pearsons Correlation is used for numerical features, in the same way Phi or Cramer V coefficient can be used for Categorical features. Which categorical variables are connected? What is the strength of this relationship? This exercise's goal is to show how to compute correlation and use heatmap to visualize data"),
                ("Unsupervised ML", " Unsupervised machine learnin is a type of machine learning in whinch a model is trained on a dataset wihtout any labeled target variables or output variables. In unsupervised learning, the algorithm is tasked with finding patterns or strucuture in the data on its own, without any extenal guidance or feedback. The goal of unsupervised learning is to discover interesting patterns or realtionships in the data that can be used to gain insights to make predictions about new data. This is often used for tasks sucha as clustering, dimensionality reduction, and anomaly detection (Outliers)."),
                ("PCA", "Principal Component Analysis - PCA is an unsupervised statistical technique that is used to reduce the dimensions of the dataset. ML models with many input variables or higher dimensionality tend to fail when operating on a higher input dataset. PCA helps in identifying relationships among different variables & then coupling them. PCA works on some assumptions which are to be followed and it helps developers maintain a standard. PCA involves the transformation of variables in the dataset into a new set of variables which are called PCs (Principal Components). The principal components would be equal to the number of original variables in the given dataset. \n The first principal component (PC1) contains the maximum variation which was present in earlier variables, and this variation decreases as we move to the lower level. The final PC would have the least variation among variables and you will be able to reduce the dimensions of your feature set."),
                ("Linear Discriminant Analysis or LDA", "Linear discriminant analysis (LDA), normal discriminant analysis (NDA), or discriminant function analysis is a generalization of Fisher's linear discriminant, a method used in statistics and other fields, to find a linear combination of features that characterizes or separates two or more classes of objects or events. The resulting combination may be used as a linear classifier, or, more commonly, for dimensionality reduction before later classification. LDA is closely related to analysis of variance (ANOVA) and regression analysis, which also attempt to express one dependent variable as a linear combination of other features or measurements. However, ANOVA uses categorical independent variables and a continuous dependent variable, whereas discriminant analysis has continuous independent variables and a categorical dependent variable (i.e. the class label). Logistic regression and probit regression are more similar to LDA than ANOVA is, as they also explain a categorical variable by the values of continuous independent variables. These other methods are preferable in applications where it is not reasonable to assume that the independent variables are normally distributed, which is a fundamental assumption of the LDA method. LDA is also closely related to principal component analysis (PCA) and factor analysis in that they both look for linear combinations of variables which best explain the data. LDA is supervised learning when the target is categorical and explicitly attempts to model the difference between the classes of data. PCA, in contrast,is unsupervised learningand  so it does not take into account any difference in class."),
                ("K-nearest neighbors (KNN)", "KNN algorithm is a type of supervied ML algorithm that ca be used for both classification as well as regression predictive problems. However, it is mainly used for the prediction of classification problems in the industry. The following two properties would define KNN well - Lazy learning algorithm - KNN is a lazy learnin algorithm because is does not have a specialized training phase, and uses all the data for training ehile classications. KNN algrithm ate the training phase just sores the datasen and when it gets new data, then it classifies that data into a category that is much similar to the new data. Non-parametric leaning algorithm - KNN is also a non parametric learning algorithm because it doesn't assume anythink about the underlying data. -> IMPORTANT: When you run the kNN algorithm, you have to decide what k should be. Mostly an empricial question; trianl and error experimentally. If k is too small, prediciton will sensitive to noise. If k is too large, algorithm loses the local context that makes it work." ),
                ("Clusterin", "Clustering is dividing whole observations into several groups. Clustering is an unsupervised machine learning technique. It is the process of division of the dataset into groups in which the members in the same group possess similarities in features. The commonly used clustering algorithms are K-Means clustering, Hierarchical clustering, Density-based clustering, Model-based clustering, etc."),
                ("K-Means Clustering", "It is the simplest and most commonly used iterative type unsupervised learning algorithm. K is the number of clusters (groups).  In this, we randomly initialize the K number of centroids in the data (the number of k is found using the Elbow method which will be discussed later in this PowerPoint) and iterates these centroids until no change happens to the position of the centroid. Let’s go through the steps involved in K means clustering for a better understanding."),
                ("Elbow Method", "In the Elbow method, we are actually varying the number of clusters ( K ) from 1 – 10. For each value of K, we are calculating WCSS ( Within-Cluster Sum of Square ). WCSS is the sum of the squared distance between each point and the centroid in a cluster. "),
                ("Perceptron", "Perceptron is an algorithm for binary classification that uses a linear prediction function. 1. Initialize all weights w to 0. 2. Iterate through the training data. For each training instance, classify the instanc . If the prediction (the output of the classifier) was correct, don’t do anythi g. If the prediction was wrong, modify the weights by using the update rulw(j) = (y(i) - f(x(i))).x(i,j) e: where j is feature index, i is instance index and ￿ is the learning r3. te. 1 Repeat step 2 until the perceptron correctly classifiers every instance or the maximum number of iterations has been reached."),
                ("Loss Funciton", " The loss function gives the training error when using parameters w, denoted L(w). Also called cost function or objective function (in general objective could be to minimize or maximize; with loss/cost functions, we want to minimize) .Whenever there is a peak in the data, this is a Maximum. The global maximum is the highest peak in the entire data set, or the largest f(x) value the function can output. A local maximum is any peak, when the rate of change switches from positive to negative."),
                ("Gradient descent", " Gradient descent is an optimization algorithm which is commonly-used to train machine learning models and neural networks. It trains machine learning models by minimizing errors between predicted and actual results. Training data helps these models learn over time, and the cost function within gradient descent specifically acts as a barometer, gauging its accuracy with each iteration of parameter updates. Until the function is close to or equal to zero, the model will continue to adjust its parameters to yield the smallest possible error."),
                ("SVM","Ans SVM is a supervised learning algorithm that finds a hyperplane to separate two (or more) classes, such that the hyperplane is at a maximum distance from the nearest observation of each class. One can think of an SVM classifier as fitting the widest possible street between the classes. The decision boundary is then the center line of this street. ached."),
                ("Kernel Functions", "If classes are not linearly separable, it may requires a transformation to convert them to linear separable (add more dimension/feature). Kernel functions are these generic transformation functions that build new features out of existing features. Some commonn kernel functions are polynomial and Radial Basis function. Polynomial: (x_i * x_j + c)^d. The hyperparameter here is the degree ‘d’ of the polynomial. RBF: e^(−gamma * abs(x_i - x_j)^2) The hyperparameter here is ‘gamma’. Another common hyperparameter for all kernels is C. Hyperparameter C controls the tradeoff between margin size and classification error."),
                ("LOF","Effective in identifying outliers in datasets with varying densities or clusters. Doesn’t require assumptions about the underlying distribution of the data. Provides anomaly scores that can be used to rank the outliers. Cons of employing the LOF method for outlier detection include the following: Sensitivity to the choice of parameters such as the number of neighbors (n_neighbors) and the contamination rate (contamination). Can be computationally expensive for large datasets. May require careful interpretation and adjustment of the anomaly scores threshold for outlier detection. Data enthusiasts can identify outliers based on local density deviations and capture anomalies that display different patterns from their neighbors by using the Local Outlier Factor (LOF) method for outlier detection. To get precise outlier detection, however, parameter tuning and careful result interpretation are necessary."),
                ("Ensembles","An ensemble, a collection of models, is used to make predictions rather than an individual model. Each individual learner in an ensemble is called a base learner. Ensemble models can help in the following: 1) Reducing the variability of individual models, and 2) Combining the best aspects from different models to get the best output for a particular case. If the classifiers in the ensemble make different errors (i.e., the errors are not correlated), then the probability of many classifiers making the same error is much smaller than the probability of any one classifier. The drawbacks of ensembles are: 1) Interpretability: It is hard to extract the overall impact of a specific feature on the prediction, as different base learners would have processed the feature in different ways (e.g., parametric models calculate coefficients, while decision tree-based models use entropy/gini). As the final prediction is an average of several base learners with different strategies and parameters, it is very difficult to estimate a variable's overall contribution to the final prediction. 2) Like decision trees, ensemble methods like Random Forest and AdaBoost are prone to overfitting if allowed to develop in an unrestricted manner. Careful tuning of hyperparameters and pruning is required to avoid overfitting."),
                ("Types fo Ensembles", "1. Bagging: Randomly samples data points from the original dataset with replacement. From each subset of the data, a decision tree is generated, and the outputs of all such trees are combined to arrive at the final prediction (the bagging technique is also known as bootstrap aggregation). Bagging can also be performed on features by randomly allocating a subset of total features to each base learner. In bagging, base learners can be trained in parallel. The output is then combined using some kind of deterministic averaging process to create a strong learner at the end. Random forest, which is one of the bagging models, is composed of deep decision trees to create a forest that has low variance. Thus, this ensemble model resolves the problem of overfitting, which we have when we work with individual decision trees. Random forest is an example of the bagging method. 2. Boosting: Sequentially fits models to the errors of earlier models. In each iteration in boosting, a new classifier is trained to try to correctly classify instances that the previous classifier got wrong. In boosting, weak models are sequentially connected in such a way that the subsequent models are dependent on errors of the previous model. The most popular boosting algorithms are AdaBoost, Gradient Boosting, and XGBoost. The aim of bagging is to reduce variance and not bias, but the aim of boosting is to reduce bias and not variance."),
                ("AdaBoost", "AdaBoost is a common boosting algorithm. AdaBoost stands for adaptive boosting. It uses all training data in every iteration but weighs the training instances differently in each iteration, so the classifier is encouraged to get certain instances correct over others. 1. AdaBoost starts with a uniform distribution of weights over training examples, i.e., it gives equal weights to all its observations. These weights tell the importance of each data point being considered. 2. We start with a single weak learner to make the initial predictions. 3. Once the initial predictions are made, patterns that were not captured by previous weak learners are taken care of by the next weak learner by giving more weightage to the misclassified data points. 4. Apart from giving weightage to each observation, the model also gives weightage to each weak learner. The more errors in the weak learner, the less weightage is given to it. This helps when the ensembled model makes final predictions. 5. After getting these two weights, for the observations and the individual weak learners, the next model (weak learner) in the sequence trains on the resampled data (data sampled according to the weights) to make the next prediction. 6. The model will iteratively continue the steps mentioned above for a prespecified number of weak learners. 7. In the end, we take a weighted sum of the predictions from all these weak learners to get an overall strong learner."),
                ("Natural Language Processing", "Natural Language Understanding helps machines 'read' text (or another input such as speech) by simulating the human ability to understand a natural language such as English, Spanish, or Chinese. Natural Language Processing includes both Natural Language Understanding and Natural Language Generation, which simulates the human ability to create natural language text, e.g., to summarize information or take part in a dialogue. Widely used in knowledge-driven organizations, text mining is the process of examining large collections of documents to discover new information or help answer specific research questions. Text mining identifies facts, relationships, and assertions that would otherwise remain buried in the mass of textual big data. Once extracted, this information is converted into a structured form that can be further analyzed or presented directly using clustered HTML tables, mind maps, charts, etc. The structured data created by text mining can be integrated into databases, data warehouses, or business intelligence dashboards and used for descriptive, prescriptive, or predictive analytics."),
                ("Stemming / Lemmatizing / Stop Words", "Stem – the part of the word that never changes even when different forms of the word are used. It is the main part of the verb to which the endings are added. E.g., the stem of ‘repeated’ is ‘repeat.’ Stemming is the process of reducing unimportant or irrelevant words to their word stem, base, or root form. The process involves removing the last few characters of a given word to obtain a shorter form, even if that form doesn’t have any meaning. Stemming use cases include sentiment analysis, spam classification, etc. Lemma – the verb base or dictionary form of a word, such as do, does, done, and doing, are forms of the same lexeme. Here, 'do' is the lemma. Lemmatization – a process of determining the lemma of a word based on the knowledge of context in the document. Unlike stemming, lemmatization finds meaningful root words, but it takes more time. Its use cases include sentiment chatbots, generative AI, etc."),
                ("Bag of Words", "The key to measuring document similarity is turning documents into vectors based on specific words and their frequencies. Bag of Words is a technique to turn a document of text into a vector of numbers so that the unstructured data is converted into a structured form that can be further analyzed and used in predictive modeling. We start with a template for the vector, which needs a master list of terms. A term can be a word, a number, or anything that appears frequently in documents. There are almost 200,000 words in English – it would take much too long to process document vectors of that length. Commonly, vectors are made from a small number (50–1000) of the most frequently occurring words. A problem with scoring word frequency is that highly frequent words start to dominate in the document (e.g., larger score) but may not contain as much 'informational content' to the model as rarer but perhaps domain-specific words."),
                ("TF-IDF", "One approach is to rescale the frequency of words by how often they appear in all documents so that the scores for frequent words like 'the,' which are also frequent across all documents, are penalized. This approach to scoring is called Term Frequency – Inverse Document Frequency (TF-IDF) for short, where: • Term Frequency: is a scoring of the frequency of the word in the current document. It is a measure of how frequently a term, t, appears in a document, d: tf(t,d) = n(t,d) / Number of terms in the document. Here, in the numerator, n is the number of times the term 't' appears in the document 'd.' Thus, each document and term would have its own TF value. • Inverse Document Frequency: is a scoring of how rare the word is across documents. The inverse document frequency of term t, idf(t), is the log of the number of documents in D divided by the number of those documents that contain the term t: idf(t) = log(number of documents / number of documents with term 't'). We can now compute the TF-IDF score for each word in the corpus. Words with a higher score are more important, and those with a lower score are less important: tf_idf(t,d) = tf(t,d) * idf(t). The scores are a weighting where not all words are equally important or interesting. The scores have the effect of highlighting words that are distinct (contain useful information) in a given document.")
               ]

    general_concepts =  pd.DataFrame(general_concepts, columns=['Concept','Description'])
   
    return display(Markdown(general_concepts.to_markdown(index=False)))


#print("OpenAI module is installed successfully!")
def myresearch(query):
    import openai
    from rich.console import Console
    openai.api_key = "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"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Make sure you're using a chat model
        messages=[{"role": "user", "content": query}]
    )
    result = (response["choices"][0]["message"]["content"])

    console = Console()
    
    return console.print(result)