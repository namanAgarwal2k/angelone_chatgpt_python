from SmartApi import SmartConnect
import pyotp

from config.config import API_KEY, CLIENT_CODE, PASSWORD, TOTP  

class SmartConnectSingleton:
    _instance = None

    @staticmethod
    def _initialize_session():
        """Initialize the session for Angel One SmartConnect."""
        SmartConnectSingleton._instance = SmartConnect(api_key=API_KEY)

        # Generate TOTP using pyotp or fetch it manually
        totp = pyotp.TOTP(TOTP)
        current_totp = totp.now()

        data = SmartConnectSingleton._instance.generateSession(
            CLIENT_CODE,
            PASSWORD,
            current_totp 
        )

        # Check if login is successful
        if isinstance(data, dict) and data.get('status') is True:
            print("Session initialized successfully")
        else:
            raise Exception(f"Failed to initialize session: {data.get('message', 'Unknown error')}")

    @staticmethod
    def get_instance() -> SmartConnect:
        """Return the single instance of SmartConnect."""
        if SmartConnectSingleton._instance is None:
            SmartConnectSingleton._initialize_session()
        return SmartConnectSingleton._instance
