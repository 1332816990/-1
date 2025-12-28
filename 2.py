import streamlit as st
import requests
import json

# ===================== 页面基础配置（科技蓝新风格） =====================
st.set_page_config(
    page_title="AI内容创作助手 (Kimi 驱动)",
    page_icon="🚀",
    layout="wide"
)

# 自定义样式（科技蓝为主色调）
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
        white-space: pre-wrap; /* 保留换行符 */
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


# ===================== Kimi API 核心函数（保持不变） =====================
def call_kimi_api(api_key, prompt, model="moonshot-v1-8k"):
    """
    调用Kimi（月之暗面）API生成内容
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


# ===================== Streamlit 界面交互（科技蓝新风格） =====================
# 侧边栏：API密钥配置
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
        help="模型越大，支持的输入输出内容越长"
    )

# 主界面：AI内容创作助手
st.title("🚀 AI 内容创作助手")
st.subheader("基于 Kimi AI 生成高质量的文案、脚本和创意")
st.markdown("---")

# 功能选择卡片
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📝 选择创作类型</div>', unsafe_allow_html=True)
function_type = st.radio(
    "", # 隐藏默认标签
    ["爆款话题推荐", "短视频文案", "直播口播脚本", "评论区互动话术"],
    horizontal=True,
    captions=["生成高热度的话题标签", "创作引人入胜的短视频脚本", "撰写专业的直播流程话术", "设计高互动性的评论回复"]
)
st.markdown('</div>', unsafe_allow_html=True)

# 输入区卡片
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💡 输入你的创作需求</div>', unsafe_allow_html=True)
placeholder_map = {
    "爆款话题推荐": "例如：生成10个关于「AI绘画」的高热度抖音话题。",
    "短视频文案": "例如：为「一款便携咖啡机」写一个30秒的带货短视频文案，要求有吸引力的开头和明确的购买引导。",
    "直播口播脚本": "例如：为「新书发布会」生成一个5分钟的直播开场和作者介绍脚本。",
    "评论区互动话术": "例如：当粉丝问「产品什么时候发货」时，生成3种不同风格的回复话术。"
}
user_input = st.text_area(
    "", # 隐藏默认标签
    placeholder=placeholder_map[function_type],
    height=150,
    help="越详细的需求，生成的内容质量越高"
)

# 附加选项
col1, col2 = st.columns(2)
with col1:
    add_tags = st.checkbox("✅ 生成时附带热门标签（#xxx）", value=True)
with col2:
    add_bgm = st.checkbox("🎶 推荐适配的背景音乐", value=True)

st.markdown('</div>', unsafe_allow_html=True)


# 生成按钮
if st.button("🔥 开始创作", use_container_width=True):
    if not kimi_api_key:
        st.error("❌ 请先在左侧侧边栏输入你的 Kimi API Key！")
    elif not user_input.strip():
        st.warning("⚠️ 创作需求不能为空，请输入你的想法。")
    else:
        # 构建Prompt
        prompt_base = f"""
        你是一位专业的内容策略师。请根据用户需求，创作一份高质量的「{function_type}」。
        用户需求：「{user_input}」
        创作要求：
        1. 内容必须原创、专业且符合主流平台规范。
        2. 语言风格需根据类型调整，或口语化、或正式、或幽默。
        3. 结构清晰，重点突出，具有很强的吸引力和实用性。
        """
        if add_tags:
            prompt_base += "4. 在内容末尾，生成5-8个与主题高度相关的热门标签（格式：#话题名）。"
        if add_bgm and function_type in ["短视频文案", "直播口播脚本"]:
            prompt_base += "5. 推荐2-3首适配内容风格和情感的背景音乐（说明推荐理由）。"

        # 显示加载状态并生成内容
        with st.spinner("🤖 AI 正在深度思考，为您创作中..."):
            generated_text = call_kimi_api(kimi_api_key, prompt_base, model_option)

        # 展示结果
        st.markdown("---")
        st.markdown('<div class="card-title">🎯 创作结果</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="generated-content">{generated_text}</div>', unsafe_allow_html=True)
        st.success("✅ 创作完成！您可以直接复制使用。")

# 示例提示
with st.expander("📌 点击查看优秀需求示例"):
    st.write("""
    *   **爆款话题推荐**: 为「宠物智能喂食器」生成10个适合小红书平台的高热度话题。
    *   **短视频文案**: 为「一场说走就走的露营」创作一个富有感染力的Vlog短视频脚本。
    *   **直播口播脚本**: 撰写一份「知识付费课程」的直播引流和转化话术，包含破冰、价值塑造和限时优惠环节。
    *   **评论区互动话术**: 当有客户在评论区反馈「产品有瑕疵」时，生成一套专业且能安抚情绪的危机公关回复话术。
    """)
