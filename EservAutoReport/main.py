from selenium import webdriver
from QuickProject.Commander import Commander
from . import *
from . import _config

app = Commander(name)
settings = _config.select("global")


def email(to: list, status: str = None):
    if not (_email := settings.get("email", None)):
        return
    import datetime

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not status:
        requirePackage(".RawSender", "Sender")(
            _email, settings.get("email_password"), settings.get("smtp"), "CUP自动填报"
        ).send(to, "【学生每日填报】上报成功", f"上报成功: {current_time}")
    else:
        requirePackage(".RawSender", "Sender")(
            _email, settings.get("email_password"), settings.get("smtp"), "CUP自动填报"
        ).send(to, "【学生每日填报】上报失败", f"上报失败: {status}")


def _report(user: str, driver: webdriver.Remote = None):
    infos = _config.select(user)

    from selenium.webdriver.common.by import By

    with QproDefaultConsole.status("正在打开浏览器...") as st:
        st.update("正在进入上报页面...")
        driver.get("https://eserv.cup.edu.cn/v2/matter/fill")

        driver.implicitly_wait(1)

        st.update("正在登录...")

        driver.switch_to.frame("loginIframe")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys(infos.get("username"))
        inputs[1].send_keys(infos.get("password"))

        driver.find_element(By.CLASS_NAME, "login_btn").click()

        driver.implicitly_wait(1)

        st.update("正在查找上报信息...")

        driver.switch_to.default_content()

        driver.implicitly_wait(5)

        ul = driver.find_element(By.CLASS_NAME, "matter_list_data")
        lis = ul.find_elements(By.TAG_NAME, "li")
        span = None
        for li in lis:
            span = li.find_element(By.TAG_NAME, "span")
            if span.text == "学生每日填报":
                break

        if not span:
            from QuickProject import QproErrorString

            QproDefaultConsole.print(QproErrorString, "未找到上报信息")
            driver.close()
            email([infos.get("to")], "未找到上报信息")
            return

        st.update("正在进入上报页面...")

        span.click()

        driver.implicitly_wait(10)

        st.update("正在填写上报信息...")

        table = driver.find_element(By.TAG_NAME, "table")
        trs = table.find_elements(By.TAG_NAME, "tr")

        tr4 = trs[4]
        td2 = tr4.find_elements(By.TAG_NAME, "td")[1]
        td4 = tr4.find_elements(By.TAG_NAME, "td")[3]

        td2.find_element(By.CLASS_NAME, "el-input__suffix").click()

        driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[2].click()

        td4.find_element(By.CLASS_NAME, "el-input__suffix").click()
        driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[4].click()

        tr11 = trs[11]
        td4 = tr11.find_elements(By.TAG_NAME, "td")[3]
        td4.find_element(By.TAG_NAME, "span").click()

        region_panel = driver.find_element(By.CLASS_NAME, "showdregions")

        provinces = region_panel.find_element(By.CLASS_NAME, "provinces")
        sps = provinces.find_elements(By.TAG_NAME, "span")

        for sp in sps:
            if sp.text == infos.get("province"):
                sp.click()
                break

        cities = region_panel.find_element(By.CLASS_NAME, "city")
        sps = cities.find_elements(By.TAG_NAME, "span")

        for sp in sps:
            if sp.text == infos.get("city"):
                sp.click()
                break

        if infos.get("district"):
            county = region_panel.find_element(By.CLASS_NAME, "county")
            sps = county.find_elements(By.TAG_NAME, "span")
            for sp in sps:
                if sp.text == infos.get("district"):
                    sp.click()
                    break

        address = region_panel.find_element(By.CLASS_NAME, "address")
        textarea = address.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys(infos.get("address"))
        region_panel.find_element(By.CLASS_NAME, "sure").click()

        tr12 = trs[12]
        td2 = tr12.find_elements(By.TAG_NAME, "td")[1]
        td2.find_element(By.CLASS_NAME, "el-input__suffix").click()
        driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[6].click()

        tr15 = trs[15]
        td1 = tr15.find_elements(By.TAG_NAME, "td")[0]
        td1.find_element(By.TAG_NAME, "input").click()

        st.update("正在提交上报信息...")

        driver.implicitly_wait(1)

        driver.find_element(By.CLASS_NAME, "help_btn").click()
        driver.find_element(By.CLASS_NAME, "zl-button-primary").click()

        driver.implicitly_wait(10)  # 等待提交成功

    QproDefaultConsole.print(QproInfoString, "上报成功!")
    email([infos.get("to")])


@app.command()
def report(user: str):
    """
    自动上报
    """
    from selenium import webdriver

    try:
        driver: webdriver.WebDriver = None
        with QproDefaultConsole.status("正在打开浏览器...") as st:
            if remote_url := settings.get("remote-url", None):
                st.update("正在打开远程浏览器...")
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                )
            else:
                from selenium.webdriver.chrome.options import Options

                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
        _report(user, driver)
        driver.close()
    except Exception as e:
        from QuickProject import QproErrorString

        if remote_url:
            driver.close()
        else:
            driver.quit()

        QproDefaultConsole.print(QproErrorString, e)
        email(_config.select(user).get("to"), e)
        raise e


@app.command()
def reset():
    """
    重置配置文件
    """
    from .__config__ import config_path
    import shutil

    shutil.rmtree(config_path)


@app.command()
def config(key: str, value: str = ""):
    """
    配置文件
    """
    if value:
        _config.set(key, value)
    else:
        QproDefaultConsole.print(QproInfoString, f'"{key}": "{_config.select(key)}"')


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
