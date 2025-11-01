# 📚 MathAI User Guide

## Getting Better Responses

### 🎯 Response Length Guide

MathAI automatically adjusts response length based on your question:

| Question Type            | Response Style | Example                           |
| ------------------------ | -------------- | --------------------------------- |
| **Simple Calculations**  | Concise        | "What is 2+2?" → Brief answer     |
| **Single-Step Problems** | Moderate       | "Solve x + 5 = 10" → Key steps    |
| **Complex Problems**     | Detailed       | "Integrate x²" → Full explanation |

### ✍️ How to Ask Questions

#### ✅ Good Questions (Get Concise Responses):

```
What is 15 + 27?
Calculate 100 - 45
What is 8 × 7?
Solve x + 3 = 10
```

#### ✅ Good Questions (Get Detailed Responses):

```
Explain how to solve 2x² + 5x - 3 = 0
What is the derivative of sin(x)?
Prove the Pythagorean theorem
How do you integrate e^x?
```

#### ❌ Avoid:

```
What is weather today? (Not math-related)
How to hack? (Blocked by guardrails)
Tell me about history (Not math-related)
```

---

## 🎨 Understanding Responses

### Response Components:

1. **Step-by-Step Solution**: Numbered steps with explanations
2. **Calculations**: Shown clearly with working
3. **Final Answer**: Clearly highlighted
4. **Source Info**: Shows if answer came from KB or web search
5. **Confidence Score**: How confident the AI is (0-100%)

### Example Response Format:

```
### Step-by-Step Solution:

**Step 1: Understand the problem**
- Reasoning: [explanation]
- Calculation: [math work]

**Step 2: Apply the method**
- Reasoning: [explanation]
- Calculation: [math work]

**Final Answer:** [result]
```

---

## 🔧 Using Features

### 1️⃣ Like/Dislike Buttons

- 👍 **Like**: Quick positive feedback (rating: 5)
- 👎 **Dislike**: Quick negative feedback (rating: 2)
- No modal opens - feedback sent silently

### 2️⃣ Detailed Feedback (··· button)

Opens feedback modal where you can:

- Rate 1-5 stars
- Add comments
- Suggest improvements
- Helps AI learn better

### 3️⃣ Copy Button

- Copies solution to clipboard
- Great for notes or sharing

### 4️⃣ Settings Panel

Access via sidebar:

- Choose response style (Concise/Balanced/Detailed)
- Theme selection
- Preferences saved locally

---

## 💡 Tips for Best Results

### For Quick Answers:

```
Keep questions simple and direct:
✅ "What is 25% of 80?"
✅ "Factor x² - 9"
✅ "Simplify √16"
```

### For Learning:

```
Ask for explanations:
✅ "Explain how to solve quadratic equations"
✅ "What is the concept of derivatives?"
✅ "How do I find the area of a circle?"
```

### For Problem Solving:

```
Provide context:
✅ "I have an equation 3x + 7 = 22. How do I solve it?"
✅ "Need to find the volume of a cylinder, r=5, h=10"
✅ "How do I calculate compound interest?"
```

---

## 🚀 Advanced Usage

### Using the Knowledge Base:

- AI checks its knowledge base first
- If confidence is low, searches the web
- Shows source in metadata

### Web Search Integration:

- Automatically triggered for:
  - Current events in math
  - Specialized topics
  - When KB confidence < 50%
- Cites sources in response

### Feedback Learning:

- Your feedback improves future responses
- Positive feedback (4-5 stars) helps AI learn
- Improved solutions stored for similar questions

---

## 🎓 Subject Coverage

### ✅ Supported Topics:

- **Algebra**: Equations, expressions, polynomials
- **Calculus**: Derivatives, integrals, limits
- **Geometry**: Shapes, areas, volumes, theorems
- **Trigonometry**: Functions, identities, equations
- **Statistics**: Mean, median, probability
- **Arithmetic**: Basic operations, percentages
- **Number Theory**: Primes, factors, GCD/LCM

### 🔄 Coming Soon:

- Linear algebra
- Differential equations
- Complex analysis
- Graph theory

---

## 📊 Monitoring Your Usage

### Analytics Dashboard:

Access via sidebar → "Analytics"

Shows:

- Total queries asked
- Average rating of responses
- Rating distribution
- Feedback trends

### Chat History:

- Saved per session
- Recent queries in sidebar
- Click to view previous answers

---

## 🛡️ Safety Features

### Input Guardrails:

- ✅ Math questions allowed
- ❌ Inappropriate content blocked
- ❌ Non-math questions rejected
- Max query length: 500 characters

### Output Guardrails:

- Ensures educational content
- Blocks inappropriate responses
- Maintains quality standards

---

## 🔍 Troubleshooting Common Issues

### "Please ask a mathematics question"

**Cause**: Question not recognized as math-related
**Fix**: Include math keywords or numbers

```
❌ "What is the meaning of life?"
✅ "What is the value of π?"
```

### Very Long Responses

**Cause**: Question triggered detailed explanation mode
**Fix**:

1. Use Settings → Response Style → Concise
2. OR ask more specific questions:
   - ❌ "Tell me about calculus"
   - ✅ "What is a derivative?"

### No Response / Error

**Causes**:

1. Backend not running
2. API key issue
3. Network problem

**Fix**: Check browser console (F12) for errors

---

## 🌟 Best Practices

### DO:

✅ Ask clear, specific questions
✅ Provide context when needed
✅ Use feedback buttons to improve AI
✅ Check source and confidence scores
✅ Copy solutions for your notes

### DON'T:

❌ Ask multiple questions at once
❌ Include personal information
❌ Expect answers to non-math questions
❌ Ignore guardrail warnings

---

## 📈 Getting the Most Value

### Daily Use Tips:

1. **Morning Review**: Ask about concepts you learned yesterday
2. **Homework Help**: Get step-by-step guidance (don't just copy!)
3. **Exam Prep**: Practice problems with immediate feedback
4. **Concept Clarity**: Ask "Explain [concept]" for understanding

### Learning Strategy:

1. Ask question
2. Read solution carefully
3. Try similar problems yourself
4. Use feedback to improve explanations
5. Review analytics to track progress

---

## 💬 Example Conversations

### Example 1: Quick Calculation

```
You: What is 15% of 200?
AI: To find 15% of 200:
    15% = 15/100 = 0.15
    0.15 × 200 = 30
    Answer: 30
```

### Example 2: Problem Solving

```
You: Solve 2x + 5 = 13
AI: ### Step-by-Step Solution:
    Step 1: Subtract 5 from both sides
    2x = 8

    Step 2: Divide both sides by 2
    x = 4

    Final Answer: x = 4
```

### Example 3: Concept Explanation

```
You: What is a derivative?
AI: A derivative measures the rate of change...
    [Detailed explanation with examples]
```

---

## 🎯 Success Metrics

You're using MathAI effectively when:

- ✅ Getting helpful responses consistently
- ✅ Understanding solutions, not just answers
- ✅ Using feedback to improve future responses
- ✅ Learning new concepts through explanations
- ✅ Solving problems independently after guidance

---

## 📞 Getting Help

If you encounter issues:

1. Check TROUBLESHOOTING.md
2. Review browser console (F12)
3. Run: `python complete_connection.py`
4. Check backend logs

For feature requests or bugs:

- Use the feedback modal
- Describe the issue clearly
- Include example query if relevant
