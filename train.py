import pandas as pd
import numpy as np
from underthesea import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# 1. Đọc và làm sạch dữ liệu 
train_data = pd.read_csv('data/train_data.csv')
train_data.dropna(subset='clean_content', inplace=True)
train_data.drop_duplicates(subset='clean_content', inplace=True)
    
# 2. Mã hóa biến mục tiêu
train_data['class'] = train_data['class'].str.strip()
train_data['class'] = train_data['class'].map({'positive': 1, 'negative': 0})

# 3. TFIDF vectorizer
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,5), max_df=0.5, min_df=5, sublinear_tf=True, norm='l2')
texts = tfidf_vectorizer.fit_transform(train_data['clean_content'].values.astype('U'))
#df = pd.DataFrame(texts.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
labels = train_data['class']

# 4. Xử lý dữ liệu mất cân bằng
smt = SMOTE(random_state=42)
texts_smt, labels_smt = smt.fit_resample(texts,labels)

# 5. Chia data thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(texts_smt, labels_smt, test_size=0.3, random_state=42)

# 6. Lựa chọn mô hình 
# models = [LogisticRegression(), SVC(), RandomForestClassifier()]
# models_dict = {0: "Logistic Regression", 1: "SVC", 2: "Random Forest"}#
# for i, model in enumerate(models):
#    model.fit(X_train, y_train)
#    y_pred = model.predict(X_test)
#    report = metrics.classification_report(y_test, y_pred, labels=[1,0], digits=3)
#    print(f"Classification Report for model {models_dict[i]}:\n", report)

# 7. Hyperparameter Tuning 
# parameters = {
#     'kernel': ('linear', 'rbf'),
#     'C': [0.125, 0.25, 0.5, 1, 2, 4],
#     'gamma': [0.125, 0.25, 0.5, 1, 2, 4]
# }

# grid = GridSearchCV(SVC(), param_grid=parameters, scoring='accuracy', cv=5)  
# grid_search = grid.fit(X_train, y_train)
# print("Best parameters:", grid_search.best_params_)

# 8. Xây dựng mô hình
model = SVC(C=4, gamma=2, kernel='rbf')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

report1 = metrics.classification_report(y_test, y_pred, labels=[1, 0], digits=3)
print("Classification Report on Test Set:\n", report1)

# 9. Kiếm tra overfitting
# model = SVC(C=4, gamma=2, kernel='rbf')
# model.fit(X_train, y_train)
# y_train_pred = model.predict(X_train)
# report2 = metrics.classification_report(y_train, y_train_pred, labels=[1,0], digits=3)
# print("Classification Report on Train Set:\n", report2)

# 10. Error Analysis
# mismatches = []
# for id, review, true_label, predicted_label in zip(train_data['id'], X_train, y_train, y_train_pred):
#     if true_label != predicted_label:
#         if true_label != 1:
#             mismatches.append(f"{id}, True Label: {true_label}, Predicted Label: {predicted_label}")
#             print(f"{id}, True Label: {true_label}, Predicted Label: {predicted_label}")

# result_length = len(mismatches)
# print(f"Số lượng bản ghi không khớp: {result_length}")

# 12. Tiến hành huấn luyện lại bằng phương pháp CrossValidation
cv_results = cross_val_score(SVC(C=4, gamma=2, kernel='rbf'), X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)

print(f"Cross-validation Accuracy Scores: {cv_results}")
print(f"Mean Accuracy: {cv_results.mean()}")
print(f"Standard Deviation: {cv_results.std()}")

# 13. Áp dụng mô hình đã huấn luyện lên tập test 
def doc_lam_sach_du_lieu(filepath):
    data = pd.read_csv(filepath)
    data = processing_text(data)
    data.dropna(subset='clean_content', inplace=True)
    data.drop_duplicates(subset='clean_content', inplace=True)
    return data

test_data = doc_lam_sach_du_lieu('data/test_data.csv')
test_data['content'] = test_data['clean_content'].values.astype('U')
test_list_vectorized = tfidf_vectorizer.transform(test_data['content']) 
y_predict =model.predict(test_list_vectorized)
test_data['class'] = y_predict
test_data = test_data.sort_values(by=['class'])
test_data[['id', 'clean_content', 'class']].to_csv('data/submit.csv', index=False)