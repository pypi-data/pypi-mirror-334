import base64
import hashlib
import hmac
import json
import os

import requests
import logging
import time
from datetime import datetime as dt, timezone
from json import JSONDecodeError
from requests_toolbelt import MultipartEncoder

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from ._exceptions import FailedRequestError
from ._p2p_method import P2PMethod

_SUBDOMAIN_TESTNET = "api-testnet"
_SUBDOMAIN_MAINNET = "api"
_DOMAIN_MAIN = "bybit"
_DOMAIN_ALT = "bytick"
_TLD_MAIN = "com"


class P2PManager:
    def __init__(
            self,
            testnet,
            api_key="",
            api_secret="",
            domain=None,
            tld=None,
            recv_window=5000,
            rsa=False,
            logging_level=logging.INFO,
            disable_ssl_checks=False
    ):
        self._testnet = testnet
        self._api_key = api_key
        self._api_secret = api_secret
        self._recv_window = recv_window
        self._rsa = rsa
        self._logging_level = logging_level

        # determine domain to use
        self._subdomain = _SUBDOMAIN_TESTNET if self._testnet else _SUBDOMAIN_MAINNET
        self._domain = _DOMAIN_MAIN if not domain else domain
        self._tld = _TLD_MAIN if not tld else tld
        self._url = "https://{SUBDOMAIN}.{DOMAIN}.{TLD}".format(SUBDOMAIN=self._subdomain, DOMAIN=self._domain, TLD=self._tld)
        self.client = requests.Session()
        self.client.verify = not disable_ssl_checks
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        self.logger = logging.getLogger(__name__)
        if len(logging.root.handlers) == 0:
            # no handler on root logger set -> we add handler just for this logger to not mess with custom logic from outside
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            handler.setLevel(self._logging_level)
            self.logger.addHandler(handler)

        self.logger.debug("Initialized P2P API session.")

    def http_req_handler(self, method: P2PMethod, params):
        if params is None:
            params = {}

        # ensure all the required params are passed
        missing_params = [p for p in method.required_params if p not in params]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

        # Bug fix: change floating whole numbers to integers to prevent
        # auth signature errors.
        for i in params.keys():
            if isinstance(params[i], float) and params[i] == int(params[i]):
                params[i] = int(params[i])

        # construct request in accordance with API specs
        timestamp = int(time.time() * 10 ** 3)

        contentType = "application/json"
        # special handling for FILE data type
        if method.http_method == "FILE":
            filepath = params["upload_file"]
            boundary = "boundary-for-file"
            contentType = f"multipart/form-data; boundary={boundary}"
            filename = os.path.basename(str(filepath))
            mimeType = "image/png"

            with open(filepath, "rb") as f:
                binary_data = f.read()

            files = MultipartEncoder(
                {
                    'upload_file': (
                        filename,
                        open(filepath, "rb"),
                        mimeType
                    )
                },
                boundary=boundary
            )
            payload = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"upload_file\"; filename=\"{filename}\"\r\nContent-Type: {mimeType}\r\n\r\n"
            ).encode() + binary_data + f"\r\n--{boundary}--\r\n".encode()
            signature = self._generate_sign_binary(payload, timestamp)
            payload = files.to_string()  # final conversion to send to server
        else:
            payload = self._generate_payload(method.http_method, params)
            signature = self._generate_sign(payload, timestamp)

        headers = {
            'X-BAPI-API-KEY': self._api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': str(timestamp),
            'X-BAPI-RECV-WINDOW': str(self._recv_window),
            'Content-Type': contentType
        }

        # build the request
        endpoint = self._url + method.url
        if method.http_method == "GET":
            r = self.client.prepare_request(
                requests.Request(
                    method.http_method, endpoint + f"?{payload}" if payload != "" else "", headers=headers
                )
            )
        elif method.http_method == "POST" or method.http_method == "FILE":
            r = self.client.prepare_request(
                requests.Request(
                    "POST", endpoint, data=payload, headers=headers
                )
            )

        # send the request
        try:
            s = self.client.send(r)
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
        ) as e:
            raise e

        if s.status_code != 200:
            if s.status_code == 403:
                error_msg = ("Access denied error. Possible causes: 1) your IP is located in the US or Mainland China, "
                             "2) IP banned due to ratelimit violation")
            elif s.status_code == 401:
                error_msg = ("Unauthorized. Possible causes: 1) incorrect API key and/or secret, "
                             "2) incorrect environment: Mainnet vs Testnet")
            else:
                error_msg = f"HTTP status code is: {s.status_code}, expected: 200"
                self.logger.error(f"{error_msg}")
            raise FailedRequestError(
                request=f"{endpoint}: {payload}",
                message=error_msg,
                status_code=s.status_code,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=s.headers,
            )

        # Convert response to dictionary, or raise if requests error.
        try:
            s_json = s.json()
        except JSONDecodeError as e:
            self.logger.debug(f"Response text: {s.text}")
            raise FailedRequestError(
                request=f"{endpoint}: {payload}",
                message="Could not decode JSON.",
                status_code=s.status_code,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=s.headers,
            )

        ret_code = "retCode"
        ret_msg = "retMsg"

        if ret_code not in s_json:
            ret_code = "ret_code"
        if ret_msg not in s_json:
            ret_msg = "ret_msg"


        # If Bybit returns an error, raise.
        if s_json[ret_code]:
            # Generate error message.
            error_msg = f"{s_json[ret_msg]} (ErrCode: {s_json[ret_code]})"
            self.logger.error(f"{error_msg}")
            raise FailedRequestError(
                request=f"{endpoint}: {payload}",
                message=s_json[ret_msg],
                status_code=s_json[ret_code],
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=s.headers,
            )
        else:
            return s_json

    def _generate_sign(self, payload, timestamp):
        sign_string = str(timestamp) + self._api_key + str(self._recv_window) + payload
        return P2PManager._sign(self._rsa, self._api_secret, sign_string)

    def _generate_sign_binary(self, payload, timestamp):
        sign_string = f"{timestamp}{self._api_key}{self._recv_window}".encode() + payload
        return P2PManager._sign(self._rsa, self._api_secret, sign_string, True)

    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _cast_values(params):
        str_params = [
            "itemId",
            "side",
            "currency_id",
            # get_ad_detail
            "id",
            "priceType",
            "premium",
            "price",
            "minAmount",
            "maxAmount",
            "remark",
            "actionType",
            "quantity",
            "paymentPeriod",
            # -> tradingPreferenceSet
            "hasUnPostAd",
            "isKyc",
            "isEmail",
            "isMobile",
            "hasRegisterTime",
            "registerTimeThreshold",
            "orderFinishNumberDay30",
            "completeRateDay30",
            "nationalLimit",
            "hasOrderFinishNumberDay30",
            "hasCompleteRateDay30",
            "hasNationalLimit",
            # get_orders
            "beginTime",
            "endTime",
            "tokenId",
            # get chat message
            "startMessageId"
        ]
        int_params = [
            "positionIdx",
        ]

        P2PManager._cast_dict_recursively(params, str_params, int_params)


    @staticmethod
    def _cast_dict_recursively(dictionary, str_params, int_params):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                # recursive edit
                P2PManager._cast_dict_recursively(value, str_params, int_params)
                continue

            if key in str_params:
                if not isinstance(value, str):
                    dictionary[key] = str(value)
            elif key in int_params:
                if not isinstance(value, int):
                    dictionary[key] = int(value)

    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _generate_payload(http_method, params):
        if http_method == "GET":
            payload = "&".join(
                [
                    str(k) + "=" + str(v)
                    for k, v in sorted(params.items())
                    if v is not None
                ]
            )
            return payload
        elif http_method == "POST":
            P2PManager._cast_values(params)
            return json.dumps(params)


    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _sign(use_rsa_authentication, secret, param_str, binary=False):
        def generate_hmac():
            hash = hmac.new(
                bytes(secret, "utf-8"),
                param_str.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        def generate_hmac_binary():
            hash = hmac.new(
                bytes(secret, "utf-8"),
                param_str,
                hashlib.sha256,
            )
            return hash.hexdigest()

        def generate_rsa():
            hash = SHA256.new(param_str.encode("utf-8"))
            encoded_signature = base64.b64encode(
                PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                    hash
                )
            )
            return encoded_signature.decode()

        def generate_rsa_binary():
            hash = SHA256.new(param_str)
            encoded_signature = base64.b64encode(
                PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                    hash
                )
            )
            return encoded_signature.decode()

        if not use_rsa_authentication:
            if binary:
                return generate_hmac_binary()
            return generate_hmac()
        else:
            if binary:
                return generate_rsa_binary()
            return generate_rsa()

