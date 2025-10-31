# Implementing Intelligent Cutoff System

## Overview
The intelligent cutoff system detects irrelevant queries and redirects students to focus on placement preparation using:
- **Relevance scoring** (0-100%) based on keyword analysis
- **Off-topic detection** across multiple categories
- **Personalized redirects** based on student performance
- **Study suggestions** to guide students back to learning

## Files Created

### 1. `intelligent_cutoff.py`
Core intelligent cutoff system with:
- `calculate_relevance_score()` - Scores queries 0-100%
- `is_off_topic()` - Detects irrelevant queries (threshold: 30%)
- `generate_redirect_message()` - Personalized motivational redirects
- `get_study_suggestions()` - Context-aware study recommendations

### 2. `context_handler_enhanced.py`
Enhanced context handler that integrates intelligent cutoff:
- Checks relevance before processing
- Returns redirect messages for off-topic queries
- Maintains all existing functionality
- Adds relevance scores to all responses

## Implementation Steps

### Option 1: Replace Existing File (Recommended)
```bash
# Backup original
copy context_handler.py context_handler_backup.py

# Replace with enhanced version
copy context_handler_enhanced.py context_handler.py
```

### Option 2: Manual Integration
Add to `context_handler.py`:

1. **Import the intelligent cutoff module** (line 7):
```python
from intelligent_cutoff import IntelligentCutoff
```

2. **Initialize in __init__** (line 13):
```python
def __init__(self, openrouter_client):
    self.openrouter_client = openrouter_client
    self.intelligent_cutoff = IntelligentCutoff()
```

3. **Add cutoff check in process_query** (after line 21):
```python
# INTELLIGENT CUTOFF: Check if query is off-topic
is_off_topic, category, relevance_score = self.intelligent_cutoff.is_off_topic(query)

if is_off_topic:
    logger.warning(f"Off-topic query detected: category={category}, relevance={relevance_score}%")
    
    # Generate personalized redirect message
    redirect_message = self.intelligent_cutoff.generate_redirect_message(
        query, category, student_context
    )
    
    # Get study suggestions
    suggestions = self.intelligent_cutoff.get_study_suggestions(student_context)
    
    return (
        redirect_message,
        {
            'off_topic': True,
            'category': category,
            'relevance_score': relevance_score,
            'suggestions': suggestions
        },
        'off_topic',
        'intelligent_cutoff'
    )
```

## How It Works

### Relevance Scoring
```
Score = 50 (base)
  + (High relevance keywords × 30)    # assessment, test, placement, etc.
  + (Medium relevance keywords × 15)  # help, guide, question, etc.
  - (Low relevance keywords × 20)     # game, movie, party, etc.
  + (Has question mark × 5)
  - (Short query with no keywords × 10)
```

**Cutoff Threshold: 30%**
- Queries below 30% are considered off-topic
- Triggers personalized redirect response

### Off-Topic Categories
1. **Entertainment**: games, movies, music, social media
2. **Personal**: relationships, dating, romance
3. **Sports**: cricket, football, tournaments
4. **Random**: weather, food, travel, shopping
5. **Casual Chat**: bored, fun, jokes, hanging out

### Personalized Redirects
Based on student performance level:

**Beginner** (0 assessments):
> "Hey {name}! I know you're curious about other things, but let's focus on getting started with your placement prep! 🚀 You have {count} assessments waiting for you. Let's tackle your first one together!"

**Needs Improvement** (<60% average):
> "Hi {name}, I understand you have other interests, but your placement prep needs attention right now! 📚 Your current average is {score}% - let's work on improving that together!"

**Good** (60-80% average):
> "Hey {name}! You're doing well at {score}%, but let's keep that momentum going! 💪 Ready to tackle the next challenge?"

**Excellent** (>80% average):
> "Impressive work, {name}! You're at {score}% - that's fantastic! 🌟 Challenge yourself with the remaining assessments. Keep pushing!"

## Testing

### Test Queries (Should Trigger Cutoff)
```python
# Entertainment
"What's the best game to play?"
"Have you seen the latest movie?"
"Which Netflix series should I watch?"

# Personal
"How do I get a girlfriend?"
"I'm feeling lonely"

# Sports
"Who won the cricket match?"
"Tell me about IPL"

# Random
"What's the weather like?"
"I'm bored, tell me a joke"

# Low relevance
"random chat"
"just talking"
```

### Test Queries (Should NOT Trigger Cutoff)
```python
# High relevance
"Show me available assessments"
"What's my test score?"
"How do I prepare for placement?"
"Help me improve my coding skills"

# Medium relevance
"How do I take a test?"
"What is the passing score?"
"Can you explain this topic?"
```

## Expected Results

### Off-Topic Query Response
```json
{
  "response": "Hey John! I know you're curious about games, but let's focus on getting started with your placement prep! 🚀 You have 3 assessments waiting for you. Let's tackle your first one together!",
  "data": {
    "off_topic": true,
    "category": "entertainment",
    "relevance_score": 15,
    "suggestions": [
      "📝 Take an available assessment",
      "🚀 Start your first assessment",
      "📚 Check study materials",
      "🎯 Set learning goals"
    ]
  },
  "query_type": "off_topic",
  "model_used": "intelligent_cutoff"
}
```

### Relevant Query Response
```json
{
  "response": "You have 3 assessments available: ...",
  "data": {
    "relevance_score": 85
  },
  "query_type": "assessments",
  "model_used": "deepseek/deepseek-chat"
}
```

## Configuration

### Adjust Cutoff Threshold
In `intelligent_cutoff.py`, modify the threshold:
```python
def is_off_topic(self, query: str, relevance_threshold: int = 30):
    # Lower threshold = stricter (more queries blocked)
    # Higher threshold = lenient (fewer queries blocked)
```

**Recommended thresholds:**
- **Strict**: 40% (blocks more casual queries)
- **Balanced**: 30% (default, good balance)
- **Lenient**: 20% (only blocks obvious off-topic)

### Customize Keywords
Edit keyword lists in `intelligent_cutoff.py`:
- `high_relevance` - Add placement-related terms
- `medium_relevance` - Add general inquiry terms
- `low_relevance` - Add distraction terms
- `off_topic_keywords` - Add category-specific terms

## Benefits

1. **Keeps Students Focused**: Redirects distractions to learning
2. **Personalized Motivation**: Uses student data for relevant messages
3. **Non-Intrusive**: Friendly, encouraging tone (not preachy)
4. **Actionable**: Provides specific next steps
5. **Intelligent**: Uses scoring algorithm, not just keywords
6. **Logging**: Tracks relevance scores for analytics

## Monitoring

Check logs for cutoff triggers:
```
Query relevance score: 15% (H:0, M:0, L:2)
LOW RELEVANCE (15%) - Triggering intelligent cutoff
Off-topic detected: entertainment
```

## Rollback

If issues occur, restore original:
```bash
copy context_handler_backup.py context_handler.py
```

## Next Steps

1. ✅ Test with various off-topic queries
2. ✅ Monitor relevance scores in logs
3. ✅ Adjust threshold if needed
4. ✅ Customize redirect messages
5. ✅ Add more keywords as patterns emerge
6. ✅ Track student engagement metrics

---

**Note**: The intelligent cutoff is designed to be helpful, not restrictive. It encourages focus while maintaining a supportive, motivational tone.
