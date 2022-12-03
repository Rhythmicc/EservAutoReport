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


def login(driver, By, infos):
    driver.switch_to.frame("loginIframe")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(infos.get("username"))
    inputs[1].send_keys(infos.get("password"))

    driver.find_element(By.CLASS_NAME, "login_btn").click()

    driver.implicitly_wait(1)


def _report(user: str, driver: webdriver.Remote = None, debug: bool = False):
    infos = _config.select(user)

    from selenium.webdriver.common.by import By

    with QproDefaultConsole.status("正在打开浏览器") as st:
        st.update("正在进入上报页面")
        driver.get("https://eserv.cup.edu.cn/v2/matter/fill")

        driver.implicitly_wait(1)

        st.update("正在登录")

        login(driver, By, infos)

        st.update("正在查找上报信息")

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

        st.update("正在进入上报页面")

        span.click()

        driver.implicitly_wait(10)

        st.update("正在填写上报信息")

        table = driver.find_element(By.TAG_NAME, "table")
        trs = table.find_elements(By.TAG_NAME, "tr")

        if infos.get("status") == 0:  # 在校
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
        else:  # 离校
            tr4 = trs[4]
            td2 = tr4.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "span").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[3].click()

            tr5 = trs[5]
            td2 = tr5.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "span").click()

            region_panel = td2.find_element(By.CLASS_NAME, "showdregions")
            provinces = region_panel.find_element(
                By.CLASS_NAME, "provinces"
            ).find_elements(By.TAG_NAME, "span")
            for sp in provinces:
                if sp.text == infos.get("province"):
                    sp.click()
                    break
            cities = region_panel.find_element(By.CLASS_NAME, "city").find_elements(
                By.TAG_NAME, "span"
            )
            for sp in cities:
                if sp.text == infos.get("city"):
                    sp.click()
                    break
            if infos.get("district"):
                county = region_panel.find_element(
                    By.CLASS_NAME, "county"
                ).find_elements(By.TAG_NAME, "span")
                for sp in county:
                    if sp.text == infos.get("district"):
                        sp.click()
                        break
            address = region_panel.find_element(By.CLASS_NAME, "address")
            textarea = address.find_element(By.TAG_NAME, "textarea")
            textarea.clear()
            textarea.send_keys(infos.get("address"))
            region_panel.find_element(By.CLASS_NAME, "sure").click()

            tr6 = trs[6]
            td2 = tr6.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "input").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[
                9 + infos.get("status")
            ].click()

            tr7 = trs[7]
            td2 = tr7.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "input").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[12].click()

            tr9 = trs[9]
            td2 = tr9.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "input").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[12].click()

            tr10 = trs[10]
            td2 = tr10.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.TAG_NAME, "input").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[12].click()

            tr11 = trs[11]
            td4 = tr11.find_elements(By.TAG_NAME, "td")[3]
            td4.find_element(By.TAG_NAME, "span").click()

            region_panel = td4.find_element(By.CLASS_NAME, "showdregions")
            provinces = region_panel.find_element(
                By.CLASS_NAME, "provinces"
            ).find_elements(By.TAG_NAME, "span")
            for sp in provinces:
                if sp.text == infos.get("province"):
                    sp.click()
                    break
            cities = region_panel.find_element(By.CLASS_NAME, "city").find_elements(
                By.TAG_NAME, "span"
            )
            for sp in cities:
                if sp.text == infos.get("city"):
                    sp.click()
                    break
            if infos.get("district"):
                county = region_panel.find_element(
                    By.CLASS_NAME, "county"
                ).find_elements(By.TAG_NAME, "span")
                for sp in county:
                    if sp.text == infos.get("district"):
                        sp.click()
                        break
            address = region_panel.find_element(By.CLASS_NAME, "address")
            textarea = address.find_element(By.TAG_NAME, "textarea")
            textarea.clear()
            textarea.send_keys(infos.get("address"))
            region_panel.find_element(By.CLASS_NAME, "sure").click()

            tr12 = trs[12]
            td2 = tr12.find_elements(By.TAG_NAME, "td")[1]
            td2.find_element(By.CLASS_NAME, "el-input__suffix").click()
            driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[12].click()

            tr15 = trs[15]
            td1 = tr15.find_elements(By.TAG_NAME, "td")[0]
            td1.find_element(By.TAG_NAME, "input").click()

        st.update("正在提交上报信息")

        if not debug:
            driver.implicitly_wait(1)

            driver.find_element(By.CLASS_NAME, "help_btn").click()
            driver.find_element(By.CLASS_NAME, "zl-button-primary").click()

        driver.implicitly_wait(10)  # 等待提交成功

    QproDefaultConsole.print(QproInfoString, "上报成功!")
    email([infos.get("to")])


@app.command()
def report(user: str, _debug: bool = False):
    """
    自动上报

    :param user: 用户名
    :param _debug: 是否调试模式
    """
    from selenium import webdriver

    try:
        driver: webdriver.WebDriver = None
        with QproDefaultConsole.status("正在打开浏览器") as st:
            if remote_url := settings.get("remote-url", None) and not _debug:
                st.update("正在打开远程浏览器")
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                )
            else:
                driver = webdriver.Chrome()
        _report(user, driver, _debug)
        driver.close()
    except Exception as e:
        from QuickProject import QproErrorString

        if _debug:
            from selenium.webdriver.common.by import By

            return By, driver, _config.select(user), e

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


@app.command()
def update():
    """
    更新
    """
    from . import external_exec

    with QproDefaultConsole.status("正在更新"):
        external_exec(
            f"{user_pip} install git+https://github.com/Rhythmicc/EservAutoReport.git -U",
            True,
        )
    QproDefaultConsole.print(QproInfoString, "更新成功!")


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
