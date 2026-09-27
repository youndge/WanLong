import os
import re
import csv
from PIL import Image
import pytesseract

# ========== 配置区，自己改 ==========
IMAGE_FOLDER = "./screenshots"  # 存放100张截图的文件夹
OUTPUT_CSV = "./result.csv"     # 输出结果文件
# 匹配连续17位数字
PATTERN = re.compile(r"\d{17}")

def extract_17digits(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    all_matches = PATTERN.findall(text)
    if len(all_matches) >=2:
        # 第2个17位数字 = 二维码下方那串（第一张是券码）
        return all_matches[1]
    elif len(all_matches) ==1:
        return all_matches[0]
    else:
        return None

def main():
    results = []
    for fname in os.listdir(IMAGE_FOLDER):
        if fname.lower().endswith((".png",".jpg",".jpeg")):
            fpath = os.path.join(IMAGE_FOLDER, fname)
            num = extract_17digits(fpath)
            print(f"{fname} -> {num}")
            results.append([fname, num])
    # 写入csv
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["文件名","17位数字"])
        writer.writerows(results)
    print(f"完成！结果保存到 {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
