"""
appium API
"""
import base64
from pathlib import Path
from typing import Any, Dict
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver import Remote as AppiumRemote
from seldom.logging import log
from seldom.running.config import Seldom
from seldom.webdriver import WebDriver


class AppDriver(WebDriver):
    """
    appium base API
    """

    def __init__(self):
        self.browser = AppiumRemote(command_executor=Seldom.app_server, options=Seldom.app_info,
                                    extensions=Seldom.extensions)
        Seldom.driver = self.browser

    def background_app(self, seconds: int):
        """
        Puts the application in the background on the device for a certain duration.

        Args:
            seconds: the duration for the application to remain in the background
        """
        log.info(f"📱 background app {seconds}s")
        self.browser.background_app(seconds=seconds)
        return self

    def is_app_installed(self, bundle_id: str) -> bool:
        """Checks whether the application specified by `bundle_id` is installed on the device.

        Args:
            bundle_id: the id of the application to query

        Returns:
            `True` if app is installed
        """
        log.info(f"📱 is app installed: {bundle_id}")
        return self.browser.is_app_installed(bundle_id=bundle_id)

    def install_app(self, app_path: str, **options: Any):
        """Install the application found at `app_path` on the device.

        Args:
            app_path: the local or remote path to the application to install

        Keyword Args:
            replace (bool): [Android only] whether to reinstall/upgrade the package if it is
                already present on the device under test. True by default
            timeout (int): [Android only] how much time to wait for the installation to complete.
                60000ms by default.
            allowTestPackages (bool): [Android only] whether to allow installation of packages marked
                as test in the manifest. False by default
            useSdcard (bool): [Android only] whether to use the SD card to install the app. False by default
            grantPermissions (bool): [Android only] whether to automatically grant application permissions
                on Android 6+ after the installation completes. False by default

        Returns:
            Union['WebDriver', 'Applications']: Self instance
        """
        log.info(f"📱 install app: {app_path}")
        self.browser.install_app(app_path=app_path, **options)
        return self

    def remove_app(self, app_id: str, **options: Any):
        """Remove the specified application from the device.

        Args:
            app_id: the application id to be removed

        Keyword Args:
            keepData (bool): [Android only] whether to keep application data and caches after it is uninstalled.
                False by default
            timeout (int): [Android only] how much time to wait for the uninstall to complete.
                20000ms by default.

        Returns:
            Union['WebDriver', 'Applications']: Self instance
        """
        log.info(f"📱 remove app: {app_id}")
        self.browser.remove_app(app_id=app_id, **options)
        return self

    def terminate_app(self, app_id: str, **options: Any) -> bool:
        """Terminates the application if it is running.

        Args:
            app_id: the application id to be terminates

        Keyword Args:
            `timeout` (int): [Android only] how much time to wait for the uninstall to complete.
                500ms by default.

        Returns:
            True if the app has been successfully terminated
        """
        log.info(f"📱 terminate app: {app_id}")
        return self.browser.terminate_app(app_id=app_id, **options)

    def activate_app(self, app_id: str):
        """Activates the application if it is not running
        or is running in the background.

        Args:
            app_id: the application id to be activated

        Returns:
            Union['WebDriver', 'Applications']: Self instance
        """
        self.browser.activate_app(app_id=app_id)
        return self

    def query_app_state(self, app_id: str) -> int:
        """Queries the state of the application.

        Args:
            app_id: the application id to be queried

        Returns:
            One of possible application state constants. See ApplicationState
            class for more details.
        """
        log.info(f"📱 query app state: {app_id}")
        return self.browser.query_app_state(app_id=app_id)

    def app_strings(self, language: str = None, string_file: str = None) -> Dict[str, str]:
        """Returns the application strings from the device for the specified
        language.

        Args:
            language: strings language code
            string_file: the name of the string file to query

        Returns:
            The key is string id and the value is the content.
        """
        log.info(f"📱 app strings")
        return self.browser.app_strings(language=language, string_file=string_file)

    @staticmethod
    def base64_image(image_path: str):
        """
        jpg/png file to base64
        :param image_path:
        :return:
        """
        file_path = Path(image_path)
        if file_path.is_file() is False:
            log.error("The file path does not exist.")
            return

        with open(image_path, 'rb') as png_file:
            b64_data = base64.b64encode(png_file.read()).decode('UTF-8')
            return b64_data

    def click_image(self, image_path: str) -> None:
        """
        click image
        :param image_path:
        :return:
        """
        log.info(f"✅ image -> click.")
        self.browser.update_settings({"getMatchedImageResult": True})
        self.browser.update_settings({"fixImageTemplatescale": True})
        b64 = self.base64_image(image_path)
        self.browser.find_element(AppiumBy.IMAGE, b64).click()

    def keyboard_search(self) -> None:
        """
        appium API
        App keyboard search key.
        """
        log.info("🔍 keyboard search key.")
        self.browser.execute_script('mobile: performEditorAction', {'action': 'search'})
