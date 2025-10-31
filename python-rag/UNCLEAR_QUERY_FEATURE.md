# 🤔 Unclear Query Clarification Feature

## Overview

This feature handles **ambiguous, vague, or unclear queries** by:
1. **Acknowledging** what the student asked
2. **Clarifying** the system's purpose (placement preparation)
3. **Redirecting** to studies with actionable suggestions

Unlike the standard off-topic detection, this feature uses **AI-like understanding** to handle queries that don't clearly match any category.

---

## 🎯 Problem It Solves

### Before This Feature
**Student**: "tell me something"  
**System**: *Tries to answer with RAG, wastes API call, gives irrelevant response*

### After This Feature
**Student**: "tell me something"  
**System**: 
> "Hi John! I understand you're asking about: 'tell me something'
> 
> While I'd love to help with that, my main purpose is to assist you with your placement preparation! 📚
> 
> Let's focus on what really matters for your career success:
> • You have 2 assessments ready to take
> • Practice makes perfect - let's work on your skills!
> • Your future placement depends on consistent preparation
> 
> What would you like to focus on today? 🎯"

---

## 🧠 How It Works

### Detection Logic

An unclear query is detected when:

1. **Relevance score is borderline (30-45%)**
   - Not clearly off-topic
   - Not clearly relevant
   - Ambiguous intent

2. **Very short and vague (≤2 words, <60% relevance)**
   - "hi"
   - "ok"
   - "help"
   - "what"

3. **Contains vague phrases (<60% relevance)**
   - "what about"
   - "tell me about"
   - "i want to know"
   - "can you"
   - "something"
   - "anything"
   - "stuff"
   - "things"
   - "random"
   - "just curious"
   - "wondering"
   - "thinking about"

### Processing Flow

```
Query → Calculate Relevance Score
    ↓
Is Unclear? (Check conditions)
    ↓
    ├─ YES → Generate Clarification Message
    │         ↓
    │         Acknowledge Query
    │         ↓
    │         Explain Purpose
    │         ↓
    │         Redirect to Studies
    │         ↓
    │         Provide Suggestions
    │         ↓
    │         Return to Student
    │
    └─ NO → Continue with normal flow
              ↓
              Check if Off-Topic
              ↓
              Process with RAG or Redirect
```

---

## 📊 Examples

### Example 1: Very Vague Query

**Input**:
```
Query: "what about"
Relevance Score: 35%
Word Count: 2
```

**Detection**:
```python
is_unclear = True  # Borderline relevance (30-45%)
```

**Output**:
```
Hi Sarah! I understand you're asking about: "what about"

While I'd love to help with that, my main purpose is to assist you 
with your placement preparation! 📚

Let's focus on what really matters for your career success:
• You have 3 assessments ready to take
• Practice makes perfect - let's work on your skills!
• Your future placement depends on consistent preparation

What would you like to focus on today? 🎯
```

---

### Example 2: Incomplete Thought

**Input**:
```
Query: "tell me something"
Relevance Score: 40%
Contains: "tell me" (vague phrase)
```

**Detection**:
```python
is_unclear = True  # Contains vague phrase + borderline relevance
```

**Output**:
```
Hi John! I understand you're asking about: "tell me something"

While I'd love to help with that, my main purpose is to assist you 
with your placement preparation! 📚

Let's focus on what really matters for your career success:
• You have 2 assessments ready to take
• Practice makes perfect - let's work on your skills!
• Your future placement depends on consistent preparation

What would you like to focus on today? 🎯
```

---

### Example 3: Too Short

**Input**:
```
Query: "hi"
Relevance Score: 55%
Word Count: 1
```

**Detection**:
```python
is_unclear = True  # Very short (≤2 words) + relevance < 60%
```

