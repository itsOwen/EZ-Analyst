import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import plot_distribution, plot_scatter, plot_categorical, plot_numerical_categorical

def data_exploration(data):
    st.subheader("🔍 Data Exploration")

    st.subheader("📋 Dataset Preview")
    num_rows = st.slider("Select the number of rows to display", 5, 50, 5)
    st.write(data.head(num_rows))

    st.subheader("📊 Dataset Overview")
    st.write(f"**Rows:** {data.shape[0]}")
    st.write(f"**Columns:** {data.shape[1]}")
    st.write(f"**Duplicates:** {data.duplicated().sum()}")

    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

    st.write(f"**Categorical Columns:** {len(categorical_columns)}")
    st.write(categorical_columns)
    st.write(f"**Numerical Columns:** {len(numerical_columns)}")
    st.write(numerical_columns)

    st.subheader("🕳️ Missing Values")
    missing_data = data.isnull().sum().reset_index()
    missing_data.columns = ['Column', 'Missing Count']
    st.write(missing_data)

    st.subheader("📈 Data Statistics and Visualization")

    st.subheader("🔢 Summary Statistics for Numerical Columns")
    st.write(data[numerical_columns].describe())

    st.subheader("📊 Statistics for Categorical Columns")
    num_categorical = st.slider("Select the number of categorical columns to visualize", 1, len(categorical_columns), 1)
    selected_categorical = st.multiselect("Select the Categorical Columns for bar chart", categorical_columns, default=categorical_columns[:num_categorical])

    for column in selected_categorical:
        st.subheader(f"📊 Value Count for {column}")
        st.write(data[column].value_counts())

    st.subheader("📋 Data Types")
    data_types = data.dtypes.reset_index()
    data_types.columns = ['Column', 'Data Type']
    st.write(data_types)

    search_column = st.text_input("Search for a column")
    search_datatype = st.selectbox("Filter by Data Type", ['All'] + data.dtypes.unique().tolist())

    if search_column:
        filtered_data_types = data_types[data_types['Column'].str.contains(search_column, case=False)]
    else:
        filtered_data_types = data_types

    if search_datatype != 'All':
        filtered_data_types = filtered_data_types[filtered_data_types['Data Type'] == search_datatype]

    st.write(filtered_data_types)

    st.subheader("📊 Analyze Individual Feature Distribution")
    st.write("Here, you can explore individual numerical features, visualize their distributions, and analyze relationships between features.")

    selected_feature = st.selectbox("Select Numerical Feature", numerical_columns)

    st.subheader("📈 Distribution Plots")
    plot_type = st.selectbox("Select Plot Type", ["Histogram", "Box Plot", "KDE Plot"])
    fig = plot_distribution(data, selected_feature, plot_type)
    st.pyplot(fig)

    st.subheader("📈 Scatter Plot")
    x_feature = st.selectbox("Select X-Axis Feature", numerical_columns)
    y_feature = st.selectbox("Select Y-Axis Feature", numerical_columns)
    fig = plot_scatter(data, x_feature, y_feature)
    st.pyplot(fig)

    st.subheader("📊 Categorical Variable Analysis")
    selected_categorical_feature = st.selectbox("Select Categorical Feature", categorical_columns)
    categorical_plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Pie Chart"])
    fig = plot_categorical(data, selected_categorical_feature, categorical_plot_type)
    st.pyplot(fig)

    st.subheader("🔍 Feature Exploration of Numerical Variables")
    selected_features = st.multiselect("Select Features for Exploration", numerical_columns)

    if len(selected_features) > 1:
        st.subheader("🔍 Explore Relationships Between Features")
        if st.button("Generate Scatter Plot Matrix"):
            fig = sns.pairplot(data[selected_features])
            st.pyplot(fig)

        if st.button("Generate Pair Plot"):
            fig = sns.pairplot(data[selected_features], diag_kind='kde')
            st.pyplot(fig)

        if st.button("Generate Correlation Heatmap"):
            fig, ax = plt.subplots()
            sns.heatmap(data[selected_features].corr(), annot=True, cmap='coolwarm', ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

    st.subheader("📊 Categorical and Numerical Variable Analysis")
    selected_categorical_feature = st.selectbox("Categorical Feature", categorical_columns)
    selected_numerical_feature = st.selectbox("Numerical Feature", numerical_columns)
    fig = plot_numerical_categorical(data, selected_categorical_feature, selected_numerical_feature)
    st.pyplot(fig)