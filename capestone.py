import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(layout='wide')
st.title("Produksi Listrik dan Dampaknya Terhadap Lingkungan")
st.write("Emisi CO2 dari energi merujuk pada jumlah karbon dioksida (CO2) yang dilepaskan ke atmosfer sebagai hasil dari produksi, distribusi, dan konsumsi energi. Energi adalah faktor utama yang mendukung berbagai kegiatan manusia, tetapi banyak sumber energi konvensional seperti bahan bakar fosil (batu bara, minyak bumi, dan gas alam) menghasilkan emisi gas rumah kaca, khususnya CO2, yang berkontribusi pada perubahan iklim global.")

tab1, tab2, tab3 = st.tabs(['Emisi', 'Listik', 'Solusi'])
with tab1:
    # data pertama
    st.header("Emisi CO2 dari Energi")
    st.write("Emisi CO2 cenderung lebih tinggi di negara-negara yang perekonomiannya lebih maju, namun juga dapat sangat bervariasi tergantung pada struktur perekonomian dan sistem energinya. Misalnya, emisi per kapita akan lebih tinggi di negara-negara yang lebih bergantung pada moda transportasi padat karbon (seperti kendaraan pribadi dan penerbangan), mempunyai energi padat industri (seperti baja atau bahan kimia) atau sangat bergantung pada bahan bakar fosil untuk pembangkit listrik.")
    st.write("Angka di bawah ini mengacu pada emisi CO2 dari pembakaran bahan bakar di sektor energi. Data tersebut tidak mencakup sumber emisi gas rumah kaca penting lainnya yang terkait dengan energi seperti kebocoran metana dari operasi minyak dan gas, yang lebih sulit diukur.")
    df = pd.read_csv(r"C:\Users\adics\my_project\CO2 emissions from fuel combustion, Indonesia.csv")
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df.rename(columns={'CO2 emissions from fuel combustion, Indonesia': 'CO2'}, inplace=True)
    # dashboard metric
    col1, col2 = st.columns(2)
    with col1:
        latest_year = df.iloc[-1]
        st.metric("Emissions Mt CO2", value=latest_year['CO2'], delta=f'Year {latest_year["Year"].year}')
    
    with col2:
        oldest_year = df.iloc[0]
        latest_year = df.iloc[-1]
        growth_percentage = ((latest_year['CO2'] - oldest_year['CO2']) / oldest_year['CO2']) * 100
        st.metric("Trend", value=f'{growth_percentage:.2f}%', delta=f'Tahun {oldest_year["Year"].year} ke {latest_year["Year"].year}')
    # teks container
    col3, col4, col5 = st.columns([1,3,1])
    with col4:
        custom_container = st.container(border=True)
        with custom_container:
    # Membuat Grafik Trend Garis dengan Altair
            sales_line = alt.Chart(df).mark_line().encode(
                x='Year',
                y='CO2',
                tooltip= ['CO2', 'Year']
                ).properties(
                    title='Trend Emisi CO2',)
        # Menampilkan Grafik dengan Streamlit
            st.altair_chart(sales_line, use_container_width=True)
    st.header("Emisi CO2 Berdasarkan Sektor")
    st.write("Emisi CO2 yang dilepaskan ke atmosfer sebagai hasil dari produksi, distribusi, dan konsumsi energi. Berbagai sektor kegiatan manusia. berkontribusi masing-masing terhadap emisi gas rumah kaca. Beberapa sektor utama yang berkontribusi terhadap emisi CO2 termasuk:")
    st.markdown("""
    1. __Pembangkit Listrik:__ Pembangkit listrik tenaga batu bara, minyak, dan gas alam adalah penyumbang besar emisi CO2. Proses pembakaran untuk menghasilkan listrik melepaskan gas buang yang mengandung CO2 ke atmosfer.
    2. __Transportasi:__ Penggunaan bahan bakar fosil dalam transportasi, terutama bensin dan diesel, menyebabkan emisi CO2 yang signifikan. Mobil, truk, pesawat terbang, dan kapal yang menggunakan bahan bakar fosil menghasilkan CO2 selama proses pembakaran.
    3. __Industri:__ Proses industri yang mengandalkan energi dari bahan bakar fosil, seperti produksi logam, semen, dan kimia, juga berkontribusi terhadap emisi CO2. Energi dibutuhkan untuk memanaskan tungku, menghasilkan uap, dan menyediakan daya.""")
    # data kedua
    df2 = pd.read_csv(r"C:\Users\adics\my_project\CO2 emissions by sector, Indonesia, 2021.csv")
    df2.rename(columns={'CO2 emissions by sector, Indonesia, 2021': 'Sektor'}, inplace=True)
    # bar sektor
    df = pd.DataFrame(df2)
    # Menambahkan kolom persentase
    df['persentase'] = ((df['Value'] / df['Value'].sum()) * 100).round(2)
    # Mengelompokkan nilai di bawah 5% menjadi 'lain-lain'
    df.loc[df['persentase'] < 5, 'Sektor'] = 'lain-lain'
    df = df.groupby('Sektor', as_index=False).agg({'Value': 'sum', 'persentase': 'sum'})
    df['persentase2'] = df['persentase'].astype(str)+'%'
    # dashboard metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sektor", value=df.iloc[-0]['persentase2'], delta= df.iloc[-0]["Sektor"])
    with col2:
        st.metric("Sektor", value=df.iloc[-2]['persentase2'], delta= df.iloc[-2]["Sektor"])
    # Membuat bar chart menggunakan Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Sektor', sort= '-y'),
        y=alt.Y('Value', axis=alt.Axis(title='Emisi MtCO2')),
        tooltip=['Sektor', 'Value', 'persentase']
        ).properties(
            width=400,
    title='Emisi CO2 Berdasarkan Sektor 2021')
    # Menambahkan teks persentase di atas setiap bar
    text = chart.mark_text(align='center', baseline='bottom', dy=-5).encode(
    text='persentase2:N')
    # Menggabungkan chart dan teks
    final_chart = (chart + text).configure_axisX(labelAngle=0)
    # Tampilkan grafik
    _, midcol, _= st.columns([1,2,1])
    with midcol:
        st.altair_chart(final_chart)
