import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

def data_preprocessing(data):
    st.subheader("🛠️ Data Preprocessing")

    st.subheader("🗑️ Remove Unwanted Columns")
    columns_to_remove = st.multiselect("Select Columns to Remove", data.columns)

    if st.button("Remove Selected Columns"):
        data = data.drop(columns=columns_to_remove)
        st.write("Columns removed successfully!")
        st.write(data.head())

    st.subheader("🕳️ Handle Missing Data")
    missing_data_handling = st.selectbox("Select how to handle missing data", ["Remove Rows", "Fill with Mean", "Fill with Median", "Fill with Mode"])

    if missing_data_handling == "Remove Rows":
        columns_to_remove_missing = st.multiselect("Select columns to remove rows with missing data", data.columns)

        if st.button("Remove Rows with Missing Data"):
            data = data.dropna(subset=columns_to_remove_missing)
            st.write("Rows with missing data removed successfully!")
            st.write(data.head())
    else:
        if st.button("Fill Missing Data"):
            if missing_data_handling == "Fill with Mean":
                data = data.fillna(data.mean())
            elif missing_data_handling == "Fill with Median":
                data = data.fillna(data.median())
            else:
                data = data.fillna(data.mode().iloc[0])
            st.write("Missing data filled successfully!")
            st.write(data.head())

    st.subheader("🕳️ Missing Data Summary:")
    st.write(data.isnull().sum())

    st.subheader("📊 Encode Categorical Data")
    columns_to_encode = st.multiselect("Select Columns to perform encoding", data.select_dtypes(include=['object']).columns)
    encoding_method = st.selectbox("Select Encoding Method", ["One Hot Encoding", "Label Encoding"])

    if st.button("Apply Encoding"):
        if encoding_method == "One Hot Encoding":
            encoder = OneHotEncoder(handle_unknown='ignore')
            encoded_data = pd.DataFrame(encoder.fit_transform(data[columns_to_encode]).toarray())
            encoded_data.columns = encoder.get_feature_names_out(columns_to_encode)
            data = data.drop(columns=columns_to_encode)
            data = pd.concat([data, encoded_data], axis=1)
            st.write("One Hot Encoding applied successfully!")
            st.write(data.head())
        else:
            encoder = LabelEncoder()
            for column in columns_to_encode:
                data[column] = encoder.fit_transform(data[column])
            st.write("Label Encoding applied successfully!")
            st.write(data.head())

    st.subheader("📈 Feature Scaling")
    columns_to_scale = st.multiselect("Select Numerical Columns to Scale", data.select_dtypes(include=['int64', 'float64']).columns)
    scaling_method = st.selectbox("Select Scaling Method", ["Standardization", "Normalization"])

    if st.button("Apply Scaling"):
        if scaling_method == "Standardization":
            scaler = StandardScaler()
            data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])
            st.write("Standardization applied successfully!")
            st.write(data.head())
        else:
            data[columns_to_scale] = (data[columns_to_scale] - data[columns_to_scale].min()) / (data[columns_to_scale].max() - data[columns_to_scale].min())
            st.write("Normalization applied successfully!")
            st.write(data.head())

    st.subheader("📊 Identify and Handle Outliers")
    numeric_column = st.selectbox("Select Numeric Column for Outlier Handling", data.select_dtypes(include=['int64', 'float64']).columns)

    q1 = data[numeric_column].quantile(0.25)
    q3 = data[numeric_column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    outliers = data[(data[numeric_column] < lower_bound) | (data[numeric_column] > upper_bound)]

    if len(outliers) > 0:
        st.write(f"Outliers detected in {numeric_column}:")
        st.write(outliers)

        outlier_handling_method = st.selectbox("Select Outlier Handling Method", ["Remove Outliers", "Replace with Median"])

        if st.button("Apply Outlier Handling"):
            if outlier_handling_method == "Remove Outliers":
                data = data[(data[numeric_column] >= lower_bound) & (data[numeric_column] <= upper_bound)]
                st.write("Outliers removed successfully!")
                st.write(data.head())
            else:
                data.loc[(data[numeric_column] < lower_bound) | (data[numeric_column] > upper_bound), numeric_column] = data[numeric_column].median()
                st.write("Outliers replaced with median successfully!")
                st.write(data.head())
    else:
        st.write(f"No outliers detected in {numeric_column} using IQR.")

    st.subheader("📥 Download Preprocessed Data")
    if st.button("Download"):
        csv_data = data.to_csv(index=False)
        st.download_button(
            label="Download Preprocessed Data",
            data=csv_data,
            file_name='preprocessed_data.csv',
            mime='text/csv'
        )