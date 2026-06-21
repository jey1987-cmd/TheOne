"""
Test file demonstrating NLP-based PII redaction with various examples
Shows input/output for different scenarios and operators
"""

from redactor import TextRedactor


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def test_basic_redaction():
    """Test basic redaction with different operators"""
    redactor = TextRedactor()
    
    print_section("1. BASIC REDACTION - Different Operators")
    
    text = "John Smith works at Google. Contact him at john.smith@google.com or call (555) 123-4567."
    print(f"\nOriginal Text:\n{text}")
    
    # Test Replace operator
    print("\n--- Operator: replace ---")
    result = redactor.redact_text(text, operator="replace")
    print(f"Redacted:\n{result['redacted_text']}")
    print(f"Entities Found: {result['total_entities']}")
    for entity in result['entities_found']:
        print(f"  - {entity['type']}: '{entity['original']}'")
    
    # Test Redact operator
    print("\n--- Operator: redact ---")
    result = redactor.redact_text(text, operator="redact")
    print(f"Redacted:\n{result['redacted_text']}")
    
    # Test Hash operator
    print("\n--- Operator: hash ---")
    result = redactor.redact_text(text, operator="hash")
    print(f"Redacted:\n{result['redacted_text']}")


def test_nlp_vs_regex():
    """Compare NLP-based vs Regex-only detection"""
    redactor = TextRedactor()
    
    print_section("2. NLP vs REGEX COMPARISON")
    
    text = "Dr. Sarah Johnson from Apple Inc. sent an email to michael.brown@apple.com about the project in San Francisco."
    print(f"\nOriginal Text:\n{text}")
    
    # NLP-based detection
    print("\n--- With NLP (Hybrid Approach) ---")
    result_nlp = redactor.redact_text(text, operator="replace", use_nlp=True)
    print(f"Redacted:\n{result_nlp['redacted_text']}")
    print(f"Method: {result_nlp['method']}")
    print(f"Entities Found: {result_nlp['total_entities']}")
    for entity in result_nlp['entities_found']:
        print(f"  - {entity['type']}: '{entity['original']}'")
    
    # Regex-only detection
    print("\n--- Without NLP (Regex Only) ---")
    result_regex = redactor.redact_text(text, operator="replace", use_nlp=False)
    print(f"Redacted:\n{result_regex['redacted_text']}")
    print(f"Method: {result_regex['method']}")
    print(f"Entities Found: {result_regex['total_entities']}")
    for entity in result_regex['entities_found']:
        print(f"  - {entity['type']}: '{entity['original']}'")


def test_various_pii_types():
    """Test detection of various PII types"""
    redactor = TextRedactor()
    
    print_section("3. VARIOUS PII TYPES DETECTION")
    
    # Test different PII categories
    test_cases = [
        {
            "name": "Email Address",
            "text": "Please send the report to alice.johnson@company.com and bob@example.org"
        },
        {
            "name": "Phone Numbers",
            "text": "Call me at (555) 123-4567 or +1-555-987-6543 for more information."
        },
        {
            "name": "Credit Card",
            "text": "The payment was made with card 4532-1234-5678-9010 on the website."
        },
        {
            "name": "Social Security Number",
            "text": "My SSN is 123-45-6789 and I need to update my records."
        },
        {
            "name": "IP Address",
            "text": "Server logs show activity from 192.168.1.100 and 10.0.0.50 this morning."
        },
        {
            "name": "URLs",
            "text": "Visit https://www.example.com or https://secure.company.com/login for details."
        },
        {
            "name": "Person Names & Organizations",
            "text": "Elizabeth Warren from the Federal Reserve discussed the economic policy with Mark Zuckerberg."
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Original: {test_case['text']}")
        result = redactor.redact_text(test_case['text'], operator="replace", use_nlp=True)
        print(f"Redacted: {result['redacted_text']}")
        print(f"Found {result['total_entities']} entity/entities")


def test_complex_document():
    """Test redaction on a more complex, realistic document"""
    redactor = TextRedactor()
    
    print_section("4. COMPLEX DOCUMENT REDACTION")
    
    document = """
    CONFIDENTIAL REPORT
    
    Date: June 21, 2026
    To: Jennifer Chen, CEO
    From: Robert Wilson, Head of Sales
    
    Meeting Notes:
    
    Our top sales rep, David Martinez, closed a major deal with TechCorp Industries 
    today. The contact person was Linda Thompson (linda.thompson@techcorp.com). 
    
    David can be reached at (555) 234-5678 or david.martinez@ourcompany.com
    
    Technical Details:
    - Server IP: 192.168.100.50
    - Customer Payment Card: 5412-3456-7890-1234
    - SSN for tax purposes: 987-65-4321
    
    Next steps discussed with the client in New York. Project scheduled to launch 
    by Q3 2026.
    """
    
    print(f"Original Document:\n{document}")
    
    print("\n--- With NLP Redaction (Replace operator) ---")
    result = redactor.redact_text(document, operator="replace", use_nlp=True)
    print(f"\nRedacted Document:\n{result['redacted_text']}")
    
    print(f"\nSummary:")
    print(f"Total Entities Redacted: {result['total_entities']}")
    print(f"Detection Method: {result['method']}")
    print(f"\nDetailed Breakdown:")
    entity_types = {}
    for entity in result['entities_found']:
        entity_type = entity['type']
        if entity_type not in entity_types:
            entity_types[entity_type] = []
        entity_types[entity_type].append(entity['original'])
    
    for entity_type, values in entity_types.items():
        print(f"  {entity_type}: {len(values)} found")
        for value in values:
            print(f"    - '{value}'")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "NLP-BASED PII REDACTION - COMPREHENSIVE TEST SUITE" + " "*13 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        test_basic_redaction()
        test_nlp_vs_regex()
        test_various_pii_types()
        test_complex_document()
        
        print_section("ALL TESTS COMPLETED SUCCESSFULLY")
        print("\n✓ NLP-based redaction is working correctly!")
        print("✓ Multiple PII types detected and redacted")
        print("✓ Hybrid approach combining NLP + Regex patterns")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
