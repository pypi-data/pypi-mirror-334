import re
from typing import Dict, Any, Tuple
import os

from yaspin import yaspin

from jarvis.jarvis_agent.output_handler import OutputHandler
from jarvis.jarvis_platform.registry import PlatformRegistry
from jarvis.jarvis_tools.git_commiter import GitCommitTool
from jarvis.jarvis_tools.execute_shell_script import ShellScriptTool
from jarvis.jarvis_tools.file_operation import FileOperationTool
from jarvis.jarvis_tools.read_code import ReadCodeTool
from jarvis.jarvis_utils.config import is_confirm_before_apply_patch
from jarvis.jarvis_utils.git_utils import get_commits_between, get_latest_commit_hash
from jarvis.jarvis_utils.input import get_multiline_input
from jarvis.jarvis_utils.output import OutputType, PrettyOutput
from jarvis.jarvis_utils.utils import user_confirm

class PatchOutputHandler(OutputHandler):
    def name(self) -> str:
        return "PATCH"
    def handle(self, response: str) -> Tuple[bool, Any]:
        return False, apply_patch(response)
    
    def can_handle(self, response: str) -> bool:
        if _parse_patch(response):
            return True
        return False
    
    def prompt(self) -> str:
        return """
# 🛠️ 上下文代码补丁规范
使用<PATCH>块来指定代码更改：
--------------------------------
<PATCH>
File: [文件路径]
Reason: [修改原因]
[上下文代码片段]
</PATCH>
--------------------------------
规则：
1. 代码片段必须包含足够的上下文（前后各3行）
2. 我可以看到完整代码，所以只需显示修改的代码部分，不需要将整个文件内容都显示出来
3. 保留原始缩进和格式
4. 对于新文件，提供完整代码
5. 修改现有文件时，保留周围未更改的代码
示例：
<PATCH>
File: src/utils/math.py
Reason: 修复除零处理
def safe_divide(a, b):
    # 添加参数验证
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
# 现有代码 ...
def add(a, b):
    return a + b
</PATCH>
"""

def _parse_patch(patch_str: str) -> Dict[str, str]:
    """解析新的上下文补丁格式"""
    result = {}
    patches = re.findall(r'<PATCH>\n?(.*?)\n?</PATCH>', patch_str, re.DOTALL)
    if patches:
        for patch in patches:
            first_line = patch.splitlines()[0]
            sm = re.match(r'^File:\s*(.+)$', first_line)
            if not sm:
                PrettyOutput.print("无效的补丁格式", OutputType.WARNING)
                continue
            filepath = sm.group(1).strip()
            result[filepath] = patch
    return result

def apply_patch(output_str: str) -> str:
    """Apply patches to files"""
    with yaspin(text="正在应用补丁...", color="cyan") as spinner:
        try:
            patches = _parse_patch(output_str)
        except Exception as e:
            PrettyOutput.print(f"解析补丁失败: {str(e)}", OutputType.ERROR)
            return ""
        
        # 获取当前提交hash作为起始点
        spinner.text= "开始获取当前提交hash..."
        start_hash = get_latest_commit_hash()
        spinner.write("✅ 当前提交hash获取完成")
        
        # 按文件逐个处理
        for filepath, patch_content in patches.items():
            try:
                spinner.text = f"正在处理文件: {filepath}"
                with spinner.hidden():
                    handle_code_operation(filepath, patch_content)
                spinner.write(f"✅ 文件 {filepath} 处理完成")
            except Exception as e:
                spinner.text = f"文件 {filepath} 处理失败: {str(e)}, 回滚文件"
                revert_file(filepath)  # 回滚单个文件
                spinner.write(f"✅ 文件 {filepath} 回滚完成")
        
        final_ret = ""
        diff = get_diff()
        if diff:
            PrettyOutput.print(diff, OutputType.CODE, lang="diff")
            with spinner.hidden():
                commited = handle_commit_workflow()
            if commited:
                # 获取提交信息
                end_hash = get_latest_commit_hash()
                commits = get_commits_between(start_hash, end_hash)
                
                # 添加提交信息到final_ret
                if commits:
                    final_ret += "✅ 补丁已应用\n"
                    final_ret += "提交信息:\n"
                    for commit_hash, commit_message in commits:
                        final_ret += f"- {commit_hash[:7]}: {commit_message}\n"
                    
                    final_ret += f"应用补丁:\n{diff}"
                    
                else:
                    final_ret += "✅ 补丁已应用（没有新的提交）"
            else:
                final_ret += "❌ 我不想提交代码\n"
                final_ret += "补丁预览:\n"
                final_ret += diff
        else:
            final_ret += "❌ 没有要提交的更改\n"
        # 用户确认最终结果
        PrettyOutput.print(final_ret, OutputType.USER)
        if not is_confirm_before_apply_patch() or user_confirm("是否使用此回复？", default=True):
            return final_ret
        return get_multiline_input("请输入自定义回复")