with tab2:
    st.header("Sumber Pembangkit Listrik")
    st.write("Pembangkit listrik adalah fasilitas atau sistem yang mengubah sumber energi menjadi listrik. Ada berbagai sumber energi yang digunakan untuk pembangkit listrik, dan mereka dapat dibagi menjadi dua kategori utama: sumber energi konvensional dan sumber energi terbarukan.")    
    st.markdown("""
    __Sumber Energi Konvensional:__ Sumber energi ini mempunyai kelebihan yaitu: efisien, skala besar, dapat beroperasi secara kontinu. Kekurangannya adalah emisi gas rumah kaca dan ketergantungan bahan bakar fosil         
    1. __Pembangkit Listrik Tenaga Uap (PLTU):__ PLTU menggunakan bahan bakar fosil seperti batu bara untuk memanaskan air menjadi uap. Uap tersebut kemudian digunakan untuk memutar turbin yang menghasilkan listrik.
    2. __Pembangkit Listrik Tenaga Gas (PLTG):__ PLTG menggunakan gas alam untuk menghasilkan listrik melalui pembakaran dalam mesin pembangkit.
    3. __Pembangkit Listrik Tenaga Diesel:__ Pembangkit ini menggunakan mesin diesel (BBM) untuk menghasilkan listrik melalui pembakaran bahan bakar diesel.""")
    st.markdown("""
    __Sumber Energi Terbarukan:__ Sumber energi ini mempunyai kelebihan bersih, ramah lingkungan, sumber energi tak terbatas, dapat menggunakan sampah organik, dan berkelanjutan. Kekurangannya adalah tergantung pada cuaca, biaya awal tinggi, tuntutan lahan, terbatas pada lokasi geografis tertentu.
    1. __Pembangkit Listrik Tenaga Surya:__ Mengubah energi matahari menjadi listrik menggunakan sel surya (panel surya).
    2. __Pembangkit Listrik Tenaga Angin:__ Mengonversi energi kinetik angin menjadi listrik melalui turbin angin.
    3. __Pembangkit Listrik Tenaga Air (PLTA):__ Menggunakan energi air aliran atau potensial untuk menggerakkan turbin dan menghasilkan listrik.
    4. __Pembangkit Listrik Tenaga Biomassa:__ Menggunakan bahan organik seperti kayu, limbah pertanian, atau sampah organik untuk menghasilkan listrik.           
    5. __Pembangkit Listrik Tenaga Geotermal:__ Memanfaatkan panas bumi dari dalam bumi untuk menghasilkan uap dan menggerakkan turbin.""")
    # data ketiga
    pembangkit = pd.read_csv(r"C:\Users\adics\my_project\Electricity generation sources, Indonesia, 2021.csv")
    emisibbm= pd.read_csv(r"C:\Users\adics\my_project\Emissions from power generation by source, Indonesia, 2021.csv")
    pembangkit.rename(columns={'Electricity generation sources, Indonesia, 2021': 'sumber'}, inplace=True)
    emisibbm.rename(columns={'Emissions from power generation by source, Indonesia, 2021': 'sumber'}, inplace=True)
    merged_df2 = pd.merge(pembangkit, emisibbm, on='sumber')
    merged_df2.rename(columns={'Value_x': 'Listrik GWh', 'Value_y': 'Karbon MtCO2'}, inplace=True)

    # bar chart generator
    df = pd.DataFrame(pembangkit)
    # Membuat kolom baru 'grouped_sektor' untuk mengelompokkan nilai selain 'a', 'b', 'c'
    df['grouped_sumber'] = df['sumber'].apply(lambda x: x if x in ['Coal', 'Oil', 'Natural gas'] else 'Renewable Energy')
    df['persentase'] = ((df['Value'] / df['Value'].sum()) * 100).round(2)
    # Mengelompokkan dan menjumlahkan nilai berdasarkan 'grouped_sektor'
    grouped_df = df.groupby('grouped_sumber')['Value'].sum().reset_index()
    grouped_df['persentase'] = ((grouped_df['Value'] / grouped_df['Value'].sum()) * 100).round(2)
    grouped_df['persentase2'] = grouped_df['persentase'].astype(str)+'%'
    # dahboard metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sumber Listrik", value=grouped_df.iloc[-0]['persentase2'], delta= df.iloc[-0]["sumber"])
    with col2:
        st.metric("Sumber Listrik", value=grouped_df.iloc[-1]['persentase2'], delta= df.iloc[-2]["grouped_sumber"])
    # Membuat bar chart menggunakan Altair
    chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('grouped_sumber:N', axis=alt.Axis(title='Sumber')),
        y=alt.Y('Value', axis=alt.Axis(title='Produksi Listrik GWh')),
        tooltip=['Value:Q', 'persentase']
        ).properties(
        width=400,
        title='Sumber Pembangkit Listrik 2021')
    # Menampilkan grafik
    text = chart.mark_text(align='center', baseline='bottom', dy=-5).encode(
    text='persentase2:N')
    # Menggabungkan chart dan teks
    final_chart2 = (chart + text).configure_axisX(labelAngle=0)
    _, midcol, _= st.columns([1,2,1])
    with midcol:
        st.altair_chart(final_chart2)

    st.header("Emisi CO2 dari Pembangkit Listrik")
    st.write("Pembangkit listrik berbahan bakar fosil melepaskan karbon dioksida (CO2) ke atmosfer sebagai hasil dari proses pembakaran bahan bakar untuk menghasilkan listrik. Kebanyakan pembangkit listrik, terutama yang menggunakan bahan bakar fosil, menyumbang signifikan pada emisi CO2, yang merupakan salah satu penyebab utama perubahan iklim global.")
    st.write("Pemahaman dan penanganan emisi CO2 dari pembangkit listrik merupakan bagian dari upaya global untuk mengatasi perubahan iklim dan beralih ke sistem energi yang lebih berkelanjutan. Investasi dalam teknologi bersih dan sumber energi terbarukan menjadi semakin penting untuk mencapai target mitigasi perubahan iklim.")
    # hubungan regresi
    sumber_listrik = pd.read_csv(r"C:\Users\adics\my_project\electricity generation sources in Indonesia.csv")
    karbon_listrik = pd.read_csv(r"C:\Users\adics\my_project\emissions2 from power generation by source in Indonesia.csv")
    karbon_listrik.rename(columns={'emissions from power generation by source in Indonesia': 'sumber2'}, inplace=True)
    sumber_listrik.rename(columns={'electricity generation sources in Indonesia': 'sumber'}, inplace=True)
        
    # definisikkan ulang dataframe
    df = pd.DataFrame(sumber_listrik)
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    filtered_df = df[df['sumber'] == 'Coal']

    df = pd.DataFrame(karbon_listrik)
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    filtered_df2 = df[df['sumber2'] == 'Coal']
    
    # barchart emisi bahan bakar terhadap listrik
    filtered_df3 = df[df['Year'] == '2021']
    filtered_df3['persentase'] = ((filtered_df3['Value'] / filtered_df3['Value'].sum()) * 100).round(2)
    filtered_df3['persentase2'] = filtered_df3['persentase'].astype(str)+'%'
    # dahboard metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sumber Emisi", value=filtered_df3.iloc[-0]['persentase2'], delta= filtered_df3.iloc[-0]["sumber2"])
    with col2:
        st.metric("Sumber Emisi", value=filtered_df3.iloc[-2]['persentase2'], delta= filtered_df3.iloc[-2]["sumber2"])

    chart = alt.Chart(filtered_df3).mark_bar().encode(
            x=alt.X('sumber2:N', axis=alt.Axis(title='Sumber')),
            y=alt.Y('Value:Q', axis=alt.Axis(title='Emisi MtCO2')),
            tooltip=['Value:Q', 'persentase']
            ).properties(
            width=400,
            title='Emisi pembangkit listrik berdasarkan sumber 2021')
    
    # Menampilkan grafik
    text = chart.mark_text(align='center', baseline='bottom', dy=-5).encode(
    text='persentase2:N')
    # Menggabungkan chart dan teks
    final_chart2 = (chart + text).configure_axisX(labelAngle=0)
    _, midcol, _= st.columns([1,2,1])
    with midcol:
        st.altair_chart(final_chart2)

    st.header("Hubungan Penggunaan Batubara Terhadap Emisi CO2")
    st.write("Sebagai negara penghasil batubara terbesar di dunia, Indonesia sangat mengandalkan batubara sebagai sumber energi untuk menghasilkan listrik. Pembakaran batu bara menghasilkan emisi CO2 yang signifikan")
    #scater plot
    merged_df = pd.merge(filtered_df, filtered_df2, on='Year')
    merged_df.rename(columns={'Value_x': 'Listrik GWh', 'Value_y': 'Karbon MtCO2'}, inplace=True)
    _, midcol, _= st.columns([1,2,1])
    with midcol:
        scatter = alt.Chart(merged_df).mark_point().encode(
            x="Listrik GWh:Q",
            y=alt.Y("Karbon MtCO2:Q", axis=alt.Axis(title='Emisi MtCO2')),) 
        st.altair_chart(scatter, use_container_width=True)
