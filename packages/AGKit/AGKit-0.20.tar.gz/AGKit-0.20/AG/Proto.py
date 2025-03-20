import os
import subprocess

from AG.Logger import Logger


class Proto:
    @staticmethod
    def gen_c_sharp(file_path, dst):
        """生成C#代码文件。

        Args:
            file_path (str): 需要编译的proto文件路径。
            dst (str): 生成的C#代码的目标目录路径。

        Returns:
            None
        """
        file_path = os.path.abspath(file_path)
        proto_dir = os.path.dirname(file_path)
        proto_name = os.path.basename(file_path)
        try:
            # 执行protoc命令生成C#代码
            subprocess.call(['protoc',
                             f'--csharp_out={dst}',
                             f'--proto_path={proto_dir}',
                             f'{proto_name}']
                            )
        except Exception as e:
            Logger.ins.info("协议生成异常：%s" % e)

    @staticmethod
    def add_protoc_to_path(protoc_dir):
        """将protoc可执行文件路径添加到系统环境变量PATH中。

        Args:
            protoc_dir (str): protoc可执行文件所在的目录路径。

        Returns:
            None
        """
        env_path = os.environ.get('PATH', '')
        os.environ['PATH'] = f'{protoc_dir};{env_path}'