def revert_file(filepath: str):
    """增强版git恢复，处理新文件"""
    import subprocess
    try:
        # 检查文件是否在版本控制中
        result = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', filepath],
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            subprocess.run(['git', 'checkout', 'HEAD', '--', filepath], check=True)
        else:
            if os.path.exists(filepath):
                os.remove(filepath)
        subprocess.run(['git', 'clean', '-f', '--', filepath], check=True)
    except subprocess.CalledProcessError as e:
        PrettyOutput.print(f"恢复文件失败: {str(e)}", OutputType.ERROR)
# 修改后的恢复函数
def revert_change():
    import subprocess
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], check=True)
    subprocess.run(['git', 'clean', '-fd'], check=True)
# 修改后的获取差异函数
def get_diff() -> str:
    """使用git获取暂存区差异"""
    import subprocess
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        ret = result.stdout
        subprocess.run(['git', "reset", "--soft", "HEAD"], check=True)
        return ret
    except subprocess.CalledProcessError as e:
        return f"获取差异失败: {str(e)}"
def handle_commit_workflow()->bool:
    """Handle the git commit workflow and return the commit details.
    
    Returns:
        tuple[bool, str, str]: (continue_execution, commit_id, commit_message)
    """
    if is_confirm_before_apply_patch() and not user_confirm("是否要提交代码？", default=True):
        revert_change()
        return False
    git_commiter = GitCommitTool()
    commit_result = git_commiter.execute({})
    return commit_result["success"]


def handle_code_operation(filepath: str, patch_content: str) -> bool:
    """处理基于上下文的代码片段"""
    with yaspin(text=f"正在修改文件 {filepath}...", color="cyan") as spinner:
        try:
            if not os.path.exists(filepath):
                # 新建文件
                spinner.text = "文件不存在，正在创建文件..."
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                open(filepath, 'w', encoding='utf-8').close()
                spinner.write("✅ 文件创建完成")
            with spinner.hidden():
                old_file_content = FileOperationTool().execute({"operation": "read", "files": [{"path": filepath}]})
                if not old_file_content["success"]:
                    spinner.write("❌ 文件读取失败")
                    return False
            
            prompt = f"""
    你是一个代码审查员，请审查以下代码并将其与上下文合并。
    原始代码:
    {old_file_content["stdout"]}
    补丁内容:
    {patch_content}
    """
            prompt += f"""
    请将代码与上下文合并并返回完整的合并代码，每次最多输出300行代码。

    要求:
    1. 严格保留原始代码的格式、空行和缩进
    2. 仅在<MERGED_CODE>块中包含实际代码内容，包括空行和缩进
    3. 绝对不要使用markdown代码块（```）或反引号，除非修改的是markdown文件
    4. 除了合并后的代码，不要输出任何其他文本
    5. 所有代码输出完成后，输出<!!!FINISHED!!!>

    输出格式:
    <MERGED_CODE>
    [merged_code]
    </MERGED_CODE>
    """
            model = PlatformRegistry().get_codegen_platform()
            model.set_suppress_output(True)
            count = 30
            start_line = -1
            end_line = -1
            code = []
            finished = False
            while count>0:
                count -= 1
                response = model.chat_until_success(prompt).splitlines()
                try:
                    start_line = response.index("<MERGED_CODE>") + 1
                    try:
                        end_line = response.index("</MERGED_CODE>")
                        code = response[start_line:end_line]
                    except:
                        pass
                except:
                    pass

                try: 
                    response.index("<!!!FINISHED!!!>")
                    finished = True
                    break
                except:
                    prompt += f"""继续输出接下来的300行代码
                    要求：
                    1. 严格保留原始代码的格式、空行和缩进
                    2. 仅在<MERGED_CODE>块中包含实际代码内容，包括空行和缩进
                    3. 绝对不要使用markdown代码块（```）或反引号，除非修改的是markdown文件
                    4. 除了合并后的代码，不要输出任何其他文本
                    5. 所有代码输出完成后，输出<!!!FINISHED!!!>
                    """
                    pass
            if not finished:
                spinner.text = "生成代码失败"
                spinner.fail("❌")
                return False
            # 写入合并后的代码
            spinner.text = "写入合并后的代码..."
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(code)+"\n")
            spinner.write("✅ 合并后的代码写入完成")
            spinner.text = "代码修改完成"
            spinner.ok("✅")
            return True
        except Exception as e:
            spinner.text = "代码修改失败"
            spinner.fail("❌")
            return False
