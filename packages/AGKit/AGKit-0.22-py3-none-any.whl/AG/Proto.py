import os
import subprocess

from AG.Logger import Logger


class Proto:
    @staticmethod
    def GenCSharp(file_path, dst):
        file_path = os.path.abspath(file_path)
        proto_dir = os.path.dirname(file_path)
        proto_name = os.path.basename(file_path)
        try:
            subprocess.call(['protoc', f'--csharp_out={dst}', f'--proto_path={proto_dir}', f'{proto_name}'])
        except Exception as e:
            Logger.Instance.Info("协议生成异常：%s" % e)

    @staticmethod
    def AddProtocToPath(protoc_dir):
        env_path = os.environ.get('PATH', '')
        os.environ['PATH'] = f'{protoc_dir};{env_path}'
