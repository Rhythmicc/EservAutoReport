import os
import json
from QuickProject import user_root, user_lang, QproDefaultConsole, QproInfoString, _ask

enable_config = True
config_path = os.path.join(user_root, ".EservAutoReport_config")

user_questions = {
    "username": {
        "type": "input",
        "message": "Username" if user_lang != "zh" else "用户名",
    },
    "password": {
        "type": "password",
        "message": "Password" if user_lang != "zh" else "密码",
    },
    "province": {
        "type": "input",
        "message": "Province" if user_lang != "zh" else "省份",
    },
    "city": {
        "type": "input",
        "message": "City" if user_lang != "zh" else "城市",
    },
    "district": {
        "type": "input",
        "message": "District" if user_lang != "zh" else "区县",
    },
    "address": {
        "type": "input",
        "message": "Address" if user_lang != "zh" else "详细地址",
    },
    "to": {
        "type": "input",
        "message": "To" if user_lang != "zh" else "收件人",
    },
}

global_questions = {
    "remote-url": {
        "type": "input",
        "message": "Remote Selenium URL" if user_lang != "zh" else "远程 Selenium URL",
    },
    "email": {
        "type": "input",
        "message": "Email" if user_lang != "zh" else "邮箱",
    },
    "email_password": {
        "type": "password",
        "message": "Email password" if user_lang != "zh" else "邮箱密码",
    },
    "smtp": {
        "type": "input",
        "message": "SMTP" if user_lang != "zh" else "SMTP服务器",
    },
}


def init_config(user: str):
    with open(config_path, "w") as f:
        user_config = {i: _ask(user_questions[i]) for i in user_questions}
        global_config = {i: _ask(global_questions[i]) for i in global_questions}
        json.dump(
            {user: user_config, "global": global_config},
            f,
            indent=4,
        )
    QproDefaultConsole.print(
        QproInfoString,
        f'Config file has been created at: "{config_path}"'
        if user_lang != "zh"
        else f'配置文件已创建于: "{config_path}"',
    )


class EservAutoReportConfig:
    def __init__(self):
        if not os.path.exists(config_path):
            init_config(
                _ask(
                    {
                        "type": "input",
                        "message": "Username" if user_lang != "zh" else "用户名",
                    }
                )
            )
        while True:
            try:
                with open(config_path, "r") as f:
                    self.config = json.load(f)
                break
            except:
                init_config()

    def select(self, key):
        if key not in self.config:
            self.update(key, {i: _ask(user_questions[i]) for i in user_questions})
        return self.config[key]

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