**Output**:
```
Hi Emma! I understand you're asking about: "hi"

While I'd love to help with that, my main purpose is to assist you 
with your placement preparation! 📚

Let's focus on what really matters for your career success:
• You have 1 assessment ready to take
• Practice makes perfect - let's work on your skills!
• Your future placement depends on consistent preparation

What would you like to focus on today? 🎯
```

---

## 🔄 Comparison with Off-Topic Detection

| Feature | Off-Topic Detection | Unclear Query Clarification |
|---------|-------------------|---------------------------|
| **Trigger** | Relevance < 30% OR clear off-topic keywords | Relevance 30-45% OR vague phrases |
| **Purpose** | Block distractions (games, movies, etc.) | Handle ambiguous queries |
| **Response** | Personalized redirect based on performance | Acknowledge + explain + redirect |
| **Tone** | Motivational, performance-based | Clarifying, helpful, redirecting |
| **Example** | "What's the best game?" | "tell me something" |

---

## 🧪 Testing

### Run Tests
```bash
cd python-rag
python test_unclear_queries.py
```

### Expected Results
```
======================================================================
UNCLEAR QUERY CLARIFICATION - TEST SUITE
======================================================================

Testing Unclear Query Detection:
----------------------------------------------------------------------
✓ PASS | Score:  35% | Unclear: True  | Very vague - no context
       Query: "what about"

✓ PASS | Score:  40% | Unclear: True  | Ambiguous request
       Query: "tell me something"

✓ PASS | Score:  45% | Unclear: True  | Unclear what help is needed
       Query: "can you help"

✓ PASS | Score:  80% | Unclear: False | Clear request
       Query: "show me assessments"

✓ PASS | Score:  75% | Unclear: False | Specific question
       Query: "what is my score"

======================================================================
RESULTS: 21 passed, 0 failed out of 21 tests
======================================================================
```

---

## ⚙️ Configuration

### Adjust Unclear Threshold

Edit `intelligent_cutoff.py`:

```python
def is_unclear_query(self, query: str, relevance_score: int) -> bool:
    # Adjust borderline range
    if 30 <= relevance_score <= 45:  # Change 45 to 50 for wider range
        return True
    
    # Adjust short query threshold
    if word_count <= 2 and relevance_score < 60:  # Change 60 to 70 for stricter
        return True
```

### Add Custom Vague Phrases

```python
unclear_phrases = [
    'what about', 'tell me about', 'i want to know', 'can you',
    'something', 'anything', 'stuff', 'things', 'random',
    'just curious', 'wondering', 'thinking about',
    # Add your custom phrases here
    'whatever', 'dunno', 'idk', 'not sure'
]
```

---

## 📈 Benefits

### 1. Better User Experience
- ✅ Acknowledges what student asked (shows understanding)
- ✅ Doesn't ignore or dismiss their query
- ✅ Gently guides back to studies
- ✅ Maintains helpful, friendly tone

### 2. Cost Savings
- ✅ Prevents unclear queries from reaching API
- ✅ No wasted tokens on ambiguous requests
- ✅ Faster response time (no API call)

### 3. Improved Focus
- ✅ Redirects vague curiosity to concrete actions
- ✅ Provides specific next steps
- ✅ Encourages goal-oriented behavior

### 4. Analytics Value
- ✅ Track types of unclear queries
- ✅ Identify common vague patterns
- ✅ Improve system based on data

---

## 📊 Real-World Scenarios

### Scenario 1: Bored Student
**Query**: "just curious"  
**Intent**: Vague, no specific goal  
**Response**: Acknowledge curiosity, redirect to assessments  
**Outcome**: Student gets concrete action items

### Scenario 2: Incomplete Question
**Query**: "what about"  
**Intent**: Started question, didn't finish  
**Response**: Acknowledge incomplete thought, offer help with placement prep  
**Outcome**: Student clarifies or focuses on studies

### Scenario 3: Too Brief
**Query**: "ok"  
**Intent**: Unclear acknowledgment  
**Response**: Friendly redirect to available assessments  
**Outcome**: Student gets actionable options

