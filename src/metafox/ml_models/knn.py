from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

# knn Classifier
class KNNClassifier:
    def __init__(self, n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.metric = metric
        self.metric_params = metric_params
        self.n_jobs = n_jobs

    def fit(self, X, y):
        self.model = KNeighborsClassifier(
            n_neighbors=self.n_neighbors, 
            weights=self.weights, 
            algorithm=self.algorithm, 
            leaf_size=self.leaf_size, 
            p=self.p, 
            metric=self.metric, 
            metric_params=self.metric_params, 
            n_jobs=self.n_jobs
        )
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def get_params(self):
        return self.model.get_params()
    
# knn Regressor
class KNNRegressor:
    def __init__(self, n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.metric = metric
        self.metric_params = metric_params
        self.n_jobs = n_jobs

    def fit(self, X, y):
        self.model = KNeighborsRegressor(
            n_neighbors=self.n_neighbors, 
            weights=self.weights, 
            algorithm=self.algorithm, 
            leaf_size=self.leaf_size, 
            p=self.p, 
            metric=self.metric, 
            metric_params=self.metric_params, 
            n_jobs=self.n_jobs
        )
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
    
    def get_params(self):
        return self.model.get_params()