"""
Data Redaction App using NLP-Based PII Detection
Detects and redacts Personally Identifiable Information (PII) from text using spaCy NER
"""

import re
import spacy


class TextRedactor:
    """
    A class to handle text redaction using NLP-based entity recognition with spaCy
    and pattern-based detection for structured PII
    """
    
    def __init__(self):
        """Initialize the redactor with spaCy model and regex patterns"""
        
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("spaCy model 'en_core_web_sm' not found. Please install it using: python -m spacy download en_core_web_sm")
        
        # Define regex patterns for structured PII that spaCy doesn't detect
        self.patterns = {
            "EMAIL_ADDRESS": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE_NUMBER": r'\b(?:\+?1[-.\s]?)?(?:\(?[0-9]{3}\)?[-.\s]?)?[0-9]{3}[-.\s]?[0-9]{4}\b',
            "CREDIT_CARD": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "US_SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "IP_ADDRESS": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            "URL": r'https?://(?:www\.)?[^\s/$.?#].[^\s]*'
        }
        
        # Map spaCy entity labels to PII types
        self.spacy_entity_map = {
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",
            "FAC": "FACILITY",
            "PRODUCT": "PRODUCT",
            "EVENT": "EVENT"
        }
    
    def _get_spacy_entities(self, text: str) -> list:
        """
        Extract entities using spaCy NER
        
        Args:
            text (str): Input text to process
        
        Returns:
            list: List of tuples (entity_type, start, end, text)
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            # Map spaCy entity labels to our PII categories
            entity_type = self.spacy_entity_map.get(ent.label_, ent.label_)
            entities.append((entity_type, ent.start_char, ent.end_char, ent.text))
        
        return entities
    
    def _get_pattern_entities(self, text: str) -> list:
        """
        Extract entities using regex patterns
        
        Args:
            text (str): Input text to process
        
        Returns:
            list: List of tuples (entity_type, start, end, text)
        """
        entities = []
        
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                entities.append((entity_type, match.start(), match.end(), match.group()))
        
        return entities
    
    def redact_text(self, text: str, operator: str = "replace", use_nlp: bool = True) -> dict:
        """
        Redact PII from the input text using NLP-based and pattern-based detection
        
        Args:
            text (str): The input text to redact
            operator (str): The redaction operator - "replace", "redact", or "hash"
                          - "replace": replaces with <ENTITY_TYPE>
                          - "redact": replaces with *
                          - "hash": replaces with hash value
            use_nlp (bool): Use spaCy NER for entity detection (default: True)
        
        Returns:
            dict: A dictionary containing:
                - "redacted_text": The redacted text
                - "entities_found": List of detected entities with their types and positions
                - "total_entities": Total number of entities found
        """
        try:
            # Collect entities from both spaCy NER and regex patterns
            all_matches = []
            
            # Get entities from spaCy NER if enabled
            if use_nlp:
                all_matches.extend(self._get_spacy_entities(text))
            
            # Get entities from regex patterns
            all_matches.extend(self._get_pattern_entities(text))
            
            # Remove duplicates and overlapping entities (keep the first occurrence)
            unique_matches = []
            seen_ranges = set()
            
            for entity_type, start, end, matched_text in sorted(all_matches, key=lambda x: (x[1], x[2])):
                # Check if this range overlaps with any existing range
                is_overlapping = False
                for seen_start, seen_end in seen_ranges:
                    if not (end <= seen_start or start >= seen_end):
                        is_overlapping = True
                        break
                
                if not is_overlapping:
                    unique_matches.append((entity_type, start, end, matched_text))
                    seen_ranges.add((start, end))
            
            if not unique_matches:
                return {
                    "redacted_text": text,
                    "entities_found": [],
                    "total_entities": 0,
                    "message": "No PII detected"
                }
            
            # Sort by position (reverse order to maintain correct positions during replacement)
            unique_matches.sort(key=lambda x: x[1], reverse=True)
            
            redacted_text = text
            results = []
            
            # Process matches in reverse order to maintain correct string positions
            for entity_type, start, end, matched_text in unique_matches:
                if operator == "replace":
                    replacement = f"<{entity_type}>"
                elif operator == "redact":
                    replacement = "*" * len(matched_text)
                elif operator == "hash":
                    replacement = f"<HASH:{hash(matched_text) % 10000000:07d}>"
                else:
                    replacement = f"<{entity_type}>"
                
                results.append({
                    "type": entity_type,
                    "start": start,
                    "end": end,
                    "original": matched_text
                })
                
                # Replace the matched text
                redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
            
            # Reverse results to maintain original order
            results.reverse()
            
            return {
                "redacted_text": redacted_text,
                "entities_found": results,
                "total_entities": len(results),
                "method": "NLP + Regex" if use_nlp else "Regex only"
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "redacted_text": None,
                "entities_found": [],
                "total_entities": 0
            }
    
    def get_supported_entities(self) -> list:
        """
        Get the list of supported PII entity types
        
        Returns:
            list: List of supported entity types
        """
        return list(self.patterns.keys())


def main():
    """Main function to demonstrate the redactor"""
    redactor = TextRedactor()
    
    # Example usage
    print("=== Data Redaction App ===\n")
    
    # Display supported entities
    print("Supported PII Entity Types:")
    entities = redactor.get_supported_entities()
    for i, entity in enumerate(entities, 1):
        print(f"  {i}. {entity}")
    print()
    
    # Example texts for redaction
    examples = [
        "My name is Jey and my phone number is 555-123-4567",
        "Contact me at john.doe@example.com or call me at (555) 987-6543",
        "My SSN is 123-45-6789 and I live in New York",
        "Visit our website at https://www.example.com for more info",
        "Hello, I'm Sarah Johnson from the marketing team"
    ]
    
    print("=== Redaction Examples ===\n")
    for i, example_text in enumerate(examples, 1):
        print(f"Example {i}:")
        print(f"Original:  {example_text}")
        
        result = redactor.redact_text(example_text, operator="replace")
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Redacted:  {result['redacted_text']}")
            if result['entities_found']:
                print(f"Entities Found: {result['total_entities']}")
                for entity in result['entities_found']:
                    print(f"  - {entity['type']}: {entity['original']}")
            else:
                print(f"No entities found")
        print()


if __name__ == "__main__":
    main()
