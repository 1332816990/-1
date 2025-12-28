import streamlit as st
import openai
from dotenv import load_dotenv
import os

# --- 1. 配置和初始化 ---

# 加载环境变量，用于安全地存储API密钥
load_dotenv()

# 从环境变量中获取OpenAI API密钥
# 如果你不想用.env文件，可以直接在这里替换为：openai.api_key = "你的API密钥"
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- 2. 定义提示词模板 ---

def get_prompt_template(topic, style):
    """根据用户输入生成完整的提示词"""
    template = f"""
    # 角色
    你是一位资深的短视频内容策划与脚本撰写专家，擅长创作在抖音、小红书等平台上流行的、引人入胜的短视频脚本。

    # 任务
    根据用户提供的主题和风格，为其生成一个时长约为60秒的短视频脚本。

    # 要求
    1.  **脚本结构**：请严格按照以下结构输出：
        *   **视频标题**：一个吸引人点击的标题。
        *   **视频风格**：总结视频的整体调性。
        *   **背景音乐建议**：推荐适合视频风格的BGM类型或歌曲。
        *   **脚本内容**：以表格形式呈现，包含【景号】、【景别】、【时长】、【画面】、【台词/音效】五列。
            *   **景号**：场景编号。
            *   **景别**：远景、全景、中景、近景、特写等。
            *   **时长**：每个镜头的时长，例如 "0 - 3s"。
            *   **画面**：详细描述镜头内容，包括人物动作、表情、场景布置、运镜方式等。
            *   **台词/音效**：人物的对话、旁白，以及需要配合的背景音乐或特殊音效。

    2.  **内容要求**：
        *   **开头3秒**：必须设计一个强有力的“黄金3秒”，迅速抓住观众眼球，激发好奇心。
        *   **语言风格**：语言要口语化、有网感，避免生硬说教。
        *   **节奏**：整体节奏要明快，避免拖沓。
        *   **互动性**：在脚本中自然地引导用户进行点赞、关注或评论。

    # 输入
    1.  **视频主题**: {topic}
    2.  **视频风格**: {style}

    # 输出
    请直接生成符合上述要求的短视频脚本。
    """
    return template

# --- 3. 定义AI生成函数 ---

def generate_script(prompt):
    try:
        # 新版本的客户端初始化方式
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")  # 从环境变量获取密钥
        )
        response = client.chat.completions.create(  # 新版本的接口
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"发生错误：{e}"

# --- 4. Streamlit 用户界面 ---

def main():
    # 设置页面配置
    st.set_page_config(
        page_title="AI短视频脚本生成器",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 页面标题
    st.title("🎬 AI短视频脚本生成器")
    st.markdown("---")

    # 创建两列布局
    col1, col2 = st.columns(2)

    # 左侧：输入区
    with col1:
        st.header("📝 输入你的想法")
        topic = st.text_input("视频主题", placeholder="例如：5分钟快速出门妆")
        style = st.selectbox("视频风格", ["幽默搞笑", "干货教学", "情感共鸣", "生活日常", "探店测评"])

        generate_button = st.button("🚀 开始生成脚本")

    # 右侧：输出区
    with col2:
        st.header("🎭 生成的脚本")
        # 使用一个容器来动态更新内容
        output_container = st.empty()

        # 初始状态显示提示信息
        output_container.info("请在左侧输入主题并选择风格，然后点击“开始生成脚本”按钮。")

    # 当点击按钮时执行
    if generate_button:
        if not topic:
            st.error("视频主题不能为空！")
        else:
            # 显示生成中的状态
            with st.spinner("AI正在努力构思脚本，请稍候..."):
                # 获取完整的提示词
                final_prompt = get_prompt_template(topic, style)
                # 调用AI生成脚本
                script = generate_script(final_prompt)

            # 在右侧容器中显示生成的脚本
            output_container.markdown(f"```markdown\n{script}\n```")
            st.success("脚本生成完成！")

# --- 运行应用 ---
if __name__ == "__main__":
    main()
