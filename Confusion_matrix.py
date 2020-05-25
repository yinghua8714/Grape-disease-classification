import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

X_test = np.load('data/ImageTestHOG_input.npy')
y_test = np.load('data/DiseaseTest_input.npy')
print(X_test.shape)
print(y_test.shape)


# Beautify confusion matrix

def make_confusion_matrix(cf,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=None,
                          cmap='Blues',
                          title=None):
    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        row_size = np.size(cf, 0)
        col_size = np.size(cf, 1)
        group_percentages = []
        for i in range(row_size):
            for j in range(col_size):
                group_percentages.append(cf[i][j] / cf[i].sum())
        group_percentages = ["{0:.2%}".format(value) for value in group_percentages]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels, group_counts, group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0], cf.shape[1])

    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        # Accuracy is sum of diagonal divided by total observations
        accuracy = np.trace(cf) / float(np.sum(cf))
        stats_text = "\n\nAccuracy={0:0.2%}".format(accuracy)
    else:
        stats_text = ""

    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize is None:
        # Get default figure size if not set
        figsize = plt.rcParams.get('figure.figsize')

    if not xyticks:
        # Do not show categories if xyticks is False
        categories = False

    # MAKE THE HEAT MAP VISUALIZATION
    plt.figure(figsize=figsize)
    sns.heatmap(cf, annot=box_labels, fmt="", cmap=cmap, cbar=cbar, xticklabels=categories, yticklabels=categories)

    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)

    if title:
        plt.title(title)


# Predicting and determining the confusion matrix

loadedc_model = joblib.load('models/Random_model.sav')
# loadedc_model = joblib.load('models/SVM_model.sav')
classifier_prediction = loadedc_model.predict(X_test)

# classifier_prediction = np.load('models/Ensemble.npy')

corr_rfc = confusion_matrix(y_test, classifier_prediction)

# labelencoder = LabelEncoder()
# y_test1 = labelencoder.fit(y_test)
# en_model = load_model('models/custom_ensemble.h5')
# y_pred = en_model.predict(np.load('X_test_ensemble.npy'))
# vgg_prediction = np.argmax(y_pred, axis=-1)
# vgg_prediction = labelencoder.inverse_transform(vgg_prediction)
# corr_rfc = confusion_matrix(y_test, vgg_prediction)

make_confusion_matrix(corr_rfc, group_names=None,
                      categories=['blackrot', 'ecsa', 'healthy', 'leafblight', 'pmildew'],
                      count=True,
                      percent=True,
                      cbar=False,
                      xyticks=True,
                      xyplotlabels=True,
                      sum_stats=True,
                      figsize=(8, 6),
                      cmap='OrRd',
                      title='Confusion matrix')
# error correction - cropped heat map
b, t = plt.ylim()  # discover the values for bottom and top
b += 0.5  # Add 0.5 to the bottom
t -= 0.5  # Subtract 0.5 from the top
plt.ylim(b, t)  # update the ylim(bottom, top) values
plt.savefig('output/ensemble/confusion_matrix_en2.png', bbox_inches='tight')