---

## 🔍 Monitoring

### Log Messages
```
[INFO] Unclear query detected: relevance=35% - Using AI clarification
[INFO] Generated clarification for: "what about"
[INFO] Redirected to studies with 4 suggestions
```

### Metrics to Track
1. **Unclear Query Frequency**: How often students ask vague questions
2. **Common Vague Patterns**: Most frequent unclear phrases
3. **Clarification Effectiveness**: Do students engage after clarification?
4. **Relevance Score Distribution**: Where do unclear queries fall?

---

## 🎓 Best Practices

### 1. Keep Clarifications Friendly
- Don't sound robotic or dismissive
- Acknowledge their query genuinely
- Use encouraging language

### 2. Provide Concrete Next Steps
- Always include available assessments count
- Offer specific suggestions
- Make it easy to take action

### 3. Monitor and Adjust
- Track which queries trigger clarification
- Adjust thresholds based on patterns
- Refine vague phrase list over time

### 4. Balance Helpfulness and Focus
- Don't be too restrictive (frustrates users)
- Don't be too lenient (defeats purpose)
- Find the sweet spot for your audience

---

## 🔄 Integration with Existing System

### Works Seamlessly With:
- ✅ Off-topic detection (checked after unclear check)
- ✅ Relevance scoring (uses same scores)
- ✅ Personalized redirects (shares context)
- ✅ Study suggestions (same suggestion system)

### Processing Order:
```
1. Calculate Relevance Score
2. Check if Unclear → Clarify & Redirect
3. Check if Off-Topic → Redirect
4. Process with RAG (if relevant)
```

---

## 📝 Example Responses

### For Different Student Levels

#### Beginner (0 assessments)
```
Hi John! I understand you're asking about: "random stuff"

While I'd love to help with that, my main purpose is to assist you 
with your placement preparation! 📚

Let's focus on what really matters for your career success:
• You have 3 assessments ready to take
• Practice makes perfect - let's work on your skills!
• Your future placement depends on consistent preparation

What would you like to focus on today? 🎯
```

#### Active Student (some completed)
```
Hi Sarah! I understand you're asking about: "just curious"

While I'd love to help with that, my main purpose is to assist you 
with your placement preparation! 📚

Let's focus on what really matters for your career success:
• You have 1 assessment ready to take
• Practice makes perfect - let's work on your skills!
• Your future placement depends on consistent preparation

What would you like to focus on today? 🎯
```

---

## ✅ Success Criteria

Your unclear query feature is working when:

✅ Vague queries (30-45% relevance) trigger clarification  
✅ Short queries (≤2 words) are handled appropriately  
✅ Unclear phrases are detected and clarified  
✅ Students receive friendly, helpful redirects  
✅ Concrete next steps are always provided  
✅ Logs show clarification triggers  
✅ Students engage with suggestions after clarification

---

## 🚀 Quick Start

### 1. Feature Already Integrated
The unclear query feature is built into `intelligent_cutoff.py` and `context_handler_enhanced.py`.

### 2. Test It
```bash
cd python-rag
python test_unclear_queries.py
```

### 3. Try Live
Start the RAG service and test with:
- "what about"
- "tell me something"
- "just curious"
- "random stuff"

### 4. Monitor Logs
Look for:
```
Unclear query detected: relevance=XX% - Using AI clarification
```

---

## 🎉 Summary

The **Unclear Query Clarification Feature** intelligently handles ambiguous queries by:

1. **Understanding** the query is vague/unclear
2. **Acknowledging** what the student asked
3. **Explaining** the system's purpose
4. **Redirecting** to placement preparation
5. **Providing** actionable next steps

**Result**: Students feel heard while staying focused on their goals! 🎯

---

**Status**: ✅ **IMPLEMENTED & TESTED**  
**Version**: 1.0  
**Integration**: Seamless with existing cutoff system  
**Ready**: Production-ready