with tab3:
    st.header("Solusi Mengurangi Dampak Lingkungan dari Produksi Listrik")
    st.write("Perubahan iklim dapat menyebabkan cuaca ekstrem, kenaikan permukaan laut, dan perubahan iklim lainnya dengan dampak serius pada lingkungan dan kehidupan manusia. Upaya dilakukan untuk mengurangi emisi CO2 dari pembangkit listrik melalui penerapan teknologi bersih, seperti pembangkit listrik tenaga angin, tenaga surya, dan teknologi penangkapan dan penyimpanan karbon (CCS). Beberapa solusi yang dapat dilakukan")
    st.markdown("__Beralih ke pembangkit energi terbarukan__")
    st.write("Semakin berkembangnya teknologi biaya untuk membangun pembangkit listrik terbarukan semakin terjangkau. Seluruh dunia sedang melakukan transisi energi besar-besaran dan diharapkan terus meningkat untuk menggantikan pembangkit listrik konvensional. Energi terbarukan dianggap sebagai alternatif yang lebih berkelanjutan dan ramah lingkungan dibandingkan dengan sumber energi konvensional berbasis bahan bakar fosil")
    # Menampilkan media
    from PIL import Image
    col1, col2, col3 = st.columns([1,1,1])
    with col1 :
        image= Image.open("hydroelectricity.jpg")
        st.image(
        image,
        caption="Hydro Generation")
    with col2:
        image2 = Image.open("wind.jpg")
        st.image(image2,
        caption="Wind Generation")
    with col3: 
        image3= Image.open("solar.jpg")
        st.image(
        image3,
        caption="Solar Generation")
    st.markdown("__Memanfaatkan limbah untuk pembangkit listrik__")
    st.write("Pembangkit listrik sampah, atau dikenal juga sebagai Pembangkit Listrik Tenaga Sampah (PLTSa), adalah instalasi yang mengonversi sampah padat menjadi energi listrik. Proses ini melibatkan penggunaan teknologi termal atau biologis untuk mengubah sampah menjadi listrik atau panas.")
    col1, col2, col3 = st.columns([1,1,1])
    with col1 :
        image4= Image.open("biofuel.jpg")
        st.image(
        image4,
        caption="Biofuel Generation")
    with col2:
        image5 = Image.open("biogas.jpg")
        st.image(image5,
        caption="Biogas Generation")
    st.markdown("__Mengurangi penggunaan listrik__")
    st.write("Pengurangan emisi CO2 dapat dimulai dari diri sendiri beberapa yang dapat dilakukan adalah menggunakan lampu hemat energi, mematikan alat-alat elektronik jika sedang tidak digunakan, menggunakan listrik sesuai kebutuhan seperti menggunakan AC hanya ketika siang hari.")
    col1, col2, col3 = st.columns([1,1,1])
    with col1 :
        image6= Image.open("lampu.jpg")
        st.image(
        image6,
        caption="Lampu Hemat Energi")
    with col2:
        image7 = Image.open("cabut.jpeg")
        st.image(image7,
        caption="Mematikan Listrik")
    with col3: 
        image8= Image.open("ac.jpeg")
        st.image(
        image8,
        caption="Menghemat Energi")


# membuat kalkulator
import matplotlib.pyplot as plt

def main():
    st.sidebar.header("Kalkulator Emisi Batubara pada Produksi Listrik")

    df = pd.DataFrame(merged_df)

    # Menampilkan data
    st.sidebar.subheader("Data:")
    st.sidebar.write(df.tail())

    # Menghitung koefisien regresi tanpa scikit-learn
    slope, intercept = hitung_regresi(df['Listrik GWh'], df['Karbon MtCO2'])

    # Menampilkan koefisien regresi
    st.sidebar.subheader("Koefisien Regresi:")
    st.sidebar.write(f"Slope (Koefisien Regresi): {slope:.3f}")
    st.sidebar.write(f"Intercept (Intersepsi): {intercept:.2f}")

    # Input untuk prediksi
    st.sidebar.subheader("Prediksi:")
    input_listrik = st.sidebar.number_input("Masukkan produksi listrik (GWh):", min_value=0, max_value=99999999)

    # Melakukan prediksi tanpa scikit-learn
    predicted_karbon = prediksi_regresi(input_listrik, slope, intercept)

    # Menampilkan hasil prediksi
    st.sidebar.write(f"Prediksi Karbon untuk Listrik {input_listrik} GWh: {predicted_karbon:.2f} MtCO2")


def hitung_regresi(x, y):
    n = len(x)
    mean_x, mean_y = np.mean(x), np.mean(y)
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sum((x - mean_x) ** 2)
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    return slope, intercept

def prediksi_regresi(x, slope, intercept):
    return slope * x + intercept

if __name__ == "__main__":
    main()
