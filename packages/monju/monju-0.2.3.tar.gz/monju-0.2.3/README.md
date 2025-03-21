![monju](https://repository-images.githubusercontent.com/873246587/e64acd4c-2d7f-44f8-ab00-bbe7a9e65d41)

# monju: Multi-AI Brainstorming Framework

Monju is a powerful multi-AI brainstorming framework designed to generate, organize, and evaluate ideas using various Large Language Models (LLMs).

The Japanese proverb “三人寄れば文殊の知恵” (San nin yoreba monju no chie) is often translated into English as “Two heads are better than one”. However, a more literal translation would be “When three people gather, they have the wisdom of Manjushri”.

## Features

- Generate ideas based on a given theme
- Organize ideas into mindmaps and affinity diagrams (class diagrams)
- Evaluate generated ideas
- Support for multiple LLM providers (OpenAI, Anthropic, Google)
- Customizable parameters for idea generation

The project started as a web app [monju.ai](https://monju.ai), which was released in July 2024.

This library is the core of monju.ai that does not include frontend part.

For general information of monju.ai, see my article from Medium "[***monju.ai: a creativity enhancement tool that uses multiple generative AIs to generate ideas and organize mind maps***](https://medium.com/@daicom0204/monju-ai-a-creativity-enhancement-tool-that-uses-multiple-generative-ais-to-generate-ideas-and-f13112313084)".

## Brainstorming Process by monju

For the general approach to brainstorming, see [Brainstorming - Wikipedia](https://en.wikipedia.org/wiki/Brainstorming).

The brainstorming process by monju consists of three main steps:

1. Generate ideas in list
2. Organize ideas in mindmap and class diagram in Mermaid
3. Evaluate ideas including overall, good points, and areas for improvement

Each step is implemented as a method in the `Monju` class.

Both mindmap and class diagram are described in Mermaid text format. Output can be drawn by any mermaid-compatible tools mainly in JavaScript, e.g. [Mermaid Live Editor](https://mermaid.live/).

## KJ method (Affinity Diagram)

In Japan, another popular ideation tool "KJ method" is often used as part of brainstorming. This method might be known as "affinity diagram" in English.

The KJ method is to categorize ideas into groups based on their similarity. Each idea is written on a single card, then categorized into groups with labels.

People in Japan hesitate open discussion. Writing in cards and categorizing them into groups might help open mind.

In monju, affinity diagram is generated as class diagram of Mermaid. This process is called "pseudo KJ method" in this library.

For details of KJ method, see [Affinity diagram - Wikipedia](https://en.wikipedia.org/wiki/Affinity_diagram).

## Installation

```bash
pip install monju
```

## Requirements

- Python 3.10 or later
- API keys for the LLM providers

This library uses `LLMMaster`, a unified interface to access major LLM providers. Set API keys following the instructions from [LLM Master](https://github.com/Habatakurikei/llmmaster), another repository by the same author.

## Usage

### Batch Execution

By just one call, all the steps of brainstorming can be done. Here is an typical example.

```python
import json
from pathlib import Path

from monju import Monju

API_KEY = Path('your_api_keys.txt').read_text(encoding='utf-8')

# Use this function to arrange parameters in dictionary format.
def pack_parameters(**kwargs):
    return kwargs


# Initialize monju with your API keys and brainstorming parameters
params = pack_parameters(
    theme="How to survive in the era of emerging AI?",
    ideas=5,
    freedom=0.2,
    language="en"
)
bs = Monju(api_keys=API_KEY, verbose=True, **params)

# Start the brainstorming process
bs.brainstorm()

# Show the results
print(f'Result:\n{json.dumps(bs.record, indent=2, ensure_ascii=False)}')
```

Information related to a session is stored in `bs.record` as `dict`. You can extract items you want separately, or print/save an entire record as JSON.

### Step-by-Step Execution

There is another way to use monju by calling each process step by step.

The following example works equivalently to the batch execution example above.

```python
import json
from pathlib import Path

from monju import Monju

API_KEY = Path('your_api_keys.txt').read_text(encoding='utf-8')

# Use this function to arrange parameters in dictionary format.
def pack_parameters(**kwargs):
    return kwargs


# Initialize monju with your API keys and brainstorming parameters
params = pack_parameters(
    theme="How to survive in the era of emerging AI?",
    ideas=5,
    freedom=0.2,
    language="en"
)

bs = Monju(api_keys=API_KEY, verbose=True, **params)

# Start the brainstorming process
print(f"Status: {bs.status}")
bs.generate_ideas()
print(f"Status: {bs.status}")
bs.organize_ideas()
print(f"Status: {bs.status}")
bs.evaluate_ideas()
print(f"Status: {bs.status}")
bs.verify()
print(f"Status: {bs.status}")

# Show the results
print(f'Result:\n{json.dumps(bs.record, indent=2, ensure_ascii=False)}')
```

Types of `bs.status` are explained in later section.

### Input Parameters

There are several parameters to set for `Monju` class:

- Constractor parameters:
  - `api_keys` (str): API keys for LLMs in `LLMMaster` manner
  - `verbose` (bool): print progress for debugging, default is `False`
- Brainstorming parameters `params` as `dict`:
  - `theme` (str) **required**: theme or topic of brainstorming, a.k.a. prompt
  - `ideas` (int): number of ideas to generate by each LLM
  - `freedom` (float): value of freedom-looking thinking for each LLM, a.k.a. temperature, between 0 and 1. Higher more free-thinking, lower more concervative.
  - `language` (str): language for output, default is `en` and must be followed by two-letter code defined in [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)


### Output Format

Results, `bs.record` in the examples, are given in `dict`. Here is an actual output.

```json
{
  "input": {
    "theme": "How to survive in the era of emerging AI?",
    "ideas": 5,
    "freedom": 0.2,
    "language": "en",
    "idea_generation": {
      "openai": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "prompt": "\nPurpose: Generate 5 ideas on the following \"Theme\" and meeting the \"Conditions\".\n\nConditions:\n1. Propose ideas with free thinking.\n2. Consider the 5W1H when proposing.\n3. Return the results in bullet points as shown in the \"Format\".\n4. The language of the output is in EN of ISO 639-1 format.\n5. Do not include your explanations.\n6. Do not add any unnecessary decorations to the bullet points.\n\nTheme: How to survive in the era of emerging AI?\n\nFormat:\n- Idea\n",
        "temperature": 0.2
      },
      "anthropic": {
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "prompt": "\nPurpose: Generate 5 ideas on the following \"Theme\" and meeting the \"Conditions\".\n\nConditions:\n1. Propose ideas with free thinking.\n2. Consider the 5W1H when proposing.\n3. Return the results in bullet points as shown in the \"Format\".\n4. The language of the output is in EN of ISO 639-1 format.\n5. Do not include your explanations.\n6. Do not add any unnecessary decorations to the bullet points.\n\nTheme: How to survive in the era of emerging AI?\n\nFormat:\n- Idea\n",
        "temperature": 0.2
      },
      "google": {
        "provider": "google",
        "model": "gemini-1.5-flash",
        "prompt": "\nPurpose: Generate 5 ideas on the following \"Theme\" and meeting the \"Conditions\".\n\nConditions:\n1. Propose ideas with free thinking.\n2. Consider the 5W1H when proposing.\n3. Return the results in bullet points as shown in the \"Format\".\n4. The language of the output is in EN of ISO 639-1 format.\n5. Do not include your explanations.\n6. Do not add any unnecessary decorations to the bullet points.\n\nTheme: How to survive in the era of emerging AI?\n\nFormat:\n- Idea\n",
        "temperature": 0.2
      }
    },
    "mindmap": {
      "provider": "openai",
      "model": "gpt-4o"
    },
    "class_diagram": {
      "provider": "openai",
      "model": "gpt-4o"
    },
    "idea_evaluation": {
      "openai": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "prompt": "\nPurpose: Evaluate the \"Mindmap\" based on the \"Theme\" and meeting the \"Conditions\".\n\nTheme: How to survive in the era of emerging AI?\n\nConditions:\n1. Write \"Overall Evaluation\", \"Good Points\", and \"Areas for Improvement\" according to the \"Format\".\n2. The language of the output is in EN of ISO 639-1 format.\n3. Write as concisely and focused on key points as possible.\n4. The mindmap is provided as a class diagram.\n5. Do not add any unnecessary decorations to the bullet points.\n\nMindmap:\nclassDiagram\n    class LifelongLearning {\n        +Embrace lifelong learning\n        +Cultivate adaptability\n        +Continuously update skills\n    }\n    \n    class HumanSkills {\n        +Foster creativity\n        +Develop emotional intelligence\n        +Enhance critical thinking\n        +Invest in unique human skills\n    }\n    \n    class AIIntegration {\n        +Collaborate with AI\n        +Develop specialized skills\n        +Focus on human-AI collaboration\n    }\n    \n    class EthicalAI {\n        +Advocate for ethical AI use\n        +Engage in responsible AI development\n        +Promote equitable AI regulations\n    }\n    \n    class DiverseSkillSet {\n        +Build a diverse skill set\n        +Diversify expertise\n    }\n    \n    class AIUnderstanding {\n        +Develop comprehensive understanding of AI\n        +Make informed decisions\n    }\n    \n    class Entrepreneurship {\n        +Explore entrepreneurial opportunities\n        +Leverage AI for innovative solutions\n    }\n    \n    LifelongLearning --> HumanSkills\n    LifelongLearning --> AIIntegration\n    HumanSkills --> AIIntegration\n    AIIntegration --> EthicalAI\n    EthicalAI --> AIUnderstanding\n    DiverseSkillSet --> AIUnderstanding\n    Entrepreneurship --> AIIntegration\n    Entrepreneurship --> EthicalAI\n\nFormat:\n- Overall Evaluation:\n  - Bullet point\n- Good Points:\n  - Bullet point\n- Areas for Improvement:\n  - Bullet point\n",
        "temperature": 0.7
      },
      "anthropic": {
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "prompt": "\nPurpose: Evaluate the \"Mindmap\" based on the \"Theme\" and meeting the \"Conditions\".\n\nTheme: How to survive in the era of emerging AI?\n\nConditions:\n1. Write \"Overall Evaluation\", \"Good Points\", and \"Areas for Improvement\" according to the \"Format\".\n2. The language of the output is in EN of ISO 639-1 format.\n3. Write as concisely and focused on key points as possible.\n4. The mindmap is provided as a class diagram.\n5. Do not add any unnecessary decorations to the bullet points.\n\nMindmap:\nclassDiagram\n    class LifelongLearning {\n        +Embrace lifelong learning\n        +Cultivate adaptability\n        +Continuously update skills\n    }\n    \n    class HumanSkills {\n        +Foster creativity\n        +Develop emotional intelligence\n        +Enhance critical thinking\n        +Invest in unique human skills\n    }\n    \n    class AIIntegration {\n        +Collaborate with AI\n        +Develop specialized skills\n        +Focus on human-AI collaboration\n    }\n    \n    class EthicalAI {\n        +Advocate for ethical AI use\n        +Engage in responsible AI development\n        +Promote equitable AI regulations\n    }\n    \n    class DiverseSkillSet {\n        +Build a diverse skill set\n        +Diversify expertise\n    }\n    \n    class AIUnderstanding {\n        +Develop comprehensive understanding of AI\n        +Make informed decisions\n    }\n    \n    class Entrepreneurship {\n        +Explore entrepreneurial opportunities\n        +Leverage AI for innovative solutions\n    }\n    \n    LifelongLearning --> HumanSkills\n    LifelongLearning --> AIIntegration\n    HumanSkills --> AIIntegration\n    AIIntegration --> EthicalAI\n    EthicalAI --> AIUnderstanding\n    DiverseSkillSet --> AIUnderstanding\n    Entrepreneurship --> AIIntegration\n    Entrepreneurship --> EthicalAI\n\nFormat:\n- Overall Evaluation:\n  - Bullet point\n- Good Points:\n  - Bullet point\n- Areas for Improvement:\n  - Bullet point\n",
        "temperature": 0.7
      },
      "google": {
        "provider": "google",
        "model": "gemini-1.5-flash",
        "prompt": "\nPurpose: Evaluate the \"Mindmap\" based on the \"Theme\" and meeting the \"Conditions\".\n\nTheme: How to survive in the era of emerging AI?\n\nConditions:\n1. Write \"Overall Evaluation\", \"Good Points\", and \"Areas for Improvement\" according to the \"Format\".\n2. The language of the output is in EN of ISO 639-1 format.\n3. Write as concisely and focused on key points as possible.\n4. The mindmap is provided as a class diagram.\n5. Do not add any unnecessary decorations to the bullet points.\n\nMindmap:\nclassDiagram\n    class LifelongLearning {\n        +Embrace lifelong learning\n        +Cultivate adaptability\n        +Continuously update skills\n    }\n    \n    class HumanSkills {\n        +Foster creativity\n        +Develop emotional intelligence\n        +Enhance critical thinking\n        +Invest in unique human skills\n    }\n    \n    class AIIntegration {\n        +Collaborate with AI\n        +Develop specialized skills\n        +Focus on human-AI collaboration\n    }\n    \n    class EthicalAI {\n        +Advocate for ethical AI use\n        +Engage in responsible AI development\n        +Promote equitable AI regulations\n    }\n    \n    class DiverseSkillSet {\n        +Build a diverse skill set\n        +Diversify expertise\n    }\n    \n    class AIUnderstanding {\n        +Develop comprehensive understanding of AI\n        +Make informed decisions\n    }\n    \n    class Entrepreneurship {\n        +Explore entrepreneurial opportunities\n        +Leverage AI for innovative solutions\n    }\n    \n    LifelongLearning --> HumanSkills\n    LifelongLearning --> AIIntegration\n    HumanSkills --> AIIntegration\n    AIIntegration --> EthicalAI\n    EthicalAI --> AIUnderstanding\n    DiverseSkillSet --> AIUnderstanding\n    Entrepreneurship --> AIIntegration\n    Entrepreneurship --> EthicalAI\n\nFormat:\n- Overall Evaluation:\n  - Bullet point\n- Good Points:\n  - Bullet point\n- Areas for Improvement:\n  - Bullet point\n",
        "temperature": 0.7
      }
    }
  },
  "output": {
    "elapsed_time": [
      5.969,
      7.166,
      6.533
    ],
    "ideas": {
      "openai": "- Embrace lifelong learning: Continuously update skills and knowledge to stay relevant in a rapidly changing job market.\n- Foster creativity and emotional intelligence: Develop skills that AI cannot replicate, such as empathy, creativity, and critical thinking.\n- Collaborate with AI: Learn to work alongside AI tools to enhance productivity and efficiency in various tasks.\n- Advocate for ethical AI use: Engage in discussions and initiatives that promote responsible AI development and implementation.\n- Build a diverse skill set: Diversify expertise across multiple fields to adapt to various roles that may emerge due to AI advancements.",
      "anthropic": "- Develop a comprehensive understanding of AI capabilities and limitations to make informed decisions.\n- Cultivate adaptability and lifelong learning to stay relevant in a rapidly evolving job market.\n- Invest in developing unique human skills that complement AI, such as creativity, emotional intelligence, and critical thinking.\n- Advocate for ethical AI development and implementation to ensure AI benefits humanity.\n- Explore entrepreneurial opportunities in the AI industry to leverage your expertise and contribute to its responsible growth.",
      "google": "- **Idea:** Develop specialized skills that complement AI, such as creativity, emotional intelligence, and critical thinking.\n- **Idea:** Embrace lifelong learning and adapt to the evolving job market by acquiring new skills and knowledge.\n- **Idea:** Focus on building strong human connections and fostering collaboration to leverage the strengths of both humans and AI.\n- **Idea:** Advocate for ethical AI development and regulations to ensure responsible and equitable use of AI technology.\n- **Idea:** Explore entrepreneurial opportunities that leverage AI to create innovative solutions and address societal challenges."
    },
    "mindmap": "mindmap\n    root [How to survive in the era of emerging AI?]\n        -Lifelong Learning and Adaptability-\n            -Embrace lifelong learning: Continuously update skills and knowledge to stay relevant in a rapidly changing job market.-\n            -Cultivate adaptability and lifelong learning to stay relevant in a rapidly evolving job market.-\n            -Embrace lifelong learning and adapt to the evolving job market by acquiring new skills and knowledge.-\n        -Human Skills Development-\n            -Foster creativity and emotional intelligence: Develop skills that AI cannot replicate, such as empathy, creativity, and critical thinking.-\n            -Invest in developing unique human skills that complement AI, such as creativity, emotional intelligence, and critical thinking.-\n            -Develop specialized skills that complement AI, such as creativity, emotional intelligence, and critical thinking.-\n        -Collaboration with AI-\n            -Collaborate with AI: Learn to work alongside AI tools to enhance productivity and efficiency in various tasks.-\n            -Focus on building strong human connections and fostering collaboration to leverage the strengths of both humans and AI.-\n        -Ethical AI Advocacy-\n            -Advocate for ethical AI use: Engage in discussions and initiatives that promote responsible AI development and implementation.-\n            -Advocate for ethical AI development and implementation to ensure AI benefits humanity.-\n            -Advocate for ethical AI development and regulations to ensure responsible and equitable use of AI technology.-\n        -Diverse Skill Set and Entrepreneurship-\n            -Build a diverse skill set: Diversify expertise across multiple fields to adapt to various roles that may emerge due to AI advancements.-\n            -Explore entrepreneurial opportunities in the AI industry to leverage your expertise and contribute to its responsible growth.-\n            -Explore entrepreneurial opportunities that leverage AI to create innovative solutions and address societal challenges.-\n        -Understanding AI-\n            -Develop a comprehensive understanding of AI capabilities and limitations to make informed decisions.-",
    "class_diagram": "classDiagram\n    class LifelongLearning {\n        +Embrace lifelong learning\n        +Cultivate adaptability\n        +Continuously update skills\n    }\n    \n    class HumanSkills {\n        +Foster creativity\n        +Develop emotional intelligence\n        +Enhance critical thinking\n        +Invest in unique human skills\n    }\n    \n    class AIIntegration {\n        +Collaborate with AI\n        +Develop specialized skills\n        +Focus on human-AI collaboration\n    }\n    \n    class EthicalAI {\n        +Advocate for ethical AI use\n        +Engage in responsible AI development\n        +Promote equitable AI regulations\n    }\n    \n    class DiverseSkillSet {\n        +Build a diverse skill set\n        +Diversify expertise\n    }\n    \n    class AIUnderstanding {\n        +Develop comprehensive understanding of AI\n        +Make informed decisions\n    }\n    \n    class Entrepreneurship {\n        +Explore entrepreneurial opportunities\n        +Leverage AI for innovative solutions\n    }\n    \n    LifelongLearning --> HumanSkills\n    LifelongLearning --> AIIntegration\n    HumanSkills --> AIIntegration\n    AIIntegration --> EthicalAI\n    EthicalAI --> AIUnderstanding\n    DiverseSkillSet --> AIUnderstanding\n    Entrepreneurship --> AIIntegration\n    Entrepreneurship --> EthicalAI",
    "evaluation": {
      "openai": "- Overall Evaluation:\n  - The mindmap effectively outlines key strategies for surviving in the era of emerging AI, focusing on skill development and ethical considerations.\n\n- Good Points:\n  - Emphasizes the importance of lifelong learning and adaptability.\n  - Highlights the need for human skills that AI cannot replicate, such as creativity and emotional intelligence.\n  - Addresses the significance of ethical AI practices and regulations.\n  - Encourages collaboration between humans and AI, fostering innovation.\n\n- Areas for Improvement:\n  - Could provide more specific examples or actionable steps for each category.\n  - May benefit from integrating more on the potential risks of AI and how to mitigate them.\n  - Could explore the impact of AI on various industries in greater detail.",
      "anthropic": "EN\n\nOverall Evaluation:\n- The mindmap provides a comprehensive and well-structured approach to surviving in the era of emerging AI, covering key aspects such as lifelong learning, human skills, AI integration, ethical AI, diverse skill sets, and entrepreneurship.\n\nGood Points:\n- The mindmap emphasizes the importance of lifelong learning, adaptability, and continuously updating skills to stay relevant in the changing landscape.\n- It highlights the need to foster human-centric skills, such as creativity, emotional intelligence, and critical thinking, to complement AI capabilities.\n- The mindmap recognizes the significance of collaboration between humans and AI, as well as the development of specialized skills to integrate AI effectively.\n- It addresses the importance of ethical AI development and responsible use, as well as the need for informed decision-making and comprehensive understanding of AI.\n- The mindmap encourages the exploration of entrepreneurial opportunities and the leveraging of AI for innovative solutions.\n\nAreas for Improvement:\n- The mindmap could benefit from more specific strategies or actionable steps within each of the key areas to provide clearer guidance on how to implement the proposed approaches.\n- Incorporating examples or case studies could further enhance the practical applicability of the mindmap.\n- Considering the inclusion of additional factors, such as the importance of lifelong learning for mental well-being or the role of interdisciplinary collaboration in navigating the AI landscape, could strengthen the mindmap's comprehensiveness.",
      "google": "- **Overall Evaluation:** The mindmap provides a comprehensive overview of key strategies for surviving in the era of emerging AI. \n- **Good Points:**\n    - The mindmap effectively categorizes strategies into distinct but interconnected areas: Lifelong Learning, Human Skills, AI Integration, Ethical AI, Diverse Skill Set, AI Understanding, and Entrepreneurship.\n    - It highlights the importance of human skills and ethical considerations in navigating the AI landscape.\n    - The connections between the categories demonstrate the interconnectedness of different approaches.\n- **Areas for Improvement:**\n    -  The mindmap could benefit from more specific examples and actionable steps within each category. \n    -  Adding visual cues (e.g., colors, icons) could improve clarity and engagement."
    }
  }
}
```

The `record` object contains the following information:

- `input`:
  - `theme`: same as one in the input parameter.
  - `ideas`: same as one in the input parameter.
  - `freedom`: same as one in the input parameter.
  - `language`: same as one in the input parameter.
  - `idea_generation`: LLM information used for idea generation.
  - `mindmap`: LLM information used for mindmap generation.
  - `class_diagram`: LLM information used for class diagram generation.
  - `idea_evaluation`: LLM information used for idea evaluation.
- `output`:
  - `elapsed_time`: Elapsed time in seconds as `list`: (1) idea generation, (2) mindmap and class diagram generation, (3) idea evaluation in this order. Mindmaps and class diagrams are generated in a single process, running simultaniously.
  - `ideas`: Generated ideas in `dict`.
  - `mindmap`: Mindmap of the generated ideas in Mermaid format.
  - `class_diagram`: Class diagram of the generated ideas in mermaid format.
  - `evaluation`: Evaluation of the generated ideas in dictionary format if multiple LLMs are used.

### Status

On average, one brainstorming session takes about 60 seconds to complete by monju.

There are many calls of `print` in the step-by-step example. Each print shows a different status, which is useful to know progress.

Types of `bs.status` are as follows:

- `not_started`: The brainstorming process has not started. Most of cases, this status is shown when the instance of `Monju` is created.
- `idea_generation`: Generating ideas in progress or finished.
- `idea_organization`: Organizing ideas in mindmap and class diagram in progress or finished.
- `idea_evaluation`: Evaluating ideas in progress or finished.
- `verifying`: Verifying if all the outputs are generated in progress or finished.
- `done`: The brainstorming process is completed.
- `failed`: The brainstorming process is failed at some step.

## Supported LLM Providers

One of the most important features of `Monju` is to generate ideas from multiple LLMs.

`Monju` currently sets the following LLM providers as default of idea generation and evaluation:

- OpenAI: `gpt-4o-mini`
- Anthropic: `claude-3-haiku-20240307`
- Google: `gemini-1.5-flash`

And OpenAI `gpt-4o` is used for mindmap and class diagram generation.

Monju is capable of single or multiple LLMs for each step:

- Generate ideas (multiple/single LLM)
- Organize ideas in mindmap and class diagram (single LLM)
- Evaluate ideas (multiple/single LLM)

You can configure which providers and models to use for each step. Set arguments of LLM information in `params` dictionary by calling `generate_ideas(**params)`, `organize_ideas(**params)`, and `evaluate_ideas(**params)`.

This customization is not possible for the batch brainstorming.

Note that providers are not limited to those shown above. Also possible to user other providers like MistralAI, Groq, Perplexity and so on, as possible as they are defined in `LLMMaster` class.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Apache License 2.0](LICENSE)
