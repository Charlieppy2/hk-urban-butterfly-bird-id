"""
分批上傳圖片文件到 Git LFS
每5個物種目錄為一批
"""

import os
import subprocess
import sys

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_image_files_in_dir(directory):
    """獲取目錄中的所有圖片文件"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    files = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                files.append(os.path.join(directory, file))
    return files

def upload_images_in_batches(batch_size=5):
    """分批上傳圖片到 Git LFS"""
    raw_dir = os.path.join('data', 'raw')
    
    if not os.path.exists(raw_dir):
        print(f"❌ 目錄不存在: {raw_dir}")
        return
    
    # 獲取所有物種目錄
    species_dirs = []
    for item in os.listdir(raw_dir):
        item_path = os.path.join(raw_dir, item)
        if os.path.isdir(item_path):
            species_dirs.append(item)
    
    species_dirs.sort()
    total_species = len(species_dirs)
    
    print(f"找到 {total_species} 個物種目錄")
    print(f"將分為 {((total_species + batch_size - 1) // batch_size)} 批上傳，每批 {batch_size} 個物種\n")
    
    # 分批處理
    for batch_num in range(0, total_species, batch_size):
        batch = species_dirs[batch_num:batch_num + batch_size]
        batch_num_display = (batch_num // batch_size) + 1
        total_batches = (total_species + batch_size - 1) // batch_size
        
        print(f"\n{'='*60}")
        print(f"批次 {batch_num_display}/{total_batches}: 處理物種 {batch_num + 1}-{min(batch_num + batch_size, total_species)}")
        print(f"{'='*60}")
        
        # 收集這批的所有圖片文件
        image_files = []
        for species_dir in batch:
            species_path = os.path.join(raw_dir, species_dir)
            files = get_image_files_in_dir(species_path)
            image_files.extend(files)
            print(f"  {species_dir}: {len(files)} 個圖片文件")
        
        if not image_files:
            print(f"  ⚠️ 批次 {batch_num_display} 沒有圖片文件，跳過")
            continue
        
        print(f"\n  總共 {len(image_files)} 個圖片文件需要上傳")
        
        # 使用 git add 添加文件（Git LFS 會自動處理）
        try:
            for img_file in image_files:
                # 使用相對路徑
                rel_path = os.path.relpath(img_file, os.getcwd())
                result = subprocess.run(
                    ['git', 'add', rel_path],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                if result.returncode != 0:
                    print(f"  ⚠️ 添加文件失敗: {rel_path}")
                    print(f"     錯誤: {result.stderr}")
                else:
                    print(f"  ✓ 已添加: {rel_path}")
            
            # 檢查是否有文件需要提交
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.stdout.strip():
                # 有文件需要提交
                commit_message = f"Add images batch {batch_num_display}/{total_batches}: {', '.join(batch)}"
                result = subprocess.run(
                    ['git', 'commit', '-m', commit_message],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    print(f"\n  ✅ 批次 {batch_num_display} 已提交")
                    print(f"  提交信息: {commit_message}")
                else:
                    print(f"\n  ⚠️ 提交失敗: {result.stderr}")
                    # 檢查是否是因為沒有變更
                    if "nothing to commit" in result.stderr.lower():
                        print(f"  ℹ️  沒有新文件需要提交（可能已經在 Git 中）")
                    else:
                        print(f"  請手動檢查錯誤")
            else:
                print(f"\n  ℹ️  批次 {batch_num_display} 沒有新文件需要提交（可能已經在 Git 中）")
            
        except Exception as e:
            print(f"  ❌ 處理批次 {batch_num_display} 時出錯: {e}")
            continue
        
        # 自動繼續，不需要用戶輸入
        print(f"\n  自動繼續下一批...")
    
    print(f"\n{'='*60}")
    print("✅ 所有批次處理完成！")
    print(f"{'='*60}")
    print("\n最後一步：推送到 GitHub")
    print("執行: git push origin main")
    print("注意：由於使用 Git LFS，推送可能需要較長時間")

if __name__ == '__main__':
    # 檢查 Git LFS 是否已安裝
    try:
        result = subprocess.run(['git', 'lfs', 'version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git LFS 未安裝或未配置")
            print("請先安裝 Git LFS: https://git-lfs.github.com/")
            sys.exit(1)
        print("✅ Git LFS 已安裝")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ Git 未找到，請確保 Git 已安裝")
        sys.exit(1)
    
    # 檢查是否在 Git 倉庫中
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True)
        if result.returncode != 0:
            print("❌ 當前目錄不是 Git 倉庫")
            sys.exit(1)
    except:
        print("❌ 無法檢查 Git 倉庫狀態")
        sys.exit(1)
    
    # 檢查 .gitattributes 是否已配置 Git LFS
    gitattributes_path = '.gitattributes'
    if os.path.exists(gitattributes_path):
        with open(gitattributes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'filter=lfs' in content and 'data/raw' in content:
                print("✅ .gitattributes 已配置 Git LFS")
            else:
                print("⚠️  .gitattributes 存在但可能未正確配置 Git LFS")
                print("   將更新 .gitattributes 文件...")
                update_gitattributes()
    else:
        print("⚠️  .gitattributes 不存在，將創建...")
        update_gitattributes()
    
    print("\n開始分批上傳圖片...\n")
    upload_images_in_batches(batch_size=5)

def update_gitattributes():
    """更新 .gitattributes 文件以支持 Git LFS"""
    gitattributes_path = '.gitattributes'
    
    # 讀取現有內容
    existing_content = ""
    if os.path.exists(gitattributes_path):
        with open(gitattributes_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 檢查是否已包含 data/raw 的 LFS 配置
    if 'data/raw' in existing_content and 'filter=lfs' in existing_content:
        print("  .gitattributes 已包含 data/raw 的 LFS 配置")
        return
    
    # 添加 LFS 配置
    lfs_config = "\n# Git LFS for species images\n"
    lfs_config += "data/raw/**/*.jpg filter=lfs diff=lfs merge=lfs -text\n"
    lfs_config += "data/raw/**/*.jpeg filter=lfs diff=lfs merge=lfs -text\n"
    lfs_config += "data/raw/**/*.png filter=lfs diff=lfs merge=lfs -text\n"
    lfs_config += "data/raw/**/*.gif filter=lfs diff=lfs merge=lfs -text\n"
    lfs_config += "data/raw/**/*.webp filter=lfs diff=lfs merge=lfs -text\n"
    
    with open(gitattributes_path, 'a', encoding='utf-8') as f:
        f.write(lfs_config)
    
    print("  ✅ 已更新 .gitattributes 文件")
    
    # 提交 .gitattributes 更改
    try:
        subprocess.run(['git', 'add', '.gitattributes'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Configure Git LFS for species images'], check=True)
        print("  ✅ 已提交 .gitattributes 更改")
    except:
        print("  ⚠️  無法自動提交 .gitattributes，請手動提交")

