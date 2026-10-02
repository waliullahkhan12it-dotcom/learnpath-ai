
import streamlit as st
from groq import Groq
import os
import re


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🌱",
    layout="wide"
)


# ============================================================
# SIMPLE COLORS AND DESIGN
# ============================================================

st.markdown("""
# 🌱 AI Learning Roadmap Generator

### 🤖 Create a personalized learning journey with AI

Tell us what you want to learn, your current skill level,
and how much time you have. The AI will create a roadmap
designed specifically for you.

---
""")


# ============================================================
# GROQ API
# ============================================================

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


# ============================================================
# FUNCTION TO REMOVE HTML FROM AI RESPONSE
# ============================================================

def clean_ai_response(text):

    # Convert common HTML line breaks into normal new lines
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    # Remove HTML tags such as:
    # <div>, <p>, <h1>, <table>, etc.
    text = re.sub(r"<[^>]*>", "", text)

    # Remove excessive empty lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    return text.strip()


# ============================================================
# AI ROADMAP FUNCTION
# ============================================================

def generate_roadmap(field, level, learning_time):

    prompt = f"""
You are an expert learning roadmap designer.

Create a detailed, practical and realistic learning roadmap.

LEARNER INFORMATION:

Field:
{field}

Current skill level:
{level}

Available learning time:
{learning_time}


ROADMAP REQUIREMENTS:

Create a realistic roadmap based on the learner's
skill level and available learning time.

Organize the roadmap week by week.

For every week include:

1. Main topics
2. Important concepts
3. Practical exercises
4. Recommended learning resources
5. A small practical project when appropriate
6. Expected learning outcome


At the end include:

FINAL PROJECT
Give one realistic final project related to the field.

SKILLS AFTER COMPLETION
List the important skills the learner should have.

NEXT STEPS
Explain what the learner should study after completing
this roadmap.


VERY IMPORTANT FORMATTING RULES:

Do NOT use HTML.

Never use:
<br>
<div>
</div>
<p>
</p>
<h1>
<h2>
<h3>
<table>
<tr>
<td>

Do not use HTML tags of any kind.

Use ONLY normal Markdown and plain text.

Use headings like:

## Week 1

Use bullet points like:

- Topic
- Exercise
- Project

Use normal line breaks.

Make the roadmap clear, readable and easy to understand.

Do not make the amount of work unrealistic for the
available learning time.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    answer = response.choices[0].message.content

    # Clean any HTML that the AI may have returned
    answer = clean_ai_response(answer)

    return answer


# ============================================================
# FEATURES
# ============================================================

st.header("✨ Why use this application?")

col1, col2, col3 = st.columns(3)


with col1:

    st.success(
        """
        ### 🎯 Personalized

        Your roadmap is created according to
        your skill level, goals and available time.
        """
    )


with col2:

    st.info(
        """
        ### 🧠 AI Powered

        Artificial intelligence creates a
        structured learning path for your field.
        """
    )


with col3:

    st.warning(
        """
        ### 🚀 Project Based

        Learn through practical exercises
        and real-world projects.
        """
    )


st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

st.header("📚 Create Your Learning Roadmap")

st.write(
    "Enter the following information:"
)


# ============================================================
# FIELD
# ============================================================

field = st.text_input(
    "🎓 What do you want to learn?",
    placeholder="Example: Python Programming"
)


# ============================================================
# SKILL LEVEL
# ============================================================

level = st.selectbox(
    "📊 What is your current skill level?",

    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


# ============================================================
# LEARNING TIME
# ============================================================

learning_time = st.text_input(
    "⏳ How much time do you have?",
    placeholder="Example: 3 months"
)


st.write("")


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.button(
    "🚀 Generate My Learning Roadmap",
    use_container_width=True
)


# ============================================================
# GENERATE ROADMAP
# ============================================================

if generate_button:

    # Check field
    if field.strip() == "":

        st.error(
            "⚠️ Please enter the field you want to learn."
        )

    # Check learning time
    elif learning_time.strip() == "":

        st.error(
            "⚠️ Please enter your available learning time."
        )

    else:

        # Show loading message
        with st.spinner(
            "🤖 AI is creating your personalized roadmap..."
        ):

            try:

                # Generate roadmap
                roadmap = generate_roadmap(
                    field,
                    level,
                    learning_time
                )


                # ====================================================
                # SHOW RESULT
                # ====================================================

                st.divider()

                st.header(
                    "📚 Your Personalized Learning Roadmap"
                )

                st.success(
                    f"✅ Roadmap created for {field}"
                )

                st.write(
                    f"**Skill Level:** {level}"
                )

                st.write(
                    f"**Learning Time:** {learning_time}"
                )

                st.divider()

                # Display clean AI answer
                st.markdown(roadmap)


            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating "
                    "the roadmap."
                )

                st.write(
                    "Error details:"
                )

                st.code(
                    str(e)
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 AI Learning Roadmap Generator | "
    "Learn smarter. Practice better. Build your future."
)
