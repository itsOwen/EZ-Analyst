import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(data, feature, plot_type):
    fig, ax = plt.subplots()
    if plot_type == "Histogram":
        sns.histplot(data=data, x=feature, ax=ax)
        ax.set_title(f"Histogram of {feature}")
    elif plot_type == "Box Plot":
        sns.boxplot(data=data, x=feature, ax=ax)
        ax.set_title(f"Box Plot of {feature}")
    else:
        sns.kdeplot(data=data, x=feature, ax=ax)
        ax.set_title(f"KDE Plot of {feature}")
    return fig

def plot_scatter(data, x_feature, y_feature):
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x=x_feature, y=y_feature, ax=ax)
    ax.set_title(f"Scatter Plot: {x_feature} vs {y_feature}")
    return fig

def plot_categorical(data, feature, plot_type):
    fig, ax = plt.subplots()
    if plot_type == "Bar Chart":
        sns.countplot(data=data, x=feature, ax=ax)
        ax.set_title(f"Bar Chart of {feature}")
    else:
        data[feature].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title(f"Pie Chart of {feature}")
    return fig

def plot_numerical_categorical(data, categorical_feature, numerical_feature):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x=categorical_feature, y=numerical_feature, ax=ax)
    ax.set_title(f"Mean {numerical_feature} by {categorical_feature}")
    return fig