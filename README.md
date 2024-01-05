# 🔥 Noble TLS

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)

Noble TLS is an advanced HTTP library based on requests and tls-client.
Now async, providing many more features and auto updating the JA3 fingerprints.

# Installation
```
pip install noble-tls
```

### Features
- [x] Auto updating feature: Update TLS client libs from bogdanfinn/tls-client
- [x] Async support
- [x] Proxy support
- [x] Custom JA3 string
- [x] Custom H2 settings
- [x] Custom supported signature algorithms
- [x] Custom supported versions
- [x] Custom key share curves
- [x] Custom cert compression algorithm
- [x] Custom pseudo header order
- [x] Custom connection flow
- [x] Custom header order
- [x] Custom client identifier (Chrome, Firefox, Opera, Safari, iOS, iPadOS, Android)
- [x] Random TLS extension order
- [x] Custom TLS extension order
- [x] `requests`'s `history` support
- [x] `requests`'s `allow_redirects` support
- [x] much more...

# Examples
The syntax is inspired by [requests](https://github.com/psf/requests), so its very similar and there are only very few things that are different.


Example 1 - Preset:

```python
import noble_tls
from noble_tls import Client

# Available identifiers: 
""" 
    CHROME_103 = "chrome_103"
    CHROME_104 = "chrome_104"
    CHROME_105 = "chrome_105"
    CHROME_106 = "chrome_106"
    CHROME_107 = "chrome_107"
    CHROME_108 = "chrome_108"
    CHROME_109 = "chrome_109"
    CHROME_110 = "chrome_110"
    CHROME_111 = "chrome_111"
    CHROME_112 = "chrome_112"
    CHROME_116_PSK = "chrome_116_PSK"
    CHROME_116_PSK_PQ = "chrome_116_PSK_PQ"
    CHROME_117 = "chrome_117"
    CHROME_120 = "chrome_120"
    SAFARI_15_6_1 = "safari_15_6_1"
    SAFARI_16_0 = "safari_16_0"
    SAFARI_IPAD_15_6 = "safari_ipad_15_6"
    SAFARI_IOS_15_5 = "safari_ios_15_5"
    SAFARI_IOS_15_6 = "safari_ios_15_6"
    SAFARI_IOS_16_0 = "safari_ios_16_0"
    FIREFOX_102 = "firefox_102"
    FIREFOX_104 = "firefox_104"
    FIREFOX_105 = "firefox_105"
    FIREFOX_106 = "firefox_106"
    FIREFOX_108 = "firefox_108"
    FIREFOX_110 = "firefox_110"
    FIREFOX_117 = "firefox_117"
    FIREFOX_120 = "firefox_120"
    OPERA_89 = "opera_89"
    OPERA_90 = "opera_90"
    OPERA_91 = "opera_91"
    ZALANDO_ANDROID_MOBILE = "zalando_android_mobile"
    ZALANDO_IOS_MOBILE = "zalando_ios_mobile"
    NIKE_IOS_MOBILE = "nike_ios_mobile"
    NIKE_ANDROID_MOBILE = "nike_android_mobile"
    CLOUDSCRAPER = "cloudscraper"
    MMS_IOS = "mms_ios"
    MMS_IOS_1 = "mms_ios_1"
    MMS_IOS_2 = "mms_ios_2"
    MMS_IOS_3 = "mms_ios_3"
    MESH_IOS = "mesh_ios"
    MESH_IOS_1 = "mesh_ios_1"
    MESH_IOS_2 = "mesh_ios_2"
    MESH_ANDROID = "mesh_android"
    MESH_ANDROID_1 = "mesh_android_1"
    MESH_ANDROID_2 = "mesh_android_2"
    CONFIRMED_IOS = "confirmed_ios"
    CONFIRMED_ANDROID = "confirmed_android"
    OKHTTP4_ANDROID_7 = "okhttp4_android_7"
    OKHTTP4_ANDROID_8 = "okhttp4_android_8"
    OKHTTP4_ANDROID_9 = "okhttp4_android_9"
    OKHTTP4_ANDROID_10 = "okhttp4_android_10"
    OKHTTP4_ANDROID_11 = "okhttp4_android_11"
    OKHTTP4_ANDROID_12 = "okhttp4_android_12"
    OKHTTP4_ANDROID_13 = "okhttp4_android_13"
"""

async def main():
    await noble_tls.update_if_necessary() # Update TLS client libs from bogdanfinn/tls-client
    session = noble_tls.Session(
        client=Client.CHROME_111,
        random_tls_extension_order=True
    )
    res = await session.get(
        "https://www.example.com/",
        headers={
            "key1": "value1",
        },
        proxy="http://user:password@host:port"
    )
    print(res.text)
```

Example 2 - Custom:

```python
import noble_tls


async def main():
    await noble_tls.update_if_necessary() # Update TLS client libs from bogdanfinn/tls-client
    
    session = noble_tls.Session(
        ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
        h2_settings={
            "HEADER_TABLE_SIZE": 65536,
            "MAX_CONCURRENT_STREAMS": 1000,
            "INITIAL_WINDOW_SIZE": 6291456,
            "MAX_HEADER_LIST_SIZE": 262144
        },
        h2_settings_order=[
            "HEADER_TABLE_SIZE",
            "MAX_CONCURRENT_STREAMS",
            "INITIAL_WINDOW_SIZE",
            "MAX_HEADER_LIST_SIZE"
        ],
        supported_signature_algorithms=[
            "ECDSAWithP256AndSHA256",
            "PSSWithSHA256",
            "PKCS1WithSHA256",
            "ECDSAWithP384AndSHA384",
            "PSSWithSHA384",
            "PKCS1WithSHA384",
            "PSSWithSHA512",
            "PKCS1WithSHA512",
        ],
        supported_versions=["GREASE", "1.3", "1.2"],
        key_share_curves=["GREASE", "X25519"],
        cert_compression_algo="brotli",
        pseudo_header_order=[
            ":method",
            ":authority",
            ":scheme",
            ":path"
        ],
        connection_flow=15663105,
        header_order=[
            "accept",
            "user-agent",
            "accept-encoding",
            "accept-language"
        ]
    )

    res = await session.post(
        "https://www.example.com/",
        headers={
            "key1": "value1",
        },
        proxy="http://user:password@host:port"
    )
    print(res.text)
```

# Pyinstaller / Pyarmor
**If you want to pack the library with Pyinstaller or Pyarmor, make sure to add this to your command:**

Linux - Ubuntu / x86:
```
--add-binary '{path_to_library}/tls_client/dependencies/tls-client-x86.so:tls_client/dependencies'
```

Linux Alpine / AMD64:
```
--add-binary '{path_to_library}/tls_client/dependencies/tls-client-amd64.so:tls_client/dependencies'
```

MacOS M1 and older:
```
--add-binary '{path_to_library}/tls_client/dependencies/tls-client-x86.dylib:tls_client/dependencies'
```

MacOS M2:
```
--add-binary '{path_to_library}/tls_client/dependencies/tls-client-arm64.dylib:tls_client/dependencies'
```

Windows:
```
--add-binary '{path_to_library}/tls_client/dependencies/tls-client-64.dll;tls_client/dependencies'
```
### ❤️ One final note
Package is named after [Admiral Atticus Noble in Rebel Moon: Part One - A Child of Fire villain](https://www.youtube.com/watch?v=cO-GPaASWV0)
### Acknowledgements
Big shout out to [Bogdanfinn](https://github.com/bogdanfinn) for open sourcing his [tls-client](https://github.com/bogdanfinn/tls-client) in Golang.
and FlorianREGAZ