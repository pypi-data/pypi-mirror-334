# -*- coding: UTF-8 -*-
import os

from .cmd import run_command
from .config import APACHE_READ_MODEL

chroot_fd = -1


def into_chroot_env(chroot_path):
    """
    函数功能：进入chroot状态
    函数参数：chroot_path - chroot的目录
    函数返回值：无
    """
    global chroot_fd
    if chroot_fd == -1:
        try:
            chroot_fd = os.open("/", os.O_PATH)
            os.chdir(chroot_path)
            os.chroot(".")
            os.listdir(".")
        except Exception as e:
            print(f"chroot失败：{e}")


def exit_chroot_env():
    """
    函数功能：退出chroot状态
    函数参数：无
    函数返回值：无
    """
    global chroot_fd
    if chroot_fd > 0:
        os.chdir(chroot_fd)
        os.chroot(".")
        os.close(chroot_fd)
        chroot_fd = -1


def get_mock_template(tag):
    if str(tag).startswith("ns6"):
        return "mock_ns6.cfg"
    elif str(tag).startswith("v11"):
        return "mock_ns11.cfg"
    else:
        return "mock_ns7_plus.cfg"


def generate_mock_config(params, mock_tag, _logger, config_root_dir):
    """
    mock通用配置文件设置
    os.path.abspath(__file__)
    """
    # 输出测试
    get_mock_template(mock_tag)
    fn = get_mock_template(mock_tag)
    fp = f"{config_root_dir}/{fn}"
    if os.path.exists(fp):
        content = open(fp, encoding="utf-8").read()
        content = content.replace("{Packages}", "yum" if params.get('series_version') == '7' else "dnf")
        content = content.replace("{arch}", params.get('target_arch'))
        content = content.replace("{root}", mock_tag)
        content = content.replace("{yum_url}", params.get('yum_url'))
        if params.get('yum_url').find("kojifiles/repos") < 0:
            content = content.replace('#{yum_url_in_koji}', '')

    else:
        _logger.error(f"未找到mock模版配置文件:{fp}")
        raise FileNotFoundError(f"未找到mock模版配置文件:{fp}")
    mock_cfile = f"/etc/mock/{mock_tag}.cfg"
    with open(mock_cfile, 'w', APACHE_READ_MODEL) as f:
        f.writelines(content)
    os.chmod(mock_cfile, APACHE_READ_MODEL)
    _logger.info("生成Mock配置文件" + mock_cfile)
    return mock_cfile


def init_mock_env(params, mock_tag, _logger, lorax_cpio="https://server.kylinos.cn:9031/integration_iso_files/auto_os/script/lorax/mips64el/lorax.cpio"):
    """初始化mock环境"""
    user = params.get('user', 'pungier')
    cmds = list()
    _logger.info("Build端初始化mock环境....")

    if params.get("pungi_url"):
        cmds.append(f"""su {user} -c "mock -n -r {mock_tag} --install {params.get("pungi_url")}" """)
    else:
        cmds.append(f"""su {user} -c "mock -n -r {mock_tag} --install pungi" """)
    if params.get("lorax_url"):
        cmds.append(f"""su {user} -c "mock -n -r {mock_tag} --install {params.get("lorax_url")}" """)
    else:
        cmds.append(f"""su {user} -c "mock -n -r {mock_tag} --install lorax" """)
    cmds.append(f"""su {user} -c "mock -n -r {mock_tag} --install koji" """)
    if params.get("target_arch") == "mips":
        mips_url = params.get("mips_url", lorax_cpio)
        cmds.append(
            f""" wget -nv --limit-rate=20m -r -np -nH -L --cut-dirs 4 -e robots=off -R index.html* --restrict-file-names=nocontrol \
            -P /var/lib/mock/{mock_tag}/root/root {mips_url} --no-check """)
        cmds.append(
            f""" su {user} -c "mock -n -r {mock_tag} --shell 'cpio -idumv < /root/lorax.cpio'" """)
    cmds.append(
        f""" su {user} -c "mock -n -r {mock_tag} --shell 'mkdir -p /root/buildiso/Packages /root/buildiso/lorax /root/isos'" """)
    for cmd in cmds:
        r = run_command(cmd, _logger, "mock环境初始化失败")
        if not r:
            raise SystemExit(f" 执行 【{cmd}】命令发生异常，Err :", "mock环境初始化失败")
