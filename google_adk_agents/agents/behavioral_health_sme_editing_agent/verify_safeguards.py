#!/usr/bin/env python3
"""
Quick Safeguard Verification for Deployment
"""

from implementation_advanced import validate_no_internal_metrics

def test_safeguards():
    print("🚨 TESTING METRIC LEAKAGE SAFEGUARDS:")
    print("=" * 50)
    
    # Test 1: Contaminated content (should be blocked)
    try:
        validate_no_internal_metrics('The compliance score improved significantly.')
        print("❌ FAILED: Should have blocked contaminated content!")
        return False
    except ValueError:
        print("✅ PASSED: Correctly blocked contaminated content")
    
    # Test 2: Clean content (should pass through)
    try:
        validate_no_internal_metrics('The primary cornerstone ensures quality care.')
        print("✅ PASSED: Clean content allowed through")
    except ValueError as e:
        print(f"❌ FAILED: Clean content was blocked: {e}")
        return False
    
    print("\n🛡️ ALL SAFEGUARDS OPERATIONAL!")
    return True

if __name__ == "__main__":
    test_safeguards() 