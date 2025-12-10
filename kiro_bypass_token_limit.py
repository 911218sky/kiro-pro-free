"""
Kiro Token Limit Bypass
Adapted from Cursor Free VIP project
Modifies workbench.desktop.main.js to bypass token limits
"""
import os
import shutil
import tempfile
from colorama import Fore, Style, init
from datetime import datetime
from kiro_config import get_kiro_paths, get_kiro_config

init()

EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "WARNING": "⚠️",
}

def backup_file(file_path):
    """Create timestamped backup of file"""
    if not os.path.exists(file_path):
        print(f"{Fore.RED}{EMOJI['ERROR']} File not found: {file_path}{Style.RESET_ALL}")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Backup created: {backup_path}{Style.RESET_ALL}")
        return backup_path
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Backup failed: {e}{Style.RESET_ALL}")
        return None

def analyze_workbench_js(file_path):
    """Analyze workbench.desktop.main.js to find potential modification points"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        print(f"{Fore.CYAN}{EMOJI['INFO']} Analyzing Kiro workbench file...{Style.RESET_ALL}")
        
        # Look for potential token limit functions
        token_patterns = [
            "TokenLimit", "tokenLimit", "getEffectiveTokenLimit", "getTokenLimit",
            "2e5", "200000", "maxTokens", "tokenCount", "limitTokens"
        ]
        
        # Look for UI elements
        ui_patterns = [
            "Upgrade to Pro", "Pro Trial", "upgrade", "trial", "subscription",
            "pay", "billing", "premium"
        ]
        
        found_patterns = {"token": [], "ui": []}
        
        for pattern in token_patterns:
            if pattern in content:
                # Find context around the pattern
                index = content.find(pattern)
                start = max(0, index - 100)
                end = min(len(content), index + 100)
                context = content[start:end].replace('\n', ' ')
                found_patterns["token"].append((pattern, context))
        
        for pattern in ui_patterns:
            if pattern in content:
                index = content.find(pattern)
                start = max(0, index - 50)
                end = min(len(content), index + 50)
                context = content[start:end].replace('\n', ' ')
                found_patterns["ui"].append((pattern, context))
        
        return found_patterns
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Analysis failed: {e}{Style.RESET_ALL}")
        return None

def modify_workbench_js(file_path):
    """Modify workbench.desktop.main.js to bypass token limits"""
    try:
        # First analyze the file
        analysis = analyze_workbench_js(file_path)
        if analysis:
            print(f"\n{Fore.CYAN}Analysis Results:{Style.RESET_ALL}")
            if analysis["token"]:
                print(f"{Fore.GREEN}Found {len(analysis['token'])} potential token-related patterns:{Style.RESET_ALL}")
                for pattern, context in analysis["token"][:3]:  # Show first 3
                    print(f"  • {pattern}: ...{context[:60]}...")
            else:
                print(f"{Fore.YELLOW}No token-related patterns found{Style.RESET_ALL}")
            
            if analysis["ui"]:
                print(f"{Fore.GREEN}Found {len(analysis['ui'])} potential UI patterns:{Style.RESET_ALL}")
                for pattern, context in analysis["ui"][:3]:  # Show first 3
                    print(f"  • {pattern}: ...{context[:60]}...")
            else:
                print(f"{Fore.YELLOW}No UI patterns found{Style.RESET_ALL}")
        
        # Save original file permissions
        original_stat = os.stat(file_path)
        original_mode = original_stat.st_mode
        original_uid = original_stat.st_uid
        original_gid = original_stat.st_gid

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", errors="ignore", delete=False) as tmp_file:
            # Read original content
            with open(file_path, "r", encoding="utf-8", errors="ignore") as main_file:
                content = main_file.read()

            # Define replacement patterns (original Cursor patterns)
            cursor_patterns = {
                # Token limit bypass - increase from 200k to 9M
                r'async getEffectiveTokenLimit(e){const n=e.modelName;if(!n)return 2e5;': 
                    r'async getEffectiveTokenLimit(e){return 9000000;const n=e.modelName;if(!n)return 9e5;',
                
                # UI modifications - change upgrade buttons
                r'B(k,D(Ln,{title:"Upgrade to Pro",size:"small",get codicon(){return A.rocket},get onClick(){return t.pay}}),null)': 
                    r'B(k,D(Ln,{title:"Kiro Bypass Active",size:"small",get codicon(){return A.github},get onClick(){return function(){window.open("https://github.com/yeongpin/cursor-free-vip","_blank")}}}),null)',
                
                r'M(x,I(as,{title:"Upgrade to Pro",size:"small",get codicon(){return $.rocket},get onClick(){return t.pay}}),null)': 
                    r'M(x,I(as,{title:"Kiro Bypass Active",size:"small",get codicon(){return $.github},get onClick(){return function(){window.open("https://github.com/yeongpin/cursor-free-vip","_blank")}}}),null)',
                
                r'$(k,E(Ks,{title:"Upgrade to Pro",size:"small",get codicon(){return F.rocket},get onClick(){return t.pay}}),null)': 
                    r'$(k,E(Ks,{title:"Kiro Bypass Active",size:"small",get codicon(){return F.rocket},get onClick(){return function(){window.open("https://github.com/yeongpin/cursor-free-vip","_blank")}}}),null)',
                
                # Badge replacement
                r'<div>Pro Trial': r'<div>Pro',
                
                # Auto-select text replacement
                r'py-1">Auto-select': r'py-1">Bypass-Active',
                
                # Pro status display
                r'var DWr=ne("<div class=settings__item_description>You are currently signed in with <strong></strong>.");': 
                    r'var DWr=ne("<div class=settings__item_description>You are currently signed in with <strong></strong>. <h1>Pro (Bypassed)</h1>");',
                
                # Hide notification toasts
                r'notifications-toasts': r'notifications-toasts hidden'
            }
            
            # Try additional Kiro-specific patterns based on analysis
            kiro_patterns = {}
            if analysis and analysis["token"]:
                # Add dynamic patterns based on what we found
                for pattern, context in analysis["token"]:
                    if "2e5" in context or "200000" in context:
                        # Try to create a more flexible pattern
                        if "return 2e5" in context:
                            kiro_patterns[context.strip()] = context.replace("2e5", "9000000").strip()
            
            # Combine patterns
            all_patterns = {**cursor_patterns, **kiro_patterns}

            # Apply all replacements
            modifications_made = 0
            applied_patterns = []
            
            print(f"\n{Fore.CYAN}Attempting to apply {len(all_patterns)} patterns...{Style.RESET_ALL}")
            
            for old_pattern, new_pattern in all_patterns.items():
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    modifications_made += 1
                    applied_patterns.append(old_pattern[:50] + "...")
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Applied: {old_pattern[:50]}...{Style.RESET_ALL}")

            if modifications_made == 0:
                print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} No patterns matched in Kiro's code.{Style.RESET_ALL}")
                print(f"{Fore.CYAN}This is expected - Kiro uses different code patterns than Cursor.{Style.RESET_ALL}")
                
                if analysis and (analysis["token"] or analysis["ui"]):
                    print(f"\n{Fore.CYAN}However, we found potential modification points:{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}To make this work, we need to identify Kiro-specific patterns.{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Consider contributing patterns at: https://github.com/iamaanahmad/kiro-pro-free{Style.RESET_ALL}")
                
                return False

            # Write to temporary file
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Backup original file
        backup_path = backup_file(file_path)
        if not backup_path:
            print(f"{Fore.RED}{EMOJI['ERROR']} Cannot proceed without backup{Style.RESET_ALL}")
            os.unlink(tmp_path)
            return False
        
        # Move temporary file to original position
        if os.path.exists(file_path):
            os.remove(file_path)
        shutil.move(tmp_path, file_path)

        # Restore original permissions
        os.chmod(file_path, original_mode)
        if os.name != "nt":  # Not Windows
            try:
                os.chown(file_path, original_uid, original_gid)
            except:
                pass

        print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} File modified successfully ({modifications_made} patterns applied){Style.RESET_ALL}")
        if applied_patterns:
            print(f"{Fore.CYAN}Applied patterns:{Style.RESET_ALL}")
            for pattern in applied_patterns:
                print(f"  • {pattern}")
        return True

    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Modification failed: {e}{Style.RESET_ALL}")
        if "tmp_path" in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        return False

def discover_patterns(file_path):
    """Interactive pattern discovery mode"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} Pattern Discovery Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}This mode helps identify potential modification points in Kiro's code.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}The analysis will search for common patterns and show you what was found.{Style.RESET_ALL}\n")
    
    analysis = analyze_workbench_js(file_path)
    if not analysis:
        return False
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Detailed Analysis Results:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    if analysis["token"]:
        print(f"{Fore.GREEN}Token-related patterns found:{Style.RESET_ALL}")
        for i, (pattern, context) in enumerate(analysis["token"], 1):
            print(f"\n{Fore.YELLOW}{i}. Pattern: {pattern}{Style.RESET_ALL}")
            print(f"   Context: {context}")
    else:
        print(f"{Fore.RED}No token-related patterns found.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}This suggests Kiro uses very different token management than Cursor.{Style.RESET_ALL}")
    
    if analysis["ui"]:
        print(f"\n{Fore.GREEN}UI-related patterns found:{Style.RESET_ALL}")
        for i, (pattern, context) in enumerate(analysis["ui"], 1):
            print(f"\n{Fore.YELLOW}{i}. Pattern: {pattern}{Style.RESET_ALL}")
            print(f"   Context: {context}")
    else:
        print(f"\n{Fore.RED}No UI-related patterns found.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}What this means:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if not analysis["token"] and not analysis["ui"]:
        print(f"{Fore.YELLOW}• Kiro's code structure is significantly different from Cursor{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}• The token bypass feature likely won't work without new patterns{Style.RESET_ALL}")
        print(f"{Fore.CYAN}• Machine ID reset and auto-update disable should still work{Style.RESET_ALL}")
    elif analysis["token"] or analysis["ui"]:
        print(f"{Fore.GREEN}• Some relevant patterns were found{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}• Manual analysis needed to create working modifications{Style.RESET_ALL}")
        print(f"{Fore.CYAN}• Consider contributing findings to the project{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}To contribute patterns:{Style.RESET_ALL}")
    print(f"1. Analyze the contexts shown above")
    print(f"2. Identify the exact modification needed")
    print(f"3. Test the modification manually")
    print(f"4. Share working patterns with the community")
    
    return True

def run():
    """Main execution function"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['RESET']} Kiro Token Limit Bypass{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Get Kiro paths
    paths = get_kiro_paths()
    workbench_path = paths['workbench_js_path']
    
    # Verify file exists
    if not os.path.exists(workbench_path):
        print(f"{Fore.RED}{EMOJI['ERROR']} Workbench file not found: {workbench_path}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Please ensure Kiro is properly installed{Style.RESET_ALL}")
        input(f"\n{EMOJI['INFO']} Press Enter to exit...")
        return False
    
    print(f"{Fore.CYAN}{EMOJI['INFO']} Target file: {workbench_path}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{EMOJI['WARNING']} Note: This feature has limited compatibility with Kiro 0.5.9{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} Kiro uses different code patterns than Cursor IDE{Style.RESET_ALL}\n")
    
    # Show options
    print(f"{Fore.CYAN}Available options:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1{Style.RESET_ALL}. Try token bypass (may not work)")
    print(f"{Fore.GREEN}2{Style.RESET_ALL}. Pattern discovery mode (recommended)")
    print(f"{Fore.GREEN}0{Style.RESET_ALL}. Cancel")
    
    choice = input(f"\n{EMOJI['INFO']} Select option (0-2): ").strip()
    
    if choice == "0":
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Operation cancelled{Style.RESET_ALL}")
        return False
    elif choice == "2":
        return discover_patterns(workbench_path)
    elif choice != "1":
        print(f"{Fore.RED}{EMOJI['ERROR']} Invalid choice{Style.RESET_ALL}")
        return False
    
    # Continue with bypass attempt
    print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} This will modify Kiro's core files{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{EMOJI['WARNING']} A backup will be created automatically{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} Based on analysis, this may not work with current Kiro version{Style.RESET_ALL}\n")
    
    # Confirm action
    response = input(f"{EMOJI['INFO']} Continue anyway? (y/N): ").strip().lower()
    if response != 'y':
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Operation cancelled{Style.RESET_ALL}")
        return False
    
    # Perform modification
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} Analyzing and modifying workbench file...{Style.RESET_ALL}\n")
    success = modify_workbench_js(workbench_path)
    
    if success:
        print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} Token limit bypass applied successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['INFO']} Please restart Kiro for changes to take effect{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} Token limit bypass could not be applied{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['INFO']} This is expected with Kiro 0.5.9 - try pattern discovery mode{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} Press Enter to continue...")
    return success

if __name__ == "__main__":
    run()
