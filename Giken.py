import streamlit as st

# 既存のページ設定
st.set_page_config(page_title="スキークラブ連絡帳", page_icon="⛷️")

# PWA・PWABuilder用の設定読み込み（追加）
st.markdown("""
    <link rel="manifest" href="https://raw.githubusercontent.com/buita04-cell/GIKEN-ski-club-app/main/manifest.json">
    <link rel="icon" href="https://raw.githubusercontent.com/buita04-cell/GIKEN-ski-club-app/main/icon.jpg">
""", unsafe_allow_html=True)
import streamlit as st

# 既存のページ設定
st.set_page_config(page_title="スキークラブ連絡帳", page_icon="⛷️")

# PWA用マニフェストファイルの読み込み設定（追加）
st.markdown(
    '<link rel="manifest" href="./manifest.json">',
    unsafe_allow_html=True
)

import streamlit as st
import datetime

# ページ設定（スマホで見やすいようタイトルとアイコンを設定）
st.set_page_config(page_title="スキークラブ雪活", page_icon="⛷️")

# --------------------------------------------------
# 1. 管理者側で管理するマスターデータ
# --------------------------------------------------
# 会員マスタ（実際はSupabase等のDBから読み込むことも可能）
MEMBER_LIST = ["選択してください", "武井", "佐藤", "鈴木", "高橋", "田中", "渡辺"]

# 主なゲレンデリスト（静岡県内＋よく行くエリア）
RESORT_LIST = [
    "選択してください",
    "イエティ",
    "リバウェル井川",
    "富士天神山",
    "白馬八方尾根",
    "野沢温泉",
    "志賀高原",
    "その他（県外）"
]

# よく使う一言（スタンプ代わりの選択肢）
QUICK_COMMENTS = [
    "指定なし",
    "最高のパウダー！",
    "バーンが引き締まって快適！",
    "午後はアイスバーン注意",
    "少し混雑しています",
    "休憩中・ランチなう ☕",
    "無事下山・帰路につきます 🚗"
]

# --------------------------------------------------
# 2. アプリ画面レイアウト
# --------------------------------------------------
st.title("⛷️ クラブ専用 ゲレンデ連絡帳")

# タブ切り替え（「ゲレンデなう」と「15秒動画」）
tab1, tab2 = st.tabs(["📍 ゲレンデなう（チェックイン）", "🎥 15秒動画共有"])

# --------------------------------------------------
# TAB 1: ゲレンデなう（文字入力ゼロのチェックイン）
# --------------------------------------------------
with tab1:
    st.subheader("📝 チェックイン・コンディション報告")
    st.caption("※ すべて選ぶだけで送信できます")
    
    # フォーム開始
    with st.form("checkin_form"):
        # ① 会員選択
        member_name = st.selectbox("👤 あなたのお名前", MEMBER_LIST)
        
        # ② ゲレンデ選択
        resort_name = st.selectbox("🏔️ 今どこにいますか？", RESORT_LIST)
        
        # ③ 雪質・コンディション（大きめの選択肢）
        condition = st.radio(
            "❄️ 今日の雪質・状況",
            ["粉雪・パウダー", "圧雪・良好", "シャバ雪・春雪", "硬め・アイスバーン"],
            horizontal=False
        )
        
        # ④ 一言メッセージ（定型文から選ぶだけ）
        comment = st.selectbox("💬 一言メッセージ", QUICK_COMMENTS)
        
        # 送信ボタン（大きめに表示）
        submitted = st.form_submit_button("🚀 これで投稿する（タップ）", use_container_width=True)
    
    # 送信された時の処理
    if submitted:
        if member_name == "選択してください" or resort_name == "選択してください":
            st.error("⚠️ 「お名前」と「ゲレンデ」を選んでからボタンを押してください。")
        else:
            now_time = datetime.datetime.now().strftime("%H:%M")
            st.success(f"✅ {member_name} さんの報告を受け付けました！")
            
            # タイムライン表示イメージ
            st.markdown("---")
            st.markdown(f"**👤 {member_name}** （{now_time}）")
            st.markdown(f"📍 **{resort_name}** ｜ ❄️ {condition}")
            if comment != "指定なし":
                st.info(f"💬 「{comment}」")

# --------------------------------------------------
# TAB 2: 15秒動画共有
# --------------------------------------------------
with tab2:
    st.subheader("🎥 滑走動画の投稿")
    
    with st.form("video_form"):
        v_member_name = st.selectbox("👤 あなたのお名前", MEMBER_LIST, key="video_member")
        v_resort_name = st.selectbox("🏔️ 撮影したゲレンデ", RESORT_LIST, key="video_resort")
        
        # スマホのカメラ起動またはライブラリから選択
        video_file = st.file_uploader("📹 動画を選択（15秒以内）", type=["mp4", "mov"])
        
        v_submitted = st.form_submit_button("📹 動画を送信する", use_container_width=True)
        
    if v_submitted:
        if v_member_name == "選択してください" or video_file is None:
            st.error("⚠️ お名前を選択し、動画ファイルを選んでください。")
        else:
            st.success("✅ 動画が投稿されました！")
            st.video(video_file)