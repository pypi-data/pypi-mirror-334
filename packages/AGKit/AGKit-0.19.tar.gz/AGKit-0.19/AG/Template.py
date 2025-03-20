import os

from AG import Logger
from AG.Singleton import Singleton
from AG.DirUtil import DirUtil


class Template(Singleton):
    """单例模式的模板管理类，负责加载和存储模板文件内容。

    Attributes:
        template_dict (dict): 存储模板类型到文件内容的字典，格式为 {模板类型: {文件名: 内容}}。
    """
    template_dict = {}

    def __init__(self):
        pass

    def init_templates(self, templates_root):
        """初始化模板，加载指定根目录下的所有模板文件内容到内存。

        Args:
            templates_root (str): 模板文件的根目录路径。

        Returns:
            None
        """
        # 检查根目录是否存在
        if not DirUtil.check(templates_root, False):
            Logger.ins.Log("该目录不存在: %s" % templates_root)
            return

        # 遍历根目录下的所有模板类型子目录
        for _, template_types, _ in os.walk(templates_root):
            for template_type in template_types:
                template_root = "%s/%s" % (templates_root, template_type)
                # 遍历当前模板类型目录下的所有文件
                for _, _, template_files in os.walk(template_root):
                    for template_file in template_files:
                        template_path = "%s/%s" % (template_root, template_file)
                        with open(template_path, 'r', encoding='utf8') as f:
                            template_content = f.read()
                            # 将模板内容按类型和文件名存储到字典中
                            if template_type not in self.template_dict.keys():
                                self.template_dict[template_type] = {}
                            self.template_dict[template_type][template_file] = template_content

    def get_template(self, template_type, template_file):
        """获取指定类型和文件名的模板内容。

        Args:
            template_type (str): 模板类型名称。
            template_file (str): 模板文件名。

        Returns:
            str: 对应模板文件的内容。
        """
        return self.template_dict[template_type][template_file]
