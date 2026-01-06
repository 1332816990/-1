import streamlit as st
import requests
import json

# ===================== 页面基础配置（保留科技蓝风格） =====================
st.set_page_config(
    page_title="AI诗歌创作助手 (Kimi 驱动)",
    page_icon="📜",
    layout="wide"
)

# 自定义样式（保留科技蓝为主色调，仅微调适配诗歌主题）
st.markdown("""
    <style>
    /* 全局样式 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        color: #0F172A; /* 深灰色标题 */
    }
    p, li, div {
        color: #334155; /* 标准文本颜色 */
    }

    /* 输入框样式 */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px; 
        border: 1px solid #CBD5E1; 
        padding: 0.6rem;
        font-size: 14px;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #165DFF;
        box-shadow: 0 0 0 3px rgba(22, 93, 255, 0.1);
        outline: none;
    }

    /* 按钮样式 */
    .stButton button {
        background-color: #165DFF; 
        color: white; 
        border-radius: 8px; 
        padding: 0.6rem 2rem;
        border: none;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #0D47A1;
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] .stMarkdown {
        padding: 0 1rem;
    }

    /* 卡片组件样式 */
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* 生成内容样式 */
    .generated-content {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid #165DFF;
        white-space: pre-wrap; /* 保留换行符，适配诗歌排版 */
        font-family: "SimSun", "Microsoft YaHei", sans-serif; /* 适配诗歌字体 */
        line-height: 2; /* 增大行间距，提升诗歌可读性 */
    }
    .topic-tag {
        color: #165DFF;
        font-weight: 600;
    }

    /* 开关和复选框 */
    .stCheckbox [data-testid="stMarkdownContainer"] {
        padding-left: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


# ===================== Kimi API 核心函数（完全保留） =====================
def call_kimi_api(api_key, prompt, model="moonshot-v1-8k"):
    """
    调用Kimi（月之暗面）API生成诗歌内容
    """
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 1500
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        return f"API请求错误：{e}，响应内容：{response.text}"
    except requests.exceptions.Timeout:
        return "API请求超时，请检查网络或稍后重试"
    except Exception as e:
        return f"未知错误：{str(e)}"


# ===================== Streamlit 界面交互（适配诗歌创作） =====================
# 侧边栏：API密钥配置（保留，无修改）
with st.sidebar:
    st.markdown('<div class="card-title">🔑 API 配置</div>', unsafe_allow_html=True)
    kimi_api_key = st.text_input(
        "Kimi API Key",
        type="password",
        placeholder="sk-...",
        help="从月之暗面官网获取你的API密钥"
    )
    st.divider()
    st.markdown('<div class="card-title">⚙️ 高级设置</div>', unsafe_allow_html=True)
    model_option = st.selectbox(
        "选择模型",
        ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
        index=0,
        help="模型越大，支持的输入输出内容越长（长诗推荐32k/128k）"
    )

# 主界面：AI诗歌创作助手（核心修改）
st.title("📜 AI 诗歌创作助手")
st.subheader("基于 Kimi AI 生成高质量的古体诗、现代诗、词牌等原创诗歌")
st.markdown("---")

# 功能选择卡片（替换为诗歌类型）
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📝 选择诗歌创作类型</div>', unsafe_allow_html=True)
function_type = st.radio(
    "", # 隐藏默认标签
    ["七言律诗", "五言绝句", "现代自由诗", "经典词牌创作", "藏头诗", "节日主题诗"],
    horizontal=True,
    captions=[
        "严格遵循格律的8句七言诗",
        "短小精炼的4句五言诗",
        "无格律限制的现代抒情诗",
        "适配《水调歌头》《念奴娇》等词牌的词作",
        "首字组成指定词语的创意诗",
        "适配中秋/端午/春节等节日的应景诗"
    ]
)
st.markdown('</div>', unsafe_allow_html=True)

# 输入区卡片（适配诗歌创作需求）
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💡 输入你的诗歌创作需求</div>', unsafe_allow_html=True)
# 不同诗歌类型的占位符示例
placeholder_map = {
    "七言律诗": "例如：以「秋日登高」为主题创作一首七言律诗，要求意境开阔，符合平仄格律，押韵平水韵下平十一尤。",
    "五言绝句": "例如：以「江南春雨」为主题创作一首五言绝句，语言清新，情景交融，押韵平水韵上平一东。",
    "现代自由诗": "例如：创作一首关于「故乡的云」的现代自由诗，情感真挚，语言优美，篇幅10-15行。",
    "经典词牌创作": "例如：用《水调歌头》词牌创作一首关于「中秋思亲」的词作，严格遵循词牌格律，押韵词林正韵。",
    "藏头诗": "例如：以「山河无恙」为藏头，创作一首七言绝句，主题为家国情怀，符合格律要求。",
    "节日主题诗": "例如：创作一首关于「春节团圆」的五言律诗，氛围喜庆，贴合节日场景，押韵平水韵。"
}
user_input = st.text_area(
    "", # 隐藏默认标签
    placeholder=placeholder_map[function_type],
    height=150,
    help="越详细的需求（主题、意境、格律、押韵要求），生成的诗歌质量越高"
)

# 附加选项（适配诗歌创作）
col1, col2 = st.columns(2)
with col1:
    add_notes = st.checkbox("📝 生成诗歌注释（解释意境/格律）", value=True)
with col2:
    add_recitation = st.checkbox("🎙️ 推荐朗诵节奏/配乐", value=True)

st.markdown('</div>', unsafe_allow_html=True)


# 生成按钮（修改文案）
if st.button("🔥 开始创作诗歌", use_container_width=True):
    if not kimi_api_key:
        st.error("❌ 请先在左侧侧边栏输入你的 Kimi API Key！")
    elif not user_input.strip():
        st.warning("⚠️ 创作需求不能为空，请输入诗歌主题/意境等要求。")
    else:
        # 构建诗歌专属Prompt（核心修改）
        prompt_base = f"""
        你是一位专业的古典文学和现代诗歌创作专家。请根据用户需求，创作一份高质量的「{function_type}」，要求如下：
        1. 内容原创，符合所选诗歌类型的格式/格律要求（无格律的现代诗除外）；
        2. 意境贴合主题，语言优美，情感真挚，无生僻字但有文学性；
        3. 古体诗/词牌需标注押韵（平水韵/词林正韵），确保平仄、对仗符合规范；
        4. 排版清晰，每句单独成行，便于阅读和朗诵。
        用户创作需求：「{user_input}」
        """
        # 附加选项的Prompt补充
        if add_notes:
            prompt_base += "5. 在诗歌后添加注释：解释诗歌的创作思路、意境内涵，古体诗需额外说明格律/押韵规则。"
        if add_recitation:
            prompt_base += "6. 推荐2-3首适配诗歌情感的背景音乐（如古筝/钢琴曲目），并说明朗诵时的节奏/语速建议。"

        # 显示加载状态并生成诗歌
        with st.spinner("🤖 AI 正在构思诗句，为您创作中..."):
            generated_text = call_kimi_api(kimi_api_key, prompt_base, model_option)

        # 展示结果（保留样式，适配诗歌排版）
        st.markdown("---")
        st.markdown('<div class="card-title">🎯 诗歌创作结果</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="generated-content">{generated_text}</div>', unsafe_allow_html=True)
        st.success("✅ 诗歌创作完成！您可以直接复制使用。")

# 示例提示（替换为诗歌创作示例）
with st.expander("📌 点击查看优秀诗歌创作需求示例"):
    st.write("""
    *   **七言律诗**: 以「边塞戍边」为主题创作七言律诗，风格雄浑悲壮，符合平水韵下平声七阳，颔联颈联对仗工整。
    *   **五言绝句**: 以「夏夜纳凉」为主题创作五言绝句，语言简洁，动静结合，押韵平水韵下平声六麻。
    *   **现代自由诗**: 创作一首关于「城市清晨」的现代诗，融入对生活的感悟，篇幅12行左右，语言细腻。
    *   **经典词牌创作**: 用《念奴娇》词牌创作一首咏史词，主题为「赤壁怀古」，严格遵循词牌格律，押韵词林正韵第十七部。
    *   **藏头诗**: 以「星辰大海」为藏头，创作一首七言律诗，主题为航天梦，符合平仄格律，押韵平水韵下平声九青。
    *   **节日主题诗**: 创作一首端午主题的五言律诗，融入龙舟、艾草、屈原等元素，氛围庄重，押韵平水韵上平声十四寒。
    """)