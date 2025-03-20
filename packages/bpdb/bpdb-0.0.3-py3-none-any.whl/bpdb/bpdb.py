import requests
import configparser
import os

class BPDBSmartMeterAPI:
    BPDB_BASE_URL = "http://202.51.186.182:33262/api/v1"
    CONFIG_FILE = os.path.expanduser("~/.python-bpdb-api-config")

    def __init__(self):
        self.token = self.load_token()

    def send_otp(self, phone_number):
        url = f"{self.BPDB_BASE_URL}/generate-otp?phone={phone_number}"
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
    
    def login(self, phone_number, otp):
        url = f"{self.BPDB_BASE_URL}/validate-otp?phone={phone_number}&otp={otp}"
        response = requests.post(url)
        response.raise_for_status()
        if response.json().get("message") == "OTP verified successfully":
            self.token = response.json().get("token")
            self.save_token(self.token)
            return self.token
    
    def consumer_info(self):
        url = f"{self.BPDB_BASE_URL}/auth/consumer"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = {}
        prepaid_data = response.json()["user"]["prepaid_data"]

        for key in [
            "division",
            "meterType",
            "accountType",
            "sndDivision",
            "sanctionLoad",
            "customerName",
            "customerAddress",
            "tariffCategory"
            ]:
            data[key] = prepaid_data[key]
        return data

    def recharge_info(self, customer_number, meter_number):
        url = f"{self.BPDB_BASE_URL}/prepaid-consumer-info?customer_number={customer_number}%2C&meter_number={meter_number}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        data = []
        orders = response.json()["message"]["orders"]["order"]
        for order in orders:
            grossAmount = order["grossAmount"]
            energyCost = order["energyCost"]
            tokens = order["tokens"]
            date = order["date"]
            data.append({
                "date": date,
                "gross_amount": grossAmount,
                "energy_cost": energyCost,
                "tokens": tokens
            })
        return data

    def save_token(self, token):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'token': token}
        with open(self.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    def load_token(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.CONFIG_FILE):
            config.read(self.CONFIG_FILE)
            return config['DEFAULT'].get('token')
        return None
