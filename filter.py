import json
import requests

# 1. 定义源文件地址 (217heidai 的 JSON 格式规则集)
SOURCE_URL = "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblocksingbox.json"

# 2. 定义你关心的关键字（只有包含这些词的规则会被保留）
KEYWORDS = ["youtube", "twitter", "instagram", "google", "telegram", "pinterest", "chatgpt", "openai", "tumblr",  "quora", "reddit"]

def main():
    response = requests.get(SOURCE_URL)
    data = response.json()
    
    new_rules = []
    # 假设 sing-box 规则结构在 data['rules'][0]['domain'] 或 'domain_suffix' 中
    # 这里根据 217heidai 的标准结构进行提取
    for rule in data.get('rules', []):
        matched = False
        # 检查 domain, domain_suffix 等字段是否包含关键字
        for key in ['domain', 'domain_suffix', 'domain_keyword']:
            values = rule.get(key, [])
            filtered_values = [v for v in values if any(k in v.lower() for k in KEYWORDS)]
            if filtered_values:
                rule[key] = filtered_values
                matched = True
        
        if matched:
            new_rules.append(rule)

    # 重新构建精简后的 sing-box rule-set json
    output = {
        "version": 1,
        "rules": new_rules
    }
    
    with open('lite-ads.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
