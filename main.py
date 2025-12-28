import streamlit as st
from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIError
import os
import time

# --- 1. 配置和初始化 (安全优化：环境变量读取密钥 + 本地缓存，无硬编码) ---
st.set_page_config(
    page_title="AI短视频脚本生成器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 侧边栏配置密钥，安全优先，不会硬编码在代码里
with st.sidebar:
    st.title("🔑 API配置")
    API_KEY = st.text_input("请输入你的OpenAI API密钥", type="password", value=st.session_state.get("api_key", ""))
    if API_KEY:
        st.session_state["api_key"] = API_KEY  # 本地缓存密钥，无需重复输入
    st.warning("✅ 密钥仅本地缓存，不会上传任何平台，安全可靠！")
    st.divider()
    st.info(
        "风格说明：\n✅幽默搞笑：适合短视频爆款\n✅干货教学：步骤清晰易模仿\n✅情感共鸣：容易涨粉\n✅生活日常：流量稳定\n✅探店测评：转化率高")

# 初始化OpenAI客户端
client = None
if API_KEY and len(API_KEY) > 10:
    client = OpenAI(api_key=API_KEY.strip())

# --- 2. 定义提示词模板 (核心优化：拆分system+user角色，GPT理解更精准) ---
# ✅ system角色：固定的AI身份、规则、格式要求（GPT的核心准则）
SYSTEM_PROMPT = """
你是一位资深的短视频内容策划与脚本撰写专家，擅长创作抖音、小红书爆款60秒短视频脚本。
严格按照以下要求输出内容，缺一不可：
1. 输出结构必须包含：视频标题、视频风格、背景音乐建议、脚本内容。
2. 脚本内容必须用【标准markdown表格】呈现，固定五列：景号、景别、时长、画面、台词/音效，列名不可修改。
3. 开头3秒必须是黄金3秒，快速抓住观众眼球，激发好奇心。
4. 语言风格口语化、有网感，节奏明快，自然引导点赞、关注、评论互动。
5. 时长总计严格控制在60秒左右，每个镜头时长标注格式为 0-3s 这种样式。
6. 画面描述要详细，包含人物动作、表情、运镜方式，台词/音效区分旁白、对话、BGM、特效音。
"""


def get_user_prompt(topic, style):
    """仅传递用户核心输入，精简token，GPT响应更快"""
    return f"生成一个【{style}】风格的短视频脚本，视频主题：{topic}，时长约60秒。"


# --- 3. 定义AI生成函数 (全量优化：细分异常捕获+参数调整+超时+重试) ---
def generate_script(user_prompt):
    """调用OpenAI API生成脚本，带完整异常处理"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},  # 正确的角色拆分
                {"role": "user", "content": user_prompt.strip()}
            ],
            temperature=0.8,  # 提高一点随机性，脚本更有创意
            top_p=0.9,  # 增加可控性，避免内容跑偏
            max_tokens=3000,  # 足够生成完整脚本，不会截断
            timeout=20,  # 超时设置，防止页面卡死
        )
        return response.choices[0].message.content.strip()

    # 细分异常，精准提示错误原因，方便排查
    except AuthenticationError:
        return "❌ 认证失败：你的API密钥无效/过期，请检查密钥是否正确！"
    except RateLimitError:
        return "❌ 限流/额度不足：你的OpenAI账号额度用完，或请求频率过高，请稍后再试！"
    except ConnectionError:
        return "❌ 网络错误：无法连接到OpenAI服务器，请检查你的网络/科学上网配置！"
    except APIError:
        return "❌ API接口错误：OpenAI服务器暂时不可用，请稍后重试！"
    except Exception as e:
        return f"❌ 未知错误：{str(e)}"


# --- 4. Streamlit 用户界面 (全量优化：体验+交互+样式) ---
def main():
    # 全局样式优化，让排版更美观
    st.markdown("""
        <style>
            .stMarkdown { font-size: 15px; line-height: 1.6; }
            .stButton>button { background-color: #165DFF; color: white; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

    # 页面标题
    st.title("🎬 AI短视频脚本生成器（优化完整版）")
    st.markdown("---")

    # 创建两列布局
    col1, col2 = st.columns(2, gap="large")

    # 左侧：输入区
    with col1:
        st.header("📝 输入你的想法")
        topic = st.text_input("视频主题", placeholder="例如：5分钟快速出门妆、办公室减脂零食测评",
                              help="必填，输入具体主题，生成效果更好")
        style = st.selectbox("视频风格", ["幽默搞笑", "干货教学", "情感共鸣", "生活日常", "探店测评"])

        # 新增：一键清空按钮
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_button = st.button("🚀 开始生成脚本", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ 清空内容", use_container_width=True)

    # 右侧：输出区
    with col2:
        st.header("🎭 生成的短视频脚本")
        # 核心优化：滚动容器展示脚本，内容再多也不会撑满页面
        output_container = st.container(height=700, border=True)
        with output_container:
            if "script_content" in st.session_state:
                st.markdown(st.session_state["script_content"])
            else:
                st.info("✨ 请在左侧输入视频主题并选择风格，点击「开始生成脚本」即可创作")

    # 清空内容逻辑
    if clear_button:
        st.session_state.pop("script_content", None)
        st.rerun()

    # 生成脚本核心逻辑
    if generate_button:
        # 严谨校验：去空格后为空则报错
        topic_clean = topic.strip()
        if not topic_clean:
            st.error("❌ 视频主题不能为空，也不能只输入空格！")
        elif not client:
            st.error("❌ 请先在左侧边栏输入你的OpenAI API密钥！")
        else:
            # 加载动画绑定输出区，视觉聚焦
            with output_container:
                with st.spinner("🎨 AI正在构思爆款脚本，正在生成表格结构，请稍候..."):
                    user_prompt = get_user_prompt(topic_clean, style)
                    script = generate_script(user_prompt)
                    st.session_state["script_content"] = script
                    st.markdown(script)

            # 成功提示在输出区下方，视觉统一
            st.success("✅ 脚本生成完成！可直接复制使用，祝你的视频爆火～")
            # 新增：一键复制脚本功能，超级实用
            st.code(st.session_state["script_content"], language="markdown")


# --- 运行应用 ---
if __name__ == "__main__":
    main()
