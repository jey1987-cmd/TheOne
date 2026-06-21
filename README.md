# NLP-Based PII Redaction System

A comprehensive data redaction solution using spaCy NER (Named Entity Recognition) combined with regex pattern matching for detecting and redacting Personally Identifiable Information (PII) from text.

## Overview

This project demonstrates an advanced approach to data redaction that goes beyond simple regex patterns. By leveraging spaCy's pre-trained NLP model (`en_core_web_sm`), the system can intelligently identify:

- **Person Names** - Named entities recognized by NLP model
- **Organizations** - Companies, institutions, organizations
- **Locations** - Geographic locations, cities, countries
- **Structured PII** - Email addresses, phone numbers, SSNs, credit cards, IP addresses, URLs

## Key Features

✨ **Hybrid Detection Approach**
- NLP-based entity recognition for context-aware PII detection
- Regex patterns for structured PII (email, phone, SSN, credit card, etc.)
- Automatic overlap detection and deduplication

🎯 **Multiple Redaction Operators**
- `replace`: Replaces with `<ENTITY_TYPE>` placeholder
- `redact`: Masks with asterisks
- `hash`: Replaces with hashed values for consistency

📊 **Rich Detection Results**
- Entity type classification
- Original text preservation
- Position tracking (start/end indices)
- Detailed entity breakdown

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd TheOne

# Install spaCy
pip install spacy

# Download the English language model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy model loaded successfully')"
```

## Project Structure

```
TheOne/
├── README.md
├── src/
│   ├── redactor.py          # Main TextRedactor class
│   └── test_redactor.py     # Comprehensive test suite
└── requirements.txt         # Project dependencies (optional)
```

## Usage

### Basic Usage

```python
from src.redactor import TextRedactor

# Initialize the redactor
redactor = TextRedactor()

# Redact PII from text
text = "John Smith works at Google. Contact: john.smith@google.com or (555) 123-4567"
result = redactor.redact_text(text, operator="replace")

print(result['redacted_text'])
# Output: <PERSON> works at <ORGANIZATION>. Contact: <EMAIL_ADDRESS> or (<CARDINAL>) <CARDINAL>-4567

print(f"Entities found: {result['total_entities']}")
```

### Different Redaction Operators

```python
# Replace with entity type
result = redactor.redact_text(text, operator="replace")
# Output: <PERSON> works at <ORGANIZATION>...

# Mask with asterisks
result = redactor.redact_text(text, operator="redact")
# Output: ********** works at ******...

# Hash-based redaction
result = redactor.redact_text(text, operator="hash")
# Output: <HASH:5582620> works at <HASH:9211655>...
```

### NLP vs Regex-Only Mode

```python
# Full hybrid approach (NLP + Regex)
result_nlp = redactor.redact_text(text, operator="replace", use_nlp=True)

# Regex patterns only (no NLP)
result_regex = redactor.redact_text(text, operator="replace", use_nlp=False)
```

## Running Tests

The project includes a comprehensive test suite demonstrating all features:

```bash
python src/test_redactor.py
```

### Test Scenarios

1. **Basic Redaction** - Tests all three operators (replace, redact, hash)
2. **NLP vs Regex** - Compares detection accuracy between approaches
3. **Various PII Types** - Tests emails, phones, SSNs, IPs, URLs, person names, organizations
4. **Complex Document** - Real-world confidential document redaction

## Performance Comparison: NLP vs Regex

| Text | Regex Only | NLP + Regex | Accuracy Gain |
|------|-----------|-----------|---|
| "Dr. Sarah Johnson from Apple Inc. sent an email to michael.brown@apple.com about the project in San Francisco." | 1 entity (email only) | 4 entities (name, org, email, location) | +300% |

## PII Types Detected

| PII Type | Detection Method | Example |
|----------|-----------------|---------|
| Person Names | NLP (spaCy NER) | John Smith, Dr. Sarah Johnson |
| Organizations | NLP (spaCy NER) | Google, Apple Inc., Federal Reserve |
| Locations | NLP (spaCy NER) | San Francisco, New York, USA |
| Email Addresses | Regex Pattern | john.smith@google.com |
| Phone Numbers | Regex Pattern | (555) 123-4567, +1-555-987-6543 |
| Credit Cards | Regex Pattern | 4532-1234-5678-9010 |
| Social Security Numbers | Regex Pattern | 123-45-6789 |
| IP Addresses | Regex Pattern | 192.168.1.100 |
| URLs | Regex Pattern | https://example.com |

## API Reference

### TextRedactor Class

#### `__init__()`
Initializes the redactor with spaCy model and regex patterns.

#### `redact_text(text: str, operator: str = "replace", use_nlp: bool = True) -> dict`

**Parameters:**
- `text` (str): Input text to redact
- `operator` (str): Redaction method - `"replace"`, `"redact"`, or `"hash"`
- `use_nlp` (bool): Enable NLP-based entity detection (default: True)

**Returns:**
```python
{
    "redacted_text": str,           # Redacted output text
    "entities_found": list,         # List of detected entities
    "total_entities": int,          # Count of redacted entities
    "method": str,                  # Detection method used
    "message": str                  # Status message (if no entities found)
}
```

**Entity Object:**
```python
{
    "type": str,          # Entity type (PERSON, ORGANIZATION, EMAIL_ADDRESS, etc.)
    "start": int,         # Start position in original text
    "end": int,           # End position in original text
    "original": str       # Original matched text
}
```

## Use Cases

- **Healthcare** - HIPAA compliance, patient record anonymization
- **Finance** - PCI-DSS compliance, customer data protection
- **Legal** - Sensitive document redaction
- **Data Science** - Creating anonymized datasets for analysis
- **Content Publishing** - Preparing data for public release
- **Data Migration** - Protecting PII during system transitions

## Advantages over Regex-Only Approach

1. **Context Awareness** - Understands context to reduce false positives
2. **Better Name Detection** - Catches person names in various contexts
3. **Organization Recognition** - Identifies company names accurately
4. **Location Awareness** - Detects geographic references
5. **Flexible** - Can toggle between NLP and regex-only modes
6. **Comprehensive** - Combines linguistic and pattern-based detection

## Limitations & Future Improvements

- NLP model size (en_core_web_sm ~40MB)
- Language limitation (currently English only)
- Processing speed for very large documents
- Custom PII patterns support (to be added)
- Support for additional spaCy models (en_core_web_md, en_core_web_lg)

## Dependencies

- `spacy>=3.0.0` - Natural Language Processing library
- Python 3.7+ - Required runtime

## Article Reference

This project is part of a Towards Data Science article demonstrating the advantages of NLP-based over regex-only PII redaction approaches.
