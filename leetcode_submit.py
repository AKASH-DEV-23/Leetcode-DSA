#!/usr/bin/env python3
"""
LeetCode Daily Submitter - Submits a solution once per day
Based on actual network capture from LeetCode
"""

import requests
import os
import sys
import time
from datetime import datetime

# ============== CONFIGURATION ==============
# Get credentials from environment variables (for GitHub Actions)
# Or set them directly below for local testing
LEETCODE_SESSION = os.environ.get("LEETCODE_SESSION", "")
CSRF_TOKEN = os.environ.get("CSRF_TOKEN", "")

# Problem configuration
PROBLEM_SLUG = "two-sum"  # e.g., "two-sum", "add-two-numbers"
QUESTION_ID = "1"          # e.g., "1" for two-sum
LANGUAGE = "java"          # "java", "python3", "cpp", etc.

# Your solution code (copy exactly from LeetCode editor)
YOUR_SOLUTION = '''class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer,Integer> mp=new HashMap<>();
        for(int i=0;i<nums.length;i++){
            int diff=target-nums[i];
            if(mp.containsKey(diff)){
                return new int[]{mp.get(diff),i};
            }
            mp.put(nums[i],i);
        }
        return new int[]{0};
    }
}'''

# ============== SUBMIT FUNCTION ==============
def submit_solution():
    """Submit solution to LeetCode"""
    
    # Validate credentials
    if not LEETCODE_SESSION or not CSRF_TOKEN:
        print("❌ Error: Missing credentials!")
        print("Set LEETCODE_SESSION and CSRF_TOKEN environment variables")
        return False
    
    # Prepare headers exactly as browser sends them
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/146.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "x-csrftoken": CSRF_TOKEN,
        "Referer": f"https://leetcode.com/problems/{PROBLEM_SLUG}/",
        "Origin": "https://leetcode.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
    
    # Prepare cookies exactly as browser has them
    cookies = {
        "LEETCODE_SESSION": LEETCODE_SESSION,
        "csrftoken": CSRF_TOKEN,
    }
    
    # Prepare payload exactly as captured
    payload = {
        "lang": LANGUAGE,
        "question_id": QUESTION_ID,
        "typed_code": YOUR_SOLUTION
    }
    
    # Submit to LeetCode
    url = f"https://leetcode.com/problems/{PROBLEM_SLUG}/submit/"
    
    try:
        print(f"📤 Submitting solution for '{PROBLEM_SLUG}'...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            submission_id = result.get('submission_id')
            print(f"✅ Success! Submission ID: {submission_id}")
            print(f"🔗 https://leetcode.com/submissions/detail/{submission_id}/")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 LeetCode Daily Submitter")
    print("-" * 40)
    
    success = submit_solution()
    
    if success:
        print("\n✨ Daily submission completed!")
        sys.exit(0)
    else:
        print("\n💥 Submission failed!")
        sys.exit(1)
