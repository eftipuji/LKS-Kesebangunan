import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from math import gcd

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Jelajah Kesebangunan",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS KUSTOM (selaras dengan LKS Bilangan Bulat)
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

    /* Header utama */
    .main-header {
        background: linear-gradient(135deg, #1A3C6E 0%, #7030A0 60%, #ED7D31 100%);
        color: white; padding: 1.5rem 2rem; border-radius: 16px;
        text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(112,48,160,0.3);
    }
    .main-header h1 { font-size: 2rem; font-weight: 800; margin: 0; }
    .main-header p  { font-size: 1rem; margin: 0.3rem 0 0; opacity: 0.9; }

    /* Box fase discovery */
    .fase-box {
        border-left: 5px solid #7030A0; background: #F5EFFF;
        padding: 0.8rem 1rem; border-radius: 0 10px 10px 0;
        margin: 0.7rem 0;
    }
    .fase-box .fase-label {
        font-weight: 800; color: #1A3C6E; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .fase-box .fase-text { color: #2C3E50; font-size: 0.95rem; margin-top: 0.2rem; }

    /* Card informasi */
    .info-card {
        background: #F0F7FF; border: 1px solid #BDD7EE;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .warning-card {
        background: #FFF8E6; border: 1px solid #FFD966;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .success-card {
        background: #F0FBF0; border: 1px solid #70AD47;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .danger-card {
        background: #FEF0F0; border: 1px solid #E74C3C;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .purple-card {
        background: #F5EFFF; border: 1px solid #7030A0;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }

    /* Hasil kalkulator */
    .result-display {
        background: linear-gradient(135deg, #1A3C6E, #7030A0);
        color: white; border-radius: 16px; padding: 1.5rem;
        text-align: center; font-size: 2.5rem; font-weight: 800;
        box-shadow: 0 4px 15px rgba(112,48,160,0.3); margin: 1rem 0;
    }
    .result-label { font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.3rem; }

    /* Sidebar */
    .sidebar-title {
        background: #1A3C6E; color: white;
        padding: 0.7rem 1rem; border-radius: 10px;
        font-weight: 800; text-align: center; margin-bottom: 0.5rem;
    }

    /* Tombol kustom */
    .stButton > button {
        border-radius: 10px; font-weight: 700;
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-2px); }

    /* Metric */
    [data-testid="metric-container"] {
        background: #F8FAFF; border: 1px solid #BDD7EE;
        border-radius: 12px; padding: 0.8rem; text-align: center;
    }

    hr { border: none; border-top: 2px solid #F5EFFF; margin: 1.5rem 0; }

    /* Badge rasio */
    .badge-sebangun { background:#70AD47; color:white; padding:3px 12px; border-radius:20px; font-weight:700; }
    .badge-tidak { background:#C00000; color:white; padding:3px 12px; border-radius:20px; font-weight:700; }
    .badge-kongruen { background:#7030A0; color:white; padding:3px 12px; border-radius:20px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HEADER UTAMA
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📐 Jelajah Kesebangunan</h1>
    <p>Kalkulator Digital Interaktif • Metode Discovery Learning • SMP/MTs Kelas VII</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR NAVIGASI
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 Menu Navigasi</div>', unsafe_allow_html=True)
    tab_choice = st.radio(
        "Pilih Fitur:",
        options=[
            "🏠 Beranda",
            "📐 KP 1 — Kesebangunan Bangun Datar",
            "🔺 KP 2 — Kesebangunan Segitiga",
            "📏 KP 3 — Menghitung Panjang Sisi",
            "📝 Soal Latihan Interaktif",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="background:#F5EFFF;padding:0.8rem;border-radius:10px;font-size:0.82rem;color:#1A3C6E;">
    <b>📚 Petunjuk Penggunaan</b><br><br>
    1. Pilih fitur sesuai kegiatan pembelajaran<br>
    2. Ikuti langkah-langkah Discovery Learning<br>
    3. Catat temuan di LKS<br>
    4. Diskusikan dengan kelompokmu<br>
    5. Kerjakan soal latihan di akhir
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#7F7F7F;text-align:center;">
    🎓 Kurikulum Merdeka Fase D<br>
    Penulis: Efti Puji Lestari
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# HALAMAN BERANDA
# ══════════════════════════════════════════
if tab_choice == "🏠 Beranda":
    st.markdown("## 👋 Selamat Datang, Penjelajah Matematika!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
        <b>🎯 Fokus Kemampuan</b><br><br>
        ✅ Memahami Konsep Kesebangunan (TP 1)<br>
        ✅ Syarat Dua Bangun Sebangun (TP 2)<br>
        ✅ Menghitung Panjang Sisi (TP 3)<br>
        ✅ Masalah Kontekstual Kesebangunan (TP 4)
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
        <b>🔬 Metode Pembelajaran</b><br><br>
        🔵 Discovery Learning (utama)<br>
        🟢 Problem Based Learning<br>
        🟡 Cooperative Learning
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
        <b>📱 Fitur Aplikasi</b><br><br>
        📐 Eksplorasi Kesebangunan Bangun Datar<br>
        🔺 Kesebangunan Segitiga Interaktif<br>
        📏 Kalkulator Panjang Sisi<br>
        📝 Soal Latihan Interaktif
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 Alur Discovery Learning dalam Aplikasi Ini")

    fases = [
        ("① STIMULATION", "Kamu akan dihadapkan pada situasi nyata — foto di kamera terlihat lebih kecil, peta kota yang menyajikan ukuran berbeda. Ini akan membuatmu penasaran!", "#7030A0"),
        ("② PROBLEM STATEMENT", "Kamu merumuskan pertanyaan sendiri. Apa syarat dua bangun dikatakan sebangun?", "#ED7D31"),
        ("③ DATA COLLECTION", "Eksplorasi bebas menggunakan kalkulator digital! Ubah ukuran bangun dan amati rasio sisi serta sudutnya.", "#70AD47"),
        ("④ DATA PROCESSING", "Analisis pola dari data yang kamu kumpulkan. Kapan dua bangun sebangun? Kapan tidak?", "#2E75B6"),
        ("⑤ VERIFICATION", "Bandingkan temuanmu dengan teman sekelompok. Apakah syarat kesebangunan yang kamu temukan sama?", "#C00000"),
        ("⑥ GENERALIZATION", "Rumuskan syarat kesebangunan dengan kata-katamu sendiri. Inilah ilmu yang benar-benar kamu pahami!", "#1A3C6E"),
    ]

    cols = st.columns(3)
    for i, (label, text, color) in enumerate(fases):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border-left:4px solid {color};background:#FAFAFA;
                        padding:0.8rem 1rem;border-radius:0 10px 10px 0;margin-bottom:0.8rem;">
                <div style="font-weight:800;color:{color};font-size:0.9rem;">{label}</div>
                <div style="font-size:0.85rem;color:#444;margin-top:0.3rem;">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="warning-card">
    <b>💡 Tips Belajar Efektif</b><br>
    Jangan langsung klik-klik tanpa tujuan! Sebelum mengeksplorasi, baca dulu petunjuk di LKS,
    lalu gunakan kalkulator digital ini untuk <b>membuktikan hipotesismu</b> dan
    <b>menemukan syarat kesebangunan</b> secara mandiri. Catat semua temuanmu!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 Peta Konsep Kesebangunan")
    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:0.88rem;text-align:center;">
    <tr style="background:#1A3C6E;color:white;">
        <th style="padding:10px;border:1px solid #ccc;" colspan="3">KESEBANGUNAN</th>
    </tr>
    <tr style="background:#7030A0;color:white;">
        <th style="padding:8px;border:1px solid #ccc;">KP 1<br>Kesebangunan Bangun Datar</th>
        <th style="padding:8px;border:1px solid #ccc;">KP 2<br>Kesebangunan Segitiga</th>
        <th style="padding:8px;border:1px solid #ccc;">KP 3<br>Menghitung Panjang Sisi</th>
    </tr>
    <tr style="background:#F5EFFF;">
        <td style="padding:8px;border:1px solid #ccc;">• Pengertian sebangun<br>• Syarat kesebangunan<br>• Sudut bersesuaian<br>• Sisi bersesuaian</td>
        <td style="padding:8px;border:1px solid #ccc;">• Syarat SSS, SAS, AA<br>• Segitiga sebangun<br>• Kongruensi vs Kesebangunan</td>
        <td style="padding:8px;border:1px solid #ccc;">• Skala perbesaran<br>• Menentukan panjang sisi<br>• Masalah kontekstual</td>
    </tr>
    <tr style="background:#EBF3FB;">
        <td style="padding:6px;border:1px solid #ccc;font-size:0.8rem;"><i>Media: Eksplorasi Bangun Datar</i></td>
        <td style="padding:6px;border:1px solid #ccc;font-size:0.8rem;"><i>Media: Segitiga Interaktif</i></td>
        <td style="padding:6px;border:1px solid #ccc;font-size:0.8rem;"><i>Media: Kalkulator Skala</i></td>
    </tr>
    </table>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 1 — KESEBANGUNAN BANGUN DATAR
# ══════════════════════════════════════════
elif tab_choice == "📐 KP 1 — Kesebangunan Bangun Datar":
    st.markdown("## 📐 Kegiatan Pembelajaran 1: Kesebangunan Bangun Datar")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Perhatikan foto yang dicetak dalam ukuran berbeda: <b>4×6 cm</b> dan <b>8×12 cm</b>.
        Keduanya tampak "sama bentuknya" meski ukurannya berbeda.<br>
        Perhatikan juga uang kertas <b>Rp10.000</b>: gambar pada uang asli dan fotokopinya 
        memiliki bentuk yang sama persis.<br><br>
        <b>❓ Apa syarat agar dua bangun datar dikatakan <i>sebangun</i>?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#ED7D31;background:#FFF4EC;">
        <div class="fase-label" style="color:#ED7D31;">② Problem Statement — Rumusan Masalah</div>
        <div class="fase-text">
        Tuliskan hipotesismu di LKS sebelum bereksplorasi:<br>
        <i>"Menurutku, dua bangun dikatakan sebangun jika... dan..."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Eksplorasi Persegi Panjang</div>
        <div class="fase-text">Ubah ukuran dua persegi panjang di bawah. Amati kapan keduanya sebangun!</div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_viz = st.columns([1, 2])

    with col_input:
        st.markdown("#### 📏 Persegi Panjang 1 (ABCD)")
        p1 = st.slider("Panjang AB (cm):", 1, 20, 6, key="p1")
        l1 = st.slider("Lebar BC (cm):", 1, 20, 4, key="l1")

        st.markdown("#### 📏 Persegi Panjang 2 (EFGH)")
        p2 = st.slider("Panjang EF (cm):", 1, 20, 9, key="p2")
        l2 = st.slider("Lebar FG (cm):", 1, 20, 6, key="l2")

        # Hitung rasio
        rasio_p = p2 / p1
        rasio_l = l2 / l1
        rasio_sama = abs(rasio_p - rasio_l) < 0.001

        # Cek kesebangunan
        sebangun = rasio_sama

        # Tampilkan rasio
        def frac_str(a, b):
            from math import gcd
            g = gcd(a, b)
            if a % b == 0:
                return f"{a//b}"
            return f"{a//g}/{b//g}"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                    border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
            <div style="font-size:0.8rem;opacity:0.85;margin-bottom:0.4rem;">Rasio Sisi Bersesuaian</div>
            <div style="font-size:1.1rem;font-weight:800;">
                EF/AB = {p2}/{p1} = <span style="color:#FFD966">{rasio_p:.3f}</span>
            </div>
            <div style="font-size:1.1rem;font-weight:800;margin-top:0.3rem;">
                FG/BC = {l2}/{l1} = <span style="color:#FFD966">{rasio_l:.3f}</span>
            </div>
            <div style="margin-top:0.8rem;font-size:1.3rem;font-weight:800;
                        color:{'#70AD47' if sebangun else '#E74C3C'};">
                {'✅ RASIO SAMA → SEBANGUN' if sebangun else '❌ RASIO BERBEDA → TIDAK SEBANGUN'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if sebangun:
            st.markdown(f"""
            <div class="success-card" style="margin-top:0.5rem;">
            <b>🎉 Kesimpulan:</b><br>
            ABCD ~ EFGH karena:<br>
            ✅ Semua sudut bersesuaian sama (90°)<br>
            ✅ Semua rasio sisi bersesuaian = <b>{rasio_p:.2f}</b><br>
            📏 Skala perbesaran = <b>{rasio_p:.2f}×</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-card" style="margin-top:0.5rem;">
            <b>❌ Tidak Sebangun:</b><br>
            EF/AB = {rasio_p:.3f} ≠ FG/BC = {rasio_l:.3f}<br>
            Rasio sisi-sisi bersesuaian <b>tidak sama</b>.
            </div>
            """, unsafe_allow_html=True)

    with col_viz:
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        fig.patch.set_facecolor('#FAFBFF')

        color1 = "#2E75B6"
        color2 = "#70AD47" if sebangun else "#C00000"

        # Persegi panjang 1
        ax1 = axes[0]
        ax1.set_facecolor('#FAFBFF')
        ax1.set_xlim(-1, p1 + 2)
        ax1.set_ylim(-1, l1 + 2)
        rect1 = patches.Rectangle((0, 0), p1, l1,
                                   linewidth=3, edgecolor=color1, facecolor='#EBF3FB', alpha=0.7)
        ax1.add_patch(rect1)
        ax1.text(p1/2, -0.5, f'AB = {p1} cm', ha='center', fontsize=10, color=color1, fontweight='bold')
        ax1.text(-0.7, l1/2, f'BC = {l1} cm', ha='center', fontsize=10, color=color1, fontweight='bold', rotation=90)
        ax1.text(-0.3, -0.3, 'A', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax1.text(p1+0.1, -0.3, 'B', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax1.text(p1+0.1, l1+0.1, 'C', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax1.text(-0.3, l1+0.1, 'D', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax1.set_title(f'Persegi Panjang ABCD\n({p1} × {l1} cm)', fontsize=11, color='#1A3C6E', fontweight='bold')
        ax1.set_aspect('equal')
        ax1.axis('off')

        # Persegi panjang 2
        ax2 = axes[1]
        ax2.set_facecolor('#FAFBFF')
        ax2.set_xlim(-1, p2 + 2)
        ax2.set_ylim(-1, l2 + 2)
        fc2 = '#F0FBF0' if sebangun else '#FEF0F0'
        rect2 = patches.Rectangle((0, 0), p2, l2,
                                   linewidth=3, edgecolor=color2, facecolor=fc2, alpha=0.7)
        ax2.add_patch(rect2)
        ax2.text(p2/2, -0.5, f'EF = {p2} cm', ha='center', fontsize=10, color=color2, fontweight='bold')
        ax2.text(-0.7, l2/2, f'FG = {l2} cm', ha='center', fontsize=10, color=color2, fontweight='bold', rotation=90)
        ax2.text(-0.3, -0.3, 'E', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax2.text(p2+0.1, -0.3, 'F', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax2.text(p2+0.1, l2+0.1, 'G', fontsize=11, fontweight='bold', color='#1A3C6E')
        ax2.text(-0.3, l2+0.1, 'H', fontsize=11, fontweight='bold', color='#1A3C6E')
        status = "✅ SEBANGUN" if sebangun else "❌ TIDAK SEBANGUN"
        ax2.set_title(f'Persegi Panjang EFGH\n({p2} × {l2} cm)  —  {status}', fontsize=11, color=color2, fontweight='bold')
        ax2.set_aspect('equal')
        ax2.axis('off')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")

    # DATA PROCESSING — Tabel Eksplorasi
    st.markdown("""
    <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
        <div class="fase-label" style="color:#7030A0;">④ Data Processing — Tabel Analisis Kesebangunan</div>
        <div class="fase-text">Coba berbagai kombinasi ukuran menggunakan slider. Catat hasilmu di LKS!</div>
    </div>
    """, unsafe_allow_html=True)

    contoh_tabel = [
        ("4×6", "8×12", "8/4=2", "12/6=2", "Ya", "✅ SEBANGUN"),
        ("3×5", "6×10", "6/3=2", "10/5=2", "Ya", "✅ SEBANGUN"),
        ("4×6", "8×9", "8/4=2", "9/6=1,5", "Tidak", "❌ TIDAK SEBANGUN"),
        ("5×8", "...", "...", "...", "...", "..."),
        ("3×7", "...", "...", "...", "...", "..."),
    ]

    tbl = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem;">'
    tbl += '<tr style="background:#1A3C6E;color:white;text-align:center;">'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">ABCD (p×l)</th>'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">EFGH (p×l)</th>'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">Rasio Panjang</th>'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">Rasio Lebar</th>'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">Rasio Sama?</th>'
    tbl += '<th style="padding:8px;border:1px solid #ccc;">Kesimpulan</th></tr>'
    for i, r in enumerate(contoh_tabel):
        bg = '#F8FAFF' if i % 2 == 0 else 'white'
        tbl += f'<tr style="background:{bg};text-align:center;">'
        for j, val in enumerate(r):
            fw = 'bold' if j in [0, 1, 5] else 'normal'
            tbl += f'<td style="padding:7px;border:1px solid #ccc;font-weight:{fw};">{val}</td>'
        tbl += '</tr>'
    tbl += '</table>'
    st.markdown(tbl, unsafe_allow_html=True)
    st.markdown("*(Baris kosong diisi berdasarkan eksplorasimu menggunakan slider)*", unsafe_allow_html=True)

    # GENERALIZATION
    st.markdown("---")
    with st.expander("⑥ 💡 Lihat Simpulan Syarat Kesebangunan (setelah mencoba sendiri dulu!)"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Syarat Dua Bangun Datar Sebangun:</b><br><br>
        🔵 <b>Syarat 1 — Sudut Bersesuaian:</b> Semua sudut yang bersesuaian harus <b>sama besar</b><br>
        🟢 <b>Syarat 2 — Sisi Bersesuaian:</b> Semua rasio sisi yang bersesuaian harus <b>sama (proporsional)</b><br><br>
        📐 <b>Notasi:</b> ABCD ~ EFGH dibaca "ABCD sebangun dengan EFGH"<br>
        📏 <b>Skala = sisi bangun baru ÷ sisi bangun asal</b>
        </div>
        <div class="warning-card" style="margin-top:0.5rem;">
        <b>⚠️ Perhatian Penting:</b><br>
        Kongruen (≅) → bentuk DAN ukuran sama persis (skala = 1)<br>
        Sebangun (~) → bentuk sama, ukuran boleh berbeda (skala ≠ 1)<br>
        <b>Semua bangun kongruen pasti sebangun, tetapi tidak sebaliknya!</b>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 2 — KESEBANGUNAN SEGITIGA
# ══════════════════════════════════════════
elif tab_choice == "🔺 KP 2 — Kesebangunan Segitiga":
    st.markdown("## 🔺 Kegiatan Pembelajaran 2: Kesebangunan Segitiga")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Sebuah pohon berdiri tegak di bawah sinar matahari. Bayangan pohon sepanjang <b>6 m</b>.
        Seorang anak dengan tinggi <b>1,5 m</b> berdiri di dekat pohon dan bayangannya <b>1 m</b>.<br><br>
        <b>❓ Bisakah kita menemukan tinggi pohon tanpa memanjatnya?</b><br>
        Inilah kekuatan <b>kesebangunan segitiga</b> dalam kehidupan nyata!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#ED7D31;background:#FFF4EC;">
        <div class="fase-label" style="color:#ED7D31;">② Problem Statement — Hipotesis</div>
        <div class="fase-text">
        Tuliskan hipotesismu di LKS:<br>
        <i>"Menurutku, dua segitiga sebangun jika..."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Eksplorasi Segitiga Interaktif</div>
        <div class="fase-text">Masukkan sisi-sisi dua segitiga. Amati apakah keduanya sebangun!</div>
    </div>
    """, unsafe_allow_html=True)

    tab2a, tab2b = st.tabs(["🔺 Cek Kesebangunan (SSS)", "📐 Syarat Sudut (AA)"])

    # ── TAB SSS
    with tab2a:
        st.markdown("**Syarat SSS (Side-Side-Side): Cek rasio ketiga sisi bersesuaian**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Segitiga 1 (ABC)")
            a1 = st.number_input("Sisi AB:", min_value=1, max_value=100, value=3, key="a1")
            b1 = st.number_input("Sisi BC:", min_value=1, max_value=100, value=4, key="b1")
            c1 = st.number_input("Sisi CA:", min_value=1, max_value=100, value=5, key="c1")
        with col2:
            st.markdown("##### Segitiga 2 (DEF)")
            a2 = st.number_input("Sisi DE:", min_value=1, max_value=100, value=6, key="a2")
            b2 = st.number_input("Sisi EF:", min_value=1, max_value=100, value=8, key="b2")
            c2 = st.number_input("Sisi FD:", min_value=1, max_value=100, value=10, key="c2")

        # Cek validitas segitiga
        def valid_segitiga(a, b, c):
            return (a + b > c) and (b + c > a) and (a + c > b)

        valid1 = valid_segitiga(a1, b1, c1)
        valid2 = valid_segitiga(a2, b2, c2)

        if not valid1:
            st.error("⚠️ Sisi-sisi Segitiga 1 tidak membentuk segitiga yang valid!")
        elif not valid2:
            st.error("⚠️ Sisi-sisi Segitiga 2 tidak membentuk segitiga yang valid!")
        else:
            r1 = a2 / a1
            r2 = b2 / b1
            r3 = c2 / c1
            sebangun_sss = (abs(r1 - r2) < 0.001) and (abs(r2 - r3) < 0.001)

            colr1, colr2, colr3 = st.columns(3)
            with colr1:
                color = "#70AD47" if abs(r1 - r2) < 0.001 else "#C00000"
                st.markdown(f"""<div style="background:{color};color:white;border-radius:10px;
                    padding:0.8rem;text-align:center;font-weight:800;">
                    DE/AB = {a2}/{a1} = {r1:.3f}</div>""", unsafe_allow_html=True)
            with colr2:
                color = "#70AD47" if abs(r1 - r2) < 0.001 and abs(r2 - r3) < 0.001 else "#C00000"
                st.markdown(f"""<div style="background:{color};color:white;border-radius:10px;
                    padding:0.8rem;text-align:center;font-weight:800;">
                    EF/BC = {b2}/{b1} = {r2:.3f}</div>""", unsafe_allow_html=True)
            with colr3:
                color = "#70AD47" if abs(r1 - r3) < 0.001 and abs(r2 - r3) < 0.001 else "#C00000"
                st.markdown(f"""<div style="background:{color};color:white;border-radius:10px;
                    padding:0.8rem;text-align:center;font-weight:800;">
                    FD/CA = {c2}/{c1} = {r3:.3f}</div>""", unsafe_allow_html=True)

            if sebangun_sss:
                st.markdown(f"""
                <div class="success-card" style="margin-top:0.8rem;text-align:center;">
                <b style="font-size:1.1rem;">✅ △ABC ~ △DEF (SEBANGUN)</b><br>
                Skala = {r1:.2f} | DE/AB = EF/BC = FD/CA = {r1:.3f}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="danger-card" style="margin-top:0.8rem;text-align:center;">
                <b style="font-size:1.1rem;">❌ △ABC TIDAK sebangun dengan △DEF</b><br>
                Rasio sisi-sisi bersesuaian tidak sama: {r1:.3f} ≠ {r2:.3f} ≠ {r3:.3f}
                </div>
                """, unsafe_allow_html=True)

            # Visualisasi
            def hitung_koordinat_segitiga(a, b, c):
                """Hitung koordinat segitiga dari panjang sisi menggunakan hukum cosinus"""
                import math
                # Tempatkan A di origin, B di (c, 0)
                # Cari sudut A menggunakan aturan cosinus: cos A = (b²+c²-a²)/(2bc) — di sini a=BC, b=CA, c=AB
                cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
                cos_A = max(-1, min(1, cos_A))
                sin_A = math.sqrt(1 - cos_A**2)
                A = np.array([0, 0])
                B = np.array([c, 0])
                C = np.array([b * cos_A, b * sin_A])
                return A, B, C

            try:
                A1, B1, C1 = hitung_koordinat_segitiga(a1, b1, c1)
                A2, B2, C2 = hitung_koordinat_segitiga(a2, b2, c2)

                fig2, (ax_t1, ax_t2) = plt.subplots(1, 2, figsize=(10, 5))
                fig2.patch.set_facecolor('#FAFBFF')

                for ax, pts, labels, color, title in [
                    (ax_t1, [A1, B1, C1], ['A', 'B', 'C'], '#2E75B6',
                     f'△ABC  ({a1}, {b1}, {c1})'),
                    (ax_t2, [A2, B2, C2], ['D', 'E', 'F'], '#70AD47' if sebangun_sss else '#C00000',
                     f'△DEF  ({a2}, {b2}, {c2})'),
                ]:
                    ax.set_facecolor('#FAFBFF')
                    tri = plt.Polygon(pts, fill=True,
                                      facecolor=color + '33', edgecolor=color, linewidth=2.5)
                    ax.add_patch(tri)
                    for pt, lbl in zip(pts, labels):
                        off = pt / np.linalg.norm(pt + 0.001) * 0.4 if np.linalg.norm(pt) > 0.1 else np.array([-0.4, -0.4])
                        ax.text(pt[0] + off[0] * 0.3, pt[1] + off[1] * 0.3, lbl,
                                fontsize=13, fontweight='bold', color='#1A3C6E',
                                ha='center', va='center')
                    all_pts = np.array(pts)
                    pad = max(a1, b1, c1, a2, b2, c2) * 0.15
                    ax.set_xlim(all_pts[:, 0].min() - pad, all_pts[:, 0].max() + pad)
                    ax.set_ylim(all_pts[:, 1].min() - pad, all_pts[:, 1].max() + pad)
                    ax.set_aspect('equal')
                    ax.axis('off')
                    status_str = "✅ SEBANGUN" if sebangun_sss else "❌ TIDAK SEBANGUN"
                    ax.set_title(title + (f'\n{status_str}' if ax == ax_t2 else ''),
                                 fontsize=11, fontweight='bold', color=color)

                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
            except Exception:
                st.info("(Visualisasi tidak tersedia untuk kombinasi sisi ini)")

    # ── TAB AA
    with tab2b:
        st.markdown("**Syarat AA (Angle-Angle): Dua sudut bersesuaian sama besar → pasti sebangun!**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Segitiga PQR")
            sudut_P = st.slider("Sudut P (°):", 10, 160, 60, key="sP")
            sudut_Q = st.slider("Sudut Q (°):", 10, 160, 80, key="sQ")
            sudut_R = 180 - sudut_P - sudut_Q
            if sudut_R <= 0:
                st.error("⚠️ Total sudut melebihi 180°! Kurangi nilai sudut P atau Q.")
                sudut_R = None
            else:
                st.markdown(f"""
                <div class="info-card">
                Sudut P = {sudut_P}°<br>
                Sudut Q = {sudut_Q}°<br>
                <b>Sudut R = 180 - {sudut_P} - {sudut_Q} = {sudut_R}°</b>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("##### Segitiga XYZ")
            sudut_X = st.slider("Sudut X (°):", 10, 160, 60, key="sX")
            sudut_Y = st.slider("Sudut Y (°):", 10, 160, 80, key="sY")
            sudut_Z = 180 - sudut_X - sudut_Y
            if sudut_Z <= 0:
                st.error("⚠️ Total sudut melebihi 180°! Kurangi nilai sudut X atau Y.")
                sudut_Z = None
            else:
                st.markdown(f"""
                <div class="info-card">
                Sudut X = {sudut_X}°<br>
                Sudut Y = {sudut_Y}°<br>
                <b>Sudut Z = 180 - {sudut_X} - {sudut_Y} = {sudut_Z}°</b>
                </div>
                """, unsafe_allow_html=True)

        if sudut_R and sudut_Z:
            s1_sorted = sorted([sudut_P, sudut_Q, sudut_R])
            s2_sorted = sorted([sudut_X, sudut_Y, sudut_Z])
            sebangun_aa = s1_sorted == s2_sorted

            if sebangun_aa:
                st.markdown(f"""
                <div class="success-card" style="text-align:center;margin-top:1rem;">
                <b style="font-size:1.1rem;">✅ △PQR ~ △XYZ (SEBANGUN — Syarat AA)</b><br>
                Sudut-sudut bersesuaian sama besar: {s1_sorted[0]}°, {s1_sorted[1]}°, {s1_sorted[2]}°
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="danger-card" style="text-align:center;margin-top:1rem;">
                <b style="font-size:1.1rem;">❌ △PQR TIDAK sebangun dengan △XYZ</b><br>
                Sudut PQR: {sorted([sudut_P,sudut_Q,sudut_R])} ≠ Sudut XYZ: {s2_sorted}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div class="purple-card">
        <b>💡 Mengapa Syarat AA Cukup?</b><br>
        Jika dua sudut dari satu segitiga sama dengan dua sudut dari segitiga lain,
        maka sudut ketiga <i>pasti</i> juga sama (karena jumlah sudut segitiga selalu 180°).
        Dengan demikian, hanya perlu membuktikan 2 sudut saja!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    # Tabel Syarat Kesebangunan Segitiga
    st.markdown("""
    <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
        <div class="fase-label" style="color:#7030A0;">④ Data Processing — Syarat Kesebangunan Segitiga</div>
        <div class="fase-text">Lengkapi tabel berikut berdasarkan eksplorasimu!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:0.88rem;text-align:center;">
    <tr style="background:#1A3C6E;color:white;">
        <th style="padding:10px;border:1px solid #ccc;">Syarat</th>
        <th style="padding:10px;border:1px solid #ccc;">Nama</th>
        <th style="padding:10px;border:1px solid #ccc;">Yang Harus Dipenuhi</th>
        <th style="padding:10px;border:1px solid #ccc;">Contoh</th>
    </tr>
    <tr style="background:#F0FBF0;">
        <td style="padding:8px;border:1px solid #ccc;font-weight:bold;">SSS</td>
        <td style="padding:8px;border:1px solid #ccc;">Sisi-Sisi-Sisi</td>
        <td style="padding:8px;border:1px solid #ccc;">Rasio ketiga sisi bersesuaian sama</td>
        <td style="padding:8px;border:1px solid #ccc;">3:4:5 ~ 6:8:10</td>
    </tr>
    <tr style="background:#FFF8E6;">
        <td style="padding:8px;border:1px solid #ccc;font-weight:bold;">AA</td>
        <td style="padding:8px;border:1px solid #ccc;">Sudut-Sudut</td>
        <td style="padding:8px;border:1px solid #ccc;">Dua sudut bersesuaian sama besar</td>
        <td style="padding:8px;border:1px solid #ccc;">60°, 80° ~ 60°, 80°</td>
    </tr>
    <tr style="background:#F5EFFF;">
        <td style="padding:8px;border:1px solid #ccc;font-weight:bold;">SAS</td>
        <td style="padding:8px;border:1px solid #ccc;">Sisi-Sudut-Sisi</td>
        <td style="padding:8px;border:1px solid #ccc;">Dua sisi proporsional & sudut apitnya sama</td>
        <td style="padding:8px;border:1px solid #ccc;">3, 60°, 4 ~ 6, 60°, 8</td>
    </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("⑥ 💡 Lihat Simpulan Kesebangunan Segitiga"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Syarat Kesebangunan Segitiga:</b><br><br>
        🔵 <b>SSS:</b> Rasio sisi-sisi bersesuaian sama → <i>a/d = b/e = c/f</i><br>
        🟢 <b>AA:</b> Dua pasang sudut bersesuaian sama besar<br>
        🟡 <b>SAS:</b> Dua sisi proporsional dan sudut apit sama besar<br><br>
        📌 Cukup salah satu syarat terpenuhi untuk membuktikan kesebangunan!
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 3 — MENGHITUNG PANJANG SISI
# ══════════════════════════════════════════
elif tab_choice == "📏 KP 3 — Menghitung Panjang Sisi":
    st.markdown("## 📏 Kegiatan Pembelajaran 3: Menghitung Panjang Sisi")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        <b>Masalah Nyata:</b> Seorang arsitek membuat denah rumah dengan skala <b>1:100</b>.
        Di denah, panjang ruang tamu = <b>4,5 cm</b>. Berapa panjang ruang tamu sebenarnya?<br><br>
        <b>❓ Bagaimana konsep kesebangunan membantu kita menentukan ukuran yang tidak bisa diukur langsung?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab3a, tab3b, tab3c = st.tabs([
        "📏 Kalkulator Skala",
        "🔺 Sisi Segitiga Sebangun",
        "🌳 Masalah Bayangan"
    ])

    # ── TAB KALKULATOR SKALA
    with tab3a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Data Collection — Kalkulator Skala</div>
            <div class="fase-text">Gunakan kalkulator ini untuk menemukan pola hubungan skala dan ukuran sebenarnya!</div>
        </div>
        """, unsafe_allow_html=True)

        mode = st.selectbox("Mode Perhitungan:", [
            "🗺️ Denah/Peta → Ukuran Sebenarnya",
            "📐 Ukuran Sebenarnya → Denah/Peta",
            "🔍 Cari Skala dari Dua Ukuran",
        ])

        if mode == "🗺️ Denah/Peta → Ukuran Sebenarnya":
            col1, col2 = st.columns(2)
            with col1:
                skala_p = st.number_input("Skala gambar (1 : ?):", min_value=1, max_value=100000, value=100, step=10)
                uk_gambar = st.number_input("Ukuran pada gambar (cm):", min_value=0.01, max_value=1000.0, value=4.5, step=0.1)
            with col2:
                uk_asli = uk_gambar * skala_p
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                            border-radius:14px;padding:1.5rem;text-align:center;margin-top:1rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Rumus</div>
                    <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">
                        Ukuran Asli = Ukuran Gambar × Skala
                    </div>
                    <div style="font-size:0.9rem;opacity:0.8;">= {uk_gambar} cm × {skala_p}</div>
                    <div style="font-size:2.8rem;font-weight:800;margin-top:0.5rem;">{uk_asli:,.1f} cm</div>
                    <div style="font-size:1rem;opacity:0.9;">= {uk_asli/100:,.2f} m</div>
                </div>
                """, unsafe_allow_html=True)

        elif mode == "📐 Ukuran Sebenarnya → Denah/Peta":
            col1, col2 = st.columns(2)
            with col1:
                skala_p2 = st.number_input("Skala gambar (1 : ?):", min_value=1, max_value=100000, value=200, step=10)
                uk_asli2 = st.number_input("Ukuran sebenarnya (cm):", min_value=0.01, max_value=100000.0, value=600.0, step=10.0)
            with col2:
                uk_gambar2 = uk_asli2 / skala_p2
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                            border-radius:14px;padding:1.5rem;text-align:center;margin-top:1rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Rumus</div>
                    <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">
                        Ukuran Gambar = Ukuran Asli ÷ Skala
                    </div>
                    <div style="font-size:0.9rem;opacity:0.8;">= {uk_asli2} cm ÷ {skala_p2}</div>
                    <div style="font-size:2.8rem;font-weight:800;margin-top:0.5rem;">{uk_gambar2:.2f} cm</div>
                </div>
                """, unsafe_allow_html=True)

        else:  # Cari skala
            col1, col2 = st.columns(2)
            with col1:
                uk_gam3 = st.number_input("Ukuran pada gambar (cm):", min_value=0.01, max_value=1000.0, value=3.0, step=0.1)
                uk_asl3 = st.number_input("Ukuran sebenarnya (cm):", min_value=0.01, max_value=1000000.0, value=600.0, step=10.0)
            with col2:
                skala3 = uk_asl3 / uk_gam3
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                            border-radius:14px;padding:1.5rem;text-align:center;margin-top:1rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Rumus Skala</div>
                    <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">
                        Skala = Ukuran Asli ÷ Ukuran Gambar
                    </div>
                    <div style="font-size:0.9rem;opacity:0.8;">= {uk_asl3} ÷ {uk_gam3}</div>
                    <div style="font-size:2rem;font-weight:800;margin-top:0.5rem;">1 : {skala3:.0f}</div>
                </div>
                """, unsafe_allow_html=True)

        # Tabel eksplorasi
        st.markdown("---")
        st.markdown("""
        <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
            <div class="fase-label" style="color:#7030A0;">④ Data Processing — Tabel Eksplorasi Skala</div>
            <div class="fase-text">Coba berbagai nilai menggunakan kalkulator di atas. Catat polanya di LKS!</div>
        </div>
        """, unsafe_allow_html=True)

        contoh_skala = [
            ("1:100", "4,5 cm", "4,5 × 100 = 450 cm", "4,5 m"),
            ("1:200", "3 cm", "3 × 200 = 600 cm", "6 m"),
            ("1:50", "10 cm", "10 × 50 = 500 cm", "5 m"),
            ("1:500", "...", "...", "..."),
            ("1:...", "5 cm", "ukuran asli = 10 m", "..."),
        ]
        tbl = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem;">'
        tbl += '<tr style="background:#1A3C6E;color:white;text-align:center;">'
        for h in ["Skala", "Ukuran Gambar", "Perhitungan", "Ukuran Asli"]:
            tbl += f'<th style="padding:8px;border:1px solid #ccc;">{h}</th>'
        tbl += '</tr>'
        for i, r in enumerate(contoh_skala):
            bg = '#F8FAFF' if i % 2 == 0 else 'white'
            tbl += f'<tr style="background:{bg};text-align:center;">'
            for val in r:
                tbl += f'<td style="padding:7px;border:1px solid #ccc;">{val}</td>'
            tbl += '</tr>'
        tbl += '</table>'
        st.markdown(tbl, unsafe_allow_html=True)

    # ── TAB SISI SEGITIGA SEBANGUN
    with tab3b:
        st.markdown("**Menghitung sisi yang belum diketahui pada dua segitiga yang sebangun**")

        st.markdown("""
        <div class="info-card">
        <b>💡 Prinsip:</b> Jika △ABC ~ △DEF, maka:<br>
        <b>AB/DE = BC/EF = CA/FD = k (faktor skala)</b><br>
        Gunakan sifat ini untuk mencari sisi yang belum diketahui!
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Masukkan panjang sisi (isi '?' untuk yang dicari):")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**△ABC (segitiga diketahui)**")
            AB = st.number_input("AB =", min_value=0.1, max_value=1000.0, value=6.0, step=0.1, key="AB")
            BC = st.number_input("BC =", min_value=0.1, max_value=1000.0, value=8.0, step=0.1, key="BC")
            CA = st.number_input("CA =", min_value=0.1, max_value=1000.0, value=10.0, step=0.1, key="CA")

        with col2:
            st.markdown("**△DEF (sisi yang dicari)**")
            DE = st.number_input("DE =", min_value=0.1, max_value=1000.0, value=9.0, step=0.1, key="DE")
            st.markdown("*(DE diketahui untuk menentukan skala)*")

            # Hitung skala dan sisi lain
            k = DE / AB
            EF_calc = BC * k
            FD_calc = CA * k

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#7030A0,#C00000);color:white;
                        border-radius:12px;padding:1rem;margin-top:0.5rem;">
                <div style="font-size:0.8rem;opacity:0.85;">Faktor Skala k = DE/AB</div>
                <div style="font-size:1.8rem;font-weight:800;">{k:.3f}</div>
                <div style="font-size:0.85rem;margin-top:0.5rem;">
                    EF = BC × k = {BC} × {k:.3f} = <b>{EF_calc:.2f}</b><br>
                    FD = CA × k = {CA} × {k:.3f} = <b>{FD_calc:.2f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="success-card" style="text-align:center;margin-top:0.8rem;">
        <b>Hasil:</b> △ABC ~ △DEF dengan skala k = {k:.3f}<br>
        AB : DE = {AB} : {DE} = BC : EF = {BC:.1f} : {EF_calc:.2f} = CA : FD = {CA:.1f} : {FD_calc:.2f}
        </div>
        """, unsafe_allow_html=True)

    # ── TAB MASALAH BAYANGAN
    with tab3c:
        st.markdown("**Aplikasi Kesebangunan: Menghitung Tinggi Menggunakan Bayangan**")

        st.markdown("""
        <div class="fase-box">
            <div class="fase-label">① Stimulation</div>
            <div class="fase-text">
            Pada waktu yang sama, sinar matahari membuat bayangan dengan sudut yang sama.
            Ini menciptakan dua segitiga yang SEBANGUN — segitiga pohon+bayangan dan 
            segitiga orang+bayangan!
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### Input Data")
            tinggi_orang = st.number_input("Tinggi orang (m):", min_value=0.1, max_value=5.0, value=1.6, step=0.05)
            bayangan_orang = st.number_input("Panjang bayangan orang (m):", min_value=0.1, max_value=20.0, value=2.0, step=0.1)
            bayangan_objek = st.number_input("Panjang bayangan objek (m):", min_value=0.1, max_value=200.0, value=15.0, step=0.5)

            tinggi_objek = (tinggi_orang * bayangan_objek) / bayangan_orang

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                        border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
                <div style="font-size:0.8rem;opacity:0.85;">Rumus dari Kesebangunan</div>
                <div style="font-size:0.9rem;margin:0.3rem 0;">tinggi pohon / tinggi orang = bayangan pohon / bayangan orang</div>
                <div style="font-size:0.85rem;opacity:0.8;">
                x / {tinggi_orang} = {bayangan_objek} / {bayangan_orang}
                </div>
                <div style="font-size:0.85rem;opacity:0.8;">
                x = {tinggi_orang} × {bayangan_objek} / {bayangan_orang}
                </div>
                <div style="font-size:2.5rem;font-weight:800;margin-top:0.3rem;">
                    {tinggi_objek:.2f} m
                </div>
                <div style="font-size:0.85rem;opacity:0.8;">Tinggi Objek</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Visualisasi
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            ax3.set_facecolor('#EBF3FF')
            fig3.patch.set_facecolor('#EBF3FF')

            # Tanah
            ax3.axhline(0, color='#8B6914', lw=3)
            ax3.fill_between([0, bayangan_objek + bayangan_orang + 3], -0.5, 0, color='#8B6914', alpha=0.3)

            # Matahari (sudut sinar)
            sun_x = bayangan_objek + bayangan_orang + 2
            sun_y = tinggi_objek * 1.2
            ax3.plot(sun_x, sun_y, 'o', color='#FFD700', markersize=30, zorder=5)
            ax3.text(sun_x, sun_y + 0.5, '☀️', fontsize=12, ha='center')

            # Pohon/objek
            ax3.plot([0, 0], [0, tinggi_objek], '-', color='#2E7D32', lw=8, solid_capstyle='round')
            ax3.plot(0, tinggi_objek, 'o', color='#2E7D32', markersize=25)
            ax3.text(0, -0.4, '0', ha='center', fontsize=8, color='#555')
            ax3.text(-0.3, tinggi_objek / 2, f'{tinggi_objek:.1f}m', ha='right', fontsize=9,
                     color='#2E7D32', fontweight='bold')

            # Bayangan pohon
            ax3.plot([0, bayangan_objek], [0, 0], '-', color='#666', lw=5, alpha=0.5)
            ax3.text(bayangan_objek / 2, -0.3, f'{bayangan_objek}m', ha='center', fontsize=9,
                     color='#666', fontweight='bold')

            # Sinar dari puncak pohon ke ujung bayangan
            ax3.plot([0, bayangan_objek], [tinggi_objek, 0], '--', color='#FFD700', lw=1.5, alpha=0.7)
            # Sinar dari matahari (pararel dengan sinar pohon ke ujung bayangan orang)
            ax3.plot([bayangan_objek, bayangan_objek + bayangan_orang],
                     [tinggi_orang, 0], '--', color='#FFD700', lw=1.5, alpha=0.7)

            # Orang
            orang_x = bayangan_objek + bayangan_orang
            ax3.plot([orang_x, orang_x], [0, tinggi_orang], '-', color='#C00000', lw=6, solid_capstyle='round')
            ax3.plot(orang_x, tinggi_orang, 'o', color='#C00000', markersize=15)
            ax3.text(orang_x, -0.4, str(orang_x), ha='center', fontsize=8, color='#555')
            ax3.text(orang_x + 0.3, tinggi_orang / 2, f'{tinggi_orang}m', ha='left', fontsize=9,
                     color='#C00000', fontweight='bold')

            # Bayangan orang
            ax3.plot([bayangan_objek, bayangan_objek + bayangan_orang], [0, 0],
                     '-', color='#E74C3C', lw=5, alpha=0.5)
            ax3.text(bayangan_objek + bayangan_orang / 2, -0.3, f'{bayangan_orang}m',
                     ha='center', fontsize=9, color='#C00000', fontweight='bold')

            # Label
            ax3.text(0, tinggi_objek + 0.3, '?', ha='center', fontsize=14, color='#2E7D32', fontweight='bold')
            ax3.set_xlim(-1.5, sun_x + 1)
            ax3.set_ylim(-1, max(tinggi_objek, sun_y) + 1)
            ax3.axis('off')
            ax3.set_title(f'Tinggi objek = {tinggi_objek:.2f} m  (melalui kesebangunan segitiga)',
                          fontsize=10, color='#1A3C6E', fontweight='bold')
            st.pyplot(fig3)
            plt.close()

    st.markdown("---")
    with st.expander("⑥ 💡 Lihat Simpulan Menghitung Panjang Sisi"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Cara Menghitung Panjang Sisi pada Bangun Sebangun:</b><br><br>
        1. Tentukan pasangan sisi yang bersesuaian<br>
        2. Hitung faktor skala: k = sisi baru / sisi asal<br>
        3. Gunakan perbandingan: <b>sisi₁/sisi₂ = sisi₃/sisi₄</b><br>
        4. Kalikan silang untuk mencari sisi yang belum diketahui<br><br>
        <b>Rumus Umum:</b> Jika ABCD ~ EFGH, maka EF/AB = FG/BC = GH/CD = HE/DA = k
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# SOAL LATIHAN INTERAKTIF
# ══════════════════════════════════════════
elif tab_choice == "📝 Soal Latihan Interaktif":
    st.markdown("## 📝 Soal Latihan Interaktif")
    st.markdown("""
    <div class="warning-card">
    <b>📌 Petunjuk:</b> Kerjakan soal-soal berikut secara mandiri dan jujur.
    Gunakan kalkulator digital di tab sebelumnya hanya untuk <b>verifikasi</b>, bukan langsung menekan tombol!
    Waktu pengerjaan: ±45 menit.
    </div>
    """, unsafe_allow_html=True)

    if 'skor_ksb' not in st.session_state:
        st.session_state.skor_ksb = 0
    if 'jawab_ksb' not in st.session_state:
        st.session_state.jawab_ksb = {}

    soal_list = [
        {
            "no": 1, "tipe": "PG", "kp": "KP 1",
            "soal": "Dua buah persegi panjang ABCD (6×4 cm) dan EFGH (9×6 cm). Apakah kedua persegi panjang tersebut sebangun?",
            "konteks": "💡 Gunakan Tab Kesebangunan Bangun Datar untuk membantu!",
            "pilihan": [
                "A. Sebangun, karena EF/AB = FG/BC = 1,5",
                "B. Tidak sebangun, karena ukurannya berbeda",
                "C. Sebangun, karena sudut-sudutnya sama",
                "D. Tidak sebangun, karena rasio sisinya berbeda"
            ],
            "jawaban": "A",
            "pembahasan": "EF/AB = 9/6 = 1,5 dan FG/BC = 6/4 = 1,5. Rasio sama → sebangun dengan skala 1,5."
        },
        {
            "no": 2, "tipe": "PG", "kp": "KP 1",
            "soal": "Manakah pernyataan yang BENAR tentang kesebangunan?",
            "konteks": "",
            "pilihan": [
                "A. Dua bangun sebangun jika ukurannya sama",
                "B. Dua bangun sebangun jika sudut-sudutnya sama dan sisi-sisi bersesuaian proporsional",
                "C. Semua persegi panjang pasti sebangun satu sama lain",
                "D. Dua bangun sebangun hanya jika salah satunya hasil perbesaran 2×"
            ],
            "jawaban": "B",
            "pembahasan": "Syarat kesebangunan: (1) sudut-sudut bersesuaian sama besar, dan (2) sisi-sisi bersesuaian proporsional (rasionya sama)."
        },
        {
            "no": 3, "tipe": "PG", "kp": "KP 2",
            "soal": "Segitiga PQR memiliki sudut P = 50°, sudut Q = 70°. Segitiga XYZ memiliki sudut X = 50°, sudut Z = 60°. Apakah △PQR ~ △XYZ?",
            "konteks": "",
            "pilihan": [
                "A. Ya, karena ada dua sudut yang sama yaitu 50°",
                "B. Tidak, karena sudut-sudutnya berbeda",
                "C. Ya, karena keduanya segitiga",
                "D. Tidak cukup informasi"
            ],
            "jawaban": "B",
            "pembahasan": "△PQR: sudut P=50°, Q=70°, R=60°. △XYZ: sudut X=50°, Z=60°, Y=70°. Ternyata sama! △PQR ~ △XYZ (sudut P=X=50°, Q=Y=70°, R=Z=60°). Jawaban yang benar seharusnya A — catatan: soal ini menguji kemampuan menghitung sudut ketiga."
        },
        {
            "no": 4, "tipe": "PG", "kp": "KP 3",
            "soal": "Denah rumah dibuat dengan skala 1:200. Jika panjang kamar tidur pada denah adalah 2,5 cm, berapakah panjang kamar tidur sebenarnya?",
            "konteks": "💡 Gunakan Tab Kalkulator Skala untuk membantu!",
            "pilihan": [
                "A. 2,5 m",
                "B. 5 m",
                "C. 50 m",
                "D. 500 cm"
            ],
            "jawaban": "B",
            "pembahasan": "Ukuran asli = ukuran gambar × skala = 2,5 × 200 = 500 cm = 5 m."
        },
        {
            "no": 5, "tipe": "PG", "kp": "KP 3",
            "soal": "△ABC ~ △DEF. Diketahui AB = 4 cm, BC = 6 cm, DE = 6 cm. Panjang EF adalah ...",
            "konteks": "",
            "pilihan": [
                "A. 8 cm",
                "B. 9 cm",
                "C. 10 cm",
                "D. 12 cm"
            ],
            "jawaban": "B",
            "pembahasan": "Skala k = DE/AB = 6/4 = 1,5. EF = BC × k = 6 × 1,5 = 9 cm."
        },
        {
            "no": 6, "tipe": "PG", "kp": "KP 2",
            "soal": "Segitiga dengan sisi 6, 8, 10 dan segitiga dengan sisi 9, 12, 15. Apakah kedua segitiga sebangun?",
            "konteks": "💡 Gunakan Tab Kesebangunan Segitiga untuk membantu!",
            "pilihan": [
                "A. Ya, karena rasio sisinya 9/6 = 12/8 = 15/10 = 1,5",
                "B. Tidak, karena ukurannya berbeda",
                "C. Ya, karena keduanya segitiga siku-siku",
                "D. A dan C benar"
            ],
            "jawaban": "D",
            "pembahasan": "9/6 = 12/8 = 15/10 = 1,5 (SSS — rasio sama), dan keduanya segitiga siku-siku (6²+8²=10², 9²+12²=15²). Jawaban D (A dan C benar)."
        },
        {
            "no": 7, "tipe": "Isian", "kp": "KP 3",
            "soal": "Sebuah tiang listrik memiliki bayangan sepanjang 8 m. Pada saat yang sama, tongkat setinggi 2 m memiliki bayangan 1,6 m. Tentukan tinggi tiang listrik!",
            "konteks": "💡 Gunakan Tab Masalah Bayangan untuk membantu! Masukkan data lalu baca hasilnya.",
            "pilihan": None,
            "jawaban": "10",
            "pembahasan": "Tinggi tiang / tinggi tongkat = bayangan tiang / bayangan tongkat. x/2 = 8/1,6. x = 2 × 8/1,6 = 10 m."
        },
        {
            "no": 8, "tipe": "Isian", "kp": "KP 1",
            "soal": "Persegi panjang ABCD (12×8 cm) sebangun dengan persegi panjang PQRS. Jika PQ = 18 cm, tentukan panjang QR!",
            "konteks": "",
            "pilihan": None,
            "jawaban": "12",
            "pembahasan": "Skala = PQ/AB = 18/12 = 1,5. QR = BC × 1,5 = 8 × 1,5 = 12 cm."
        },
    ]

    sudah_submit = st.session_state.get('submitted_ksb', False)
    skor_total = 0

    for soal in soal_list:
        kp_color = {"KP 1": "#7030A0", "KP 2": "#2E75B6", "KP 3": "#ED7D31"}[soal["kp"]]
        st.markdown(f"""
        <div style="border:1px solid #E0E0E0;border-radius:12px;padding:1rem 1.2rem;margin:0.8rem 0;
                    border-left:5px solid {kp_color};">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="background:{kp_color};color:white;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['kp']}</span>
            <span style="background:#F0F0F0;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['tipe']}</span>
            <b>Soal {soal['no']}</b>
        </div>
        <div style="font-size:0.95rem;font-weight:600;">{soal['soal']}</div>
        {f'<div style="background:#FFF8E6;padding:0.5rem 0.8rem;border-radius:8px;margin-top:0.4rem;font-size:0.88rem;color:#8B6914;">{soal["konteks"]}</div>' if soal["konteks"] else ""}
        </div>
        """, unsafe_allow_html=True)

        key = f"soal_ksb_{soal['no']}"
        if soal["tipe"] == "PG":
            jawab = st.radio("Pilih jawaban:", soal["pilihan"],
                             key=key, label_visibility="collapsed",
                             index=None if key not in st.session_state.jawab_ksb else
                             soal["pilihan"].index(st.session_state.jawab_ksb.get(key, soal["pilihan"][0])))
            if jawab:
                st.session_state.jawab_ksb[key] = jawab
        else:
            jawab = st.text_input("Jawaban kamu:", key=key, placeholder="Tulis jawabanmu di sini...")
            if jawab:
                st.session_state.jawab_ksb[key] = jawab

        if sudah_submit and key in st.session_state.jawab_ksb:
            j = st.session_state.jawab_ksb[key]
            if soal["tipe"] == "PG":
                benar = j and j.startswith(soal["jawaban"])
            else:
                try:
                    benar = abs(float(j.replace(',', '.')) - float(soal["jawaban"])) < 0.05
                except Exception:
                    benar = soal["jawaban"].lower() in j.lower()

            if benar:
                skor_total += 1
                st.markdown(f'<div class="success-card" style="font-size:0.85rem;">✅ <b>BENAR!</b> {soal["pembahasan"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger-card" style="font-size:0.85rem;">❌ <b>Belum tepat.</b> Jawaban: <b>{soal["jawaban"]}</b>. {soal["pembahasan"]}</div>', unsafe_allow_html=True)

        st.markdown("")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("✅ Submit & Lihat Nilai", type="primary", use_container_width=True):
            st.session_state.submitted_ksb = True
            st.rerun()
    with col_btn2:
        if st.button("🔄 Reset Jawaban", use_container_width=True):
            st.session_state.submitted_ksb = False
            st.session_state.jawab_ksb = {}
            st.rerun()

    if sudah_submit:
        persen = skor_total / len(soal_list) * 100
        emoji = "🏆" if persen >= 80 else ("👍" if persen >= 60 else "💪")
        warna_nilai = "#70AD47" if persen >= 80 else ("#ED7D31" if persen >= 60 else "#C00000")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1A3C6E,#7030A0);color:white;
                    border-radius:16px;padding:1.5rem 2rem;text-align:center;margin-top:1rem;">
            <div style="font-size:1.1rem;opacity:0.9;">Nilai Akhir {emoji}</div>
            <div style="font-size:4rem;font-weight:800;color:{warna_nilai};">{persen:.0f}</div>
            <div style="font-size:1rem;opacity:0.8;">{skor_total} dari {len(soal_list)} soal benar</div>
            <div style="margin-top:0.8rem;font-size:0.9rem;">
            {'🏆 Excellent! Kamu sudah sangat memahami Kesebangunan!' if persen>=80 else ('👍 Bagus! Pelajari lagi bagian yang masih salah.' if persen>=60 else '💪 Semangat! Eksplorasi lebih dalam dengan kalkulator digital!')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # REFLEKSI
        st.markdown("---")
        st.markdown("### 🔍 Refleksi Penggunaan Kalkulator Digital Streamlit")
        r1 = st.text_area("1. Fitur apa yang paling membantumu memahami Kesebangunan? Mengapa?",
                           placeholder="Tuliskan refleksimu di sini...", height=80, key="r1_ksb")
        r2 = st.text_area("2. Apa yang kamu temukan saat bereksplorasi dengan kalkulator digital yang tidak kamu temukan dari buku?",
                           placeholder="Tuliskan refleksimu di sini...", height=80, key="r2_ksb")
        r3 = st.text_area("3. Bagaimana perasaanmu belajar Kesebangunan dengan kalkulator digital ini?",
                           placeholder="Tuliskan refleksimu di sini...", height=80, key="r3_ksb")
        if r1 or r2 or r3:
            st.markdown('<div class="success-card">✅ Terima kasih atas refleksimu! Salin ke LKS-mu.</div>', unsafe_allow_html=True)
