"""
Author: Akhmad Jundan Hidayatulloh
Date: 02/03/2024
This is the dashboard.py module.
Usage:
- This module is used to create a dashboard for the bike sharing data.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_data():
    try:
        # # Print current directory for debugging
        # st.write("Current directory:", os.getcwd())

        # # List files in the directory for debugging
        # st.write("Files in directory:", os.listdir())

        # Load data
        # file_path = "./main_data.csv"
        file_path = "data/main_data.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. File not found.")
        return None


def monthly_count(data):
    # Define the order of the months
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    # Convert 'month' column to categorical with the specified order
    data["month"] = pd.Categorical(data["month"], categories=month_order, ordered=True)

    # Group by 'month' and aggregate the total counts
    return data.groupby("month").agg({"total_count": "sum"}).reset_index()


def yearly_count(data):
    return data.groupby(["year", "month"]).agg({"total_count": "sum"}).reset_index()


def monthly_weekday_count(data):
    return (
        data.groupby(["month", "workingday"])
        .agg({"total_count": ["mean", "sum"]})
        .reset_index()
    )


def hourly_count(data):
    return data.groupby("hour").agg({"total_count": "sum"}).reset_index()


def best_hour_select(data):
    return data.groupby("hour").agg({"total_count": "sum"}).idxmax()["total_count"]


def worst_hour_select(data):
    return data.groupby("hour").agg({"total_count": "sum"}).idxmin()["total_count"]


def season_year_data(data):
    return data.groupby(["season", "year"]).agg({"total_count": "sum"}).reset_index()


def seasonal(data):
    return (
        data.groupby(["date", "season"])
        .agg({"temp": "mean", "total_count": "sum"})
        .reset_index()
    )


def dailydata(data):
    return data.groupby("date").agg({"total_count": "sum"}).reset_index()


def weekly_trend(data):
    # Ensure 'date' column is of type datetime
    week = data.copy()
    week["date"] = pd.to_datetime(week["date"])

    # Set 'date' column as the index
    week.set_index("date", inplace=True)

    # Resample the data to weekly intervals and calculate the mean
    weekly_average = week.resample("W").mean()

    return weekly_average


# Set the page configuration
st.set_page_config(
    page_title="Bike Sharing Data Visualization",
    page_icon="🚲",
    layout="wide",
)

# Load the cleaned data
main_data = load_data()
main_data.head()

# Center-align the title
st.markdown(
    "<h1  style='text-align: center;'>Bike Sharing Data Visualization</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# call functions
monthly_counts = monthly_count(main_data)
yearly_counts = yearly_count(main_data)
monthly_weekday_counts = monthly_weekday_count(main_data)
hourly_data = hourly_count(main_data)
best_hour = best_hour_select(main_data)
worst_hour = worst_hour_select(main_data)
season_year = season_year_data(main_data)
seasonal_data = seasonal(main_data)
daily_data = dailydata(main_data)
weekly_average = weekly_trend(daily_data)

# Total Bike User Section
total_users = main_data["total_count"].sum()
casual_users = main_data["casual"].sum()
registered_users = main_data["registered"].sum()


col1, col2, col3 = st.columns(3)

# Total User
with col1:
    st.markdown(
        """
    <div style='text-align: center; border: 2px solid #ccc; padding: 10px; margin-bottom: 10px;'>
        <h3>Total Bike Users</h3>
        <div style='border-top: 2px solid #ccc; padding-top: 10px;'>
            <h1>{}</h1>
        </div>
    </div>
    """.format(
            total_users
        ),
        unsafe_allow_html=True,
    )

# Casual User
with col2:
    st.markdown(
        """
    <div style='text-align: center; border: 2px solid #ccc; padding: 10px; margin-bottom: 10px;'>
        <h3>Casual Bike Users</h3>
        <div style='border-top: 2px solid #ccc; padding-top: 10px;'>
            <h1>{}</h1>
        </div>
    </div>
    """.format(
            casual_users
        ),
        unsafe_allow_html=True,
    )

# Registered User
with col3:
    st.markdown(
        """
    <div style='text-align: center; border: 2px solid #ccc; padding: 10px; margin-bottom: 10px;'>
        <h3>Registered Bike Users</h3>
        <div style='border-top: 2px solid #ccc; padding-top: 10px;'>
            <h1>{}</h1>
        </div>
    </div>
    """.format(
            registered_users
        ),
        unsafe_allow_html=True,
    )
st.markdown("<hr><br>", unsafe_allow_html=True)

with st.container():
    st.subheader("Monthly Bike Sharing User")
    chart1, chart2 = st.columns(2)

    with chart1:
        chart1 = plt.figure(figsize=(8, 5), facecolor="w")
        sns.lineplot(
            x="month",
            y="total_count",
            data=monthly_counts,
            color="skyblue",
            marker="o",
            sort=False,
        )
        plt.title("Monthly Bike sharing User", color="w")
        plt.xlabel("Month", color="w")
        plt.ylabel("Total Rental Counts", color="w")
        plt.xticks(
            range(12),
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        )
        plt.grid(True)
        st.pyplot(chart1)

    with chart2:
        # Sorting the monthly counts
        sorted_monthly_counts = monthly_counts.sort_values(
            by="total_count", ascending=True
        )
        # Assigning colors to highest and lowest months
        colors = [
            (
                "red"
                if x in sorted_monthly_counts.head(1)["month"].values
                else (
                    "green"
                    if x in sorted_monthly_counts.tail(1)["month"].values
                    else "gray"
                )
            )
            for x in sorted_monthly_counts["month"]
        ]
        chart2 = plt.figure(figsize=(8, 5))
        plt.barh(
            sorted_monthly_counts["month"],
            sorted_monthly_counts["total_count"],
            color=colors,
        )
        plt.title("Monthly Performance of Bike Sharing Users (2011-2012)")
        plt.xlabel("Total Count")
        plt.ylabel("Month")
        plt.grid(axis="x")
        plt.legend(
            handles=[
                plt.Rectangle((0, 0), 1, 1, color="red", ec="k"),
                plt.Rectangle((0, 0), 1, 1, color="green", ec="k"),
                plt.Rectangle((0, 0), 1, 1, color="gray", ec="k"),
            ],
            labels=[
                "Lowest Performing Month",
                "Highest Performing Month",
                "Other Months",
            ],
            loc="lower right",
        )
        st.pyplot(chart2)

    st.write(
        """
            **Analisis:**
            Berdasarkan analisis grafik, jumlah pengguna bike sharing mengalami peningkatan dari bulan Januari hingga Mei, mencapai puncaknya pada bulan Agustus, dan kemudian mengalami penurunan dari bulan Oktober hingga Desember.
            - Pada bulan Mei, terjadi peningkatan signifikan dalam jumlah pengguna, yang mencapai puncaknya pada bulan Agustus. 
            - Pada bulan Agustus, jumlah pengguna mencapai titik tertinggi dengan total 345,991 pengguna. Sebaliknya, jumlah pengguna terendah tercatat pada bulan Januari, dengan hanya 134,933 pengguna.
            
            Ini menunjukkan bahwa musim panas (agustus) cenderung menjadi waktu yang paling populer bagi pengguna bike sharing, sedangkan penggunaan cenderung menurun selama bulan-bulan dengan cuaca yang lebih dingin.
            """
    )


with st.container():
    st.subheader("Monthly Bike Sharing User from Jan 2011 to Des 2012")
    st.markdown("<hr>", unsafe_allow_html=True)
    chart3 = plt.figure(figsize=(8, 4))
    plt.plot(yearly_counts["total_count"], marker="o", linestyle="-")
    # Customize the plot
    plt.title("Monthly Bike Sharing User (2011-2012)")
    plt.xlabel("Months")
    plt.ylabel("Total Counts")
    plt.xticks(
        ticks=range(len(yearly_counts)),
        labels=[
            f"{year}-{month}"
            for year, month in zip(yearly_counts["year"], yearly_counts["month"])
        ],
        rotation=45,
    )
    plt.grid(True)
    # Show plot
    plt.tight_layout()
    st.pyplot(chart3)

    st.write(
        """
                **Analisis:**
                - Jumlah pengguna bike sharing mengalami peningkatan yang signifikan dari tahun 2011 ke tahun 2012.
                - Peningkatan ini terjadi secara konsisten dari bulan Januari 2011 hingga Juni 2011 dan bulan Januari 2012 hingga September 2012.
                - Bulan September 2012 mencatat jumlah pengguna tertinggi dengan total 218,573 pengguna.
                - Secara keseluruhan, jumlah pengguna bike sharing pada tahun 2012 lebih tinggi dibandingkan dengan tahun 2011 pada setiap bulannya.
            """
    )


with st.container():
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(
        "The Influence of Working Day and Weekend on Monthly Bike Sharing Rental Counts"
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    work1, work2 = st.columns(2)
    with work1:
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="month",
            y=("total_count", "mean"),
            hue="workingday",
            data=monthly_weekday_counts,
        )
        plt.title("Average Rental Counts per Month: Workingday vs Weekend (Using Mean)")
        plt.xlabel("Month")
        plt.ylabel("Average Rental Counts")
        plt.xticks(rotation=45)
        avg_counts_mean_fig = plt.gcf()
        st.pyplot(avg_counts_mean_fig)

    with work2:
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="month",
            y=("total_count", "sum"),
            hue="workingday",
            data=monthly_weekday_counts,
        )
        plt.title("Total Rental Counts per Month: Workingday vs Weekend (Using Sum)")
        plt.xlabel("Month")
        plt.ylabel("Total Rental Counts")
        plt.xticks(rotation=45)
        total_counts_sum_fig = plt.gcf()
        st.pyplot(total_counts_sum_fig)

    st.write(
        """
                **Analisis:**
                - Penggunaan sepeda cenderung lebih tinggi pada akhir pekan dibandingkan dengan hari kerja, kecuali pada bulan Desember.
                - Terdapat tren peningkatan penggunaan sepeda dari Januari hingga Juni, kemudian menurun hingga November, sebelum turun secara signifikan pada bulan Desember.
                - Puncak penggunaan sepeda biasanya terjadi pada bulan-bulan musim panas (Juni, Juli, Agustus), sementara penurunan terjadi pada bulan-bulan musim dingin (Desember, Januari, Februari).
                - Terdapat variasi signifikan dalam penggunaan sepeda antar bulan, yang mungkin dipengaruhi oleh faktor seperti cuaca dan libur.
                - Meskipun rata-rata penggunaan sepeda per hari lebih tinggi pada akhir pekan, jumlah total penggunaan sepeda pada hari kerja sebenarnya lebih tinggi karena jumlah hari kerja yang lebih banyak.
            """
    )


with st.container():
    hour1, season1 = st.columns(2)
    with hour1:
        st.subheader("Hourly Bike Sharing User")
        st.markdown("<hr>", unsafe_allow_html=True)
        hourly_fig = plt.figure(figsize=(10, 6))
        plt.bar(hourly_data["hour"], hourly_data["total_count"], color="skyblue")
        plt.xlabel("Hour")
        plt.ylabel("Total Count")
        plt.title("Total Bike Share Usage by Hour")
        plt.xticks(hourly_data["hour"])
        plt.axvline(x=best_hour, color="green", linestyle="--", label="Best Hour")
        plt.axvline(x=worst_hour, color="red", linestyle="--", label="Worst Hour")
        plt.legend()
        plt.close(
            hourly_fig
        )  # Close the figure to prevent it from being displayed prematurely
        st.pyplot(hourly_fig)

        st.write(
            """
                 **Analisis:**
                 
                 **Jam Terbaik (Best Performing Hour):**
                 - Puncak penggunaan sepeda terjadi pada jam 17:00 dan 18:00, menunjukkan aktivitas tinggi pada sore hari setelah bekerja atau sekolah.
                 
                 **Jam Terburuk (Worst Performing Hour):**
                 - Penggunaan sepeda terendah terjadi pada jam 4:00 pagi, saat kebanyakan orang sedang tidur.
                 
                 **Polanya Tren Penggunaan Sepeda:**
                 - Penggunaan sepeda meningkat setelah jam 6:00 pagi dan mencapai puncaknya pada sore hari antara jam 17:00 dan 18:00, kemudian cenderung menurun menjelang malam.
                  """
        )

    with season1:
        st.subheader("Bike Sharing User by Season")
        st.markdown("<hr>", unsafe_allow_html=True)
        season1 = plt.figure(figsize=(10, 6))
        sns.barplot(
            x="season", y="total_count", hue="year", data=season_year, palette="Set2"
        )
        plt.title("Total Count of Bikes by Season in 2011 and 2012")
        plt.xlabel("Season")
        plt.ylabel("Total Count of Bikes")
        plt.legend(title="Year")
        plt.show()
        st.pyplot(season1)

        st.write(
            """
                 **Analisis:**
                    
                    **Musim Panas Menjadi Puncak Peningkatan:** 
                    - Jumlah penyewa sepeda mencapai puncaknya selama musim panas, dengan total 1,060,129 penyewa pada tahun 2011 dan 2012.

                    **Musim Semi dan Musim Gugur Mencatat Jumlah Tinggi:** 
                    - Meskipun tidak sebanyak musim panas, musim semi dan musim gugur juga mencatat jumlah penyewa yang tinggi, dengan total 918,589 penyewa pada tahun 2011 dan 2012.
                    
                    **Musim Dingin Menunjukkan Peningkatan yang Lebih Kecil:**
                    - Meskipun memiliki jumlah penyewa yang lebih rendah, musim dingin juga menunjukkan peningkatan dari tahun 2011 ke tahun 2012, naik dari 150,000 penyewa menjadi 321,348 penyewa.
                """
        )


st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("Extra Information")
tab1, tab2, tab3, tab4 = st.tabs(
    ["Count", "Temperature", "Season", "daily/weekly trent"]
)

with tab1:
    charT1, charT2 = st.columns(2)
    charT3, charT4 = st.columns(2)
    with charT1:
        charT1 = plt.figure(figsize=(8, 6))
        sns.histplot(main_data["temp"], bins=20, kde=True, color="blue")
        plt.title("Distribution of Temperature")
        plt.xlabel("Temperature")
        plt.ylabel("Frequency")
        plt.show()
        st.pyplot(charT1)

    with charT2:
        charT2 = plt.figure(figsize=(8, 6))
        ax = sns.barplot(
            x="season", y="total_count", data=main_data, palette="Set2", errorbar=None
        )
        plt.title("Box Plot of Total Count by Season")
        plt.xlabel("Season")
        plt.ylabel("Total Count")
        # Menambahkan label angka di atas setiap bar
        for p in ax.patches:
            ax.annotate(
                format(p.get_height(), ".0f"),
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 5),
                textcoords="offset points",
            )
        plt.show()
        st.pyplot(charT2)

    with charT3:
        charT3 = plt.figure(figsize=(8, 6))
        ax = sns.countplot(x="weather", data=main_data, palette="rainbow")
        plt.title("Count of Weather Categories")
        plt.xlabel("Weather")
        plt.ylabel("Count")

        # Menambahkan label angka di atas setiap bar
        for p in ax.patches:
            ax.annotate(
                format(p.get_height(), ".0f"),
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 5),
                textcoords="offset points",
            )

        plt.show()
        st.pyplot(charT3)

    with charT4:
        charT4 = plt.figure(figsize=(8, 6))
        sns.boxplot(x="weather", y="temp", data=main_data)
        plt.title("Persebaran Suhu Berdasarkan Cuaca")
        plt.xlabel("Weather")
        plt.ylabel("Temperature (Celsius)")
        plt.show()
        st.pyplot(charT4)

with tab2:
    total_user, casual, registered = st.columns(3)
    with total_user:
        # Scatter plot untuk melihat hubungan temoerature dan total pengguna penguna
        total_user = plt.figure(figsize=(8, 6))
        sns.scatterplot(x="temp", y="total_count", data=main_data, hue="weather")
        plt.title("Total Bike Sharing User in Different Temperature", color="w")
        plt.xlabel("Temperature")
        plt.ylabel("Total user")
        plt.tick_params(axis="x")
        plt.tick_params(axis="y")
        plt.show()
        st.pyplot(total_user)

    with casual:
        # Scatter plot untuk melihat hubungan temoerature dan penguna casual
        casual = plt.figure(figsize=(8, 6))
        sns.scatterplot(x="temp", y="casual", data=main_data, hue="weather")
        plt.title("Casual Bike Sharing User in Different Temperature")
        plt.xlabel("Temperature")
        plt.ylabel("Casual")
        plt.show()
        st.pyplot(casual)

    with registered:
        # Scatter plot untuk melihat hubungan temoerature dan penguna registered
        registered = plt.figure(figsize=(8, 6))
        sns.scatterplot(x="temp", y="casual", data=main_data, hue="weather")
        plt.title("Registered pengguna register pada berbagai suhu")
        plt.xlabel("Temperature")
        plt.ylabel("Registered")
        plt.show()
        st.pyplot(registered)

with tab3:
    season2, season3 = st.columns(2)
    with season3:
        season3 = plt.figure(figsize=(10, 6))
        ax = sns.countplot(x="season", hue="weather", data=main_data, palette="pastel")

        # Menambahkan label angka di atas setiap bar
        for p in ax.patches:
            ax.annotate(
                format(p.get_height(), ".0f"),
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 5),
                textcoords="offset points",
            )

        plt.title("Count of Weather Categories by Season")
        plt.xlabel("Season")
        plt.ylabel("Count")
        plt.show()
        st.pyplot(season3)

    with season2:
        season2 = plt.figure(figsize=(10, 6))
        sns.scatterplot(x="temp", y="total_count", data=seasonal_data, hue="season")
        plt.xlabel("Temperature (deg C)")
        plt.ylabel("Total Rides")
        plt.title("Clusters of bikeshare rides by season and temperature (2011-2012)")
        plt.tight_layout()
        plt.show()
        st.pyplot(season2)


with tab4:
    st.subheader("Daily and Weekly Trend of Bike Sharing Rental Counts")

    daily = plt.figure(figsize=(12, 6))
    sns.lineplot(
        x="date", y="total_count", data=daily_data, color="skyblue", sort=False
    )
    plt.title("Daily Bike Sharing User")
    plt.xlabel("Date")
    plt.ylabel("Total Rental Counts")
    plt.xticks(rotation=30)
    # Pick 10 dates from the entire range of dates
    date_range = pd.date_range(
        start=daily_data["date"].min(), end=daily_data["date"].max(), freq="D"
    )
    tick_indices = range(0, len(date_range), len(date_range) // 10)
    plt.xticks(ticks=tick_indices, labels=date_range[tick_indices].strftime("%Y-%m-%d"))

    plt.grid(True)
    plt.tight_layout()
    plt.show()
    st.pyplot(daily)

    weekly = plt.figure(figsize=(12, 6))
    sns.lineplot(
        x="date",
        y="total_count",
        data=weekly_average,
        color="blue",
        marker="o",
        sort=False,
    )
    plt.title("Weekly Trend of Bike Rentals")
    plt.xlabel("Date")
    plt.ylabel("Total Count")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
    st.pyplot(weekly)


st.caption("Copyright (c) akhmad jundan hidayatulloh 2024")
