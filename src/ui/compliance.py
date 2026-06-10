import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-inner">
                <div class="hero-eyebrow">✦ CARD COMPARE</div>
                <h1>クレジットカード比較</h1>
                <p class="hero-sub">
                    エポスプラチナを基準に、年会費・還元率・特典を
                    あなたの条件で横並び比較
                </p>
                <div class="hero-pills">
                    <span class="disclaimer-pill">独立メディア</span>
                    <span class="disclaimer-pill">試算は参考値</span>
                    <span class="disclaimer-pill">#PR含む場合あり</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <div class="site-footer">
            <h4>免責事項</h4>
            <p>
                本ページの試算・比較結果は参考情報であり、正確性・完全性を保証するものではありません。
                年会費・還元率・特典内容は各カード会社の規定により変更される場合があります。
                最新の条件・お申し込みは各カード会社の公式サイトでご確認ください。
                本サイトはエポスカード株式会社の公式サイトではありません。
            </p>
            <h4>広告について（#PR）</h4>
            <p>
                Phase 1 では公式URLのみを掲載しています。
                アフィリエイト導入時は申込ボタン付近に広告表記を追加します。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
