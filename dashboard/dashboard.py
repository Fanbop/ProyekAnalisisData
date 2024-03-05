import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def product_sold(df):
    product_id_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_id_counts.sort_values(by='product_id', ascending=False)
    return sorted_df

def order_per_month(df):
    monthly_orders_df = df.resample(rule='M', on='order_approved_at').agg({
        "order_id": "nunique",
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    monthly_orders_df = monthly_orders_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    monthly_orders_df["month_numeric"] = monthly_orders_df["order_approved_at"].map(month_mapping)
    monthly_orders_df = monthly_orders_df.sort_values("month_numeric")
    monthly_orders_df = monthly_orders_df.drop("month_numeric", axis=1)
    return monthly_orders_df

def rating(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    
    max_score = rating_service.idxmax()

    df_cust=df['review_score']

    return (rating_service,max_score,df_cust)


all_df = pd.read_csv("https://raw.githubusercontent.com/Fanbop/ProyekAnalisisData/main/data/all_data.csv")

all_df["order_approved_at"] = pd.to_datetime(all_df["order_approved_at"])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://firebasestorage.googleapis.com/v0/b/bangkit-dashboard/o/production%2F2024-B1%2Fprofiles%2F276daebc-c17a-4d5e-8555-b76387073971.jpeg?alt=media&token=d786f3fb-6e8d-4baa-b164-3bcde0f2278d")
    st.markdown("### Zulfan Zidni Ilhama")
    st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

    st.markdown("### Final Project")

    st.markdown("[Source: E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")

    st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

    st.markdown("### Contact")

    st.markdown(
        """
        - Email: [zulfanzidni@gmail.com](mailto:zulfanzidni@gmail.com)
        - Linkedin: [Zulfan Zidni Ilhama](https://www.linkedin.com/in/zulfanzidni)
        """,
        unsafe_allow_html=True
    )

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu Analisis Data',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))]

# Memanggil fungsi
most_least_product_df = product_sold(main_df)
tren_orders_df = order_per_month(all_df)
rating_service,max_score,df_rating_service=rating(main_df)

# Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #4A3AFF;'>ANALYSIS E-COMMERCE PUBLIC</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# === TREN PENJUALAN PADA PLATFORM E-COMMERCE ===
st.subheader('Tren Penjualan Pada E-Commerce')
col1, col2 = st.columns(2)

with col1:
    high_order_num = tren_orders_df['order_count'].max()
    high_order_month = tren_orders_df[tren_orders_df['order_count'] == tren_orders_df['order_count'].max()]['order_approved_at'].values[0]

with col2:
    low_order = tren_orders_df['order_count'].min()
    low_order_month = tren_orders_df[tren_orders_df['order_count'] == tren_orders_df['order_count'].min()]['order_approved_at'].values[0]

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    tren_orders_df["order_approved_at"],
    tren_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#3366CC",
    linestyle='-',
    mec='black',
    mew=1,
)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=12)
ax.set_title("Tren Penjualan Pada Tahun 2023", fontsize=24)
ax.set_xlabel("Bulan", fontsize=14) 
ax.set_ylabel("Penjualan", fontsize=12) 

st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

# === PRODUK PALING LARIS DAN KURANG DIMINATI ===
st.subheader("Best and Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))  

colors = ["#3366CC", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", data=most_least_product_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=30)
ax[0].tick_params(axis ='y', labelsize=25)
ax[0].tick_params(axis ='x', labelsize=20)

sns.barplot(x="product_id", y="product_category_name_english", data=most_least_product_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

# === TINGKAT KEPUASAN PELANGGAN ====
st.subheader('Tingkat Kepuasan Pelanggan')

def show_barplot(review_scores, most_common_score):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=review_scores.index,
                y=review_scores.values,
                order=review_scores.index,
                palette=["#3366CC" if score == most_common_score else "#D3D3D3" for score in review_scores.index],
                linewidth=1.5)
    plt.title("Tingkat Kepuasan Customer", fontsize=20)
    plt.xticks(fontsize=12)
    st.pyplot(plt)

def rating_cust_df(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    max_score = rating_service.idxmax()
    df_cust = df['review_score']
    return rating_service, max_score, df_cust

rating_service, most_common_score, _ = rating_cust_df(df)

show_barplot(rating_service, most_common_score)

st.caption('Copyright (C) Zulfan Zidni Ilhama. 2024')