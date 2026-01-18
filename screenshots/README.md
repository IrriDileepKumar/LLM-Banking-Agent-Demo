# Screenshots Directory

This directory contains screenshots demonstrating the LLM Banking Agent Demo's functionality and security features.

## 📸 Screenshot Checklist

### Basic Functionality
- [ ] `test1_vulnerable_basic.png` - Vulnerable version showing normal transaction display
- [ ] `test2_secure_basic.png` - Secure version showing normal transaction display with security notice
- [ ] `app_overview.png` - Application overview showing UI
- [ ] `user_switching.png` - User switching feature demonstration

### Attack Demonstrations - Vulnerable Version
- [ ] `test3_vulnerable_prompt_injection.png` - Prompt injection attack attempt
- [ ] `test4_vulnerable_sql_injection_basic.png` - Basic SQL injection attempt
- [ ] `test5_vulnerable_advanced_sql_injection.png` - Advanced SQL injection with social engineering

### Security Features - Secure Version
- [ ] `test3_secure_prompt_injection_blocked.png` - Prompt injection blocked
- [ ] `test4_secure_sql_injection_blocked.png` - SQL injection blocked at tool level
- [ ] `test5_secure_advanced_sql_blocked.png` - Advanced attack blocked with multi-layer defense

### Testing Results
- [ ] `test_automated_results.png` - Automated test suite results
- [ ] `sql_injection_detection.png` - SQL injection detection in action

## 📝 Instructions for Taking Screenshots

1. **Start both versions** of the application:
   ```bash
   # Terminal 1 - Vulnerable version
   source env/bin/activate && python -m streamlit run main.py --server.port 8501
   
   # Terminal 2 - Secure version
   source env/bin/activate && python -m streamlit run main_secure.py --server.port 8502
   ```

2. **Use the test payloads** from [QUICK_START.md](../QUICK_START.md)

3. **Capture screenshots** showing:
   - The input prompt
   - The LLM's response
   - Any error messages or security alerts
   - Transaction data (if displayed)

4. **Save screenshots** with descriptive names matching the checklist above

5. **Optimize images**:
   - Use PNG format for clarity
   - Crop to show relevant content
   - Keep file sizes reasonable (< 500KB each)

## 🎯 Screenshot Guidelines

### What to Include
- ✅ Full chat interface showing the conversation
- ✅ User input and LLM response
- ✅ Security alerts or error messages
- ✅ Transaction data or results
- ✅ User switcher showing current user

### What to Avoid
- ❌ Personal information or real API keys
- ❌ Unnecessary browser chrome or desktop elements
- ❌ Blurry or low-quality images
- ❌ Screenshots with sensitive data

## 📊 Example Screenshot Layout

```
┌─────────────────────────────────────────┐
│  🏦 Bank LLM Agent    👤 MartyMcFly     │
├─────────────────────────────────────────┤
│                                         │
│  User: [Attack payload here]            │
│                                         │
│  Assistant: [Response/Alert here]       │
│                                         │
│  [Transaction data or error message]    │
│                                         │
└─────────────────────────────────────────┘
```

---

**Note**: Screenshots will be referenced in the main README.md and TESTING_GUIDE.md
