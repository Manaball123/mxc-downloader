import cfg
from Crypto.Cipher import AES
import base64




# export function getHttpUriForMxc(
#     baseUrl: string,
#     mxc?: string,
#     width?: number,
#     height?: number,
#     resizeMethod?: string,
#     allowDirectLinks = false,
#     allowRedirects?: boolean,
#     useAuthentication?: boolean,
# ): string {
#     if (typeof mxc !== "string" || !mxc) {
#         return "";
#     }
#     if (mxc.indexOf("mxc://") !== 0) {
#         if (allowDirectLinks) {
#             return mxc;
#         } else {
#             return "";
#         }
#     }

#     if (useAuthentication) {
#         allowRedirects = true; // per docs (MSC3916 always expects redirects)

#         // Dev note: MSC3916 removes `allow_redirect` entirely, but
#         // for explicitness we set it here. This makes it slightly more obvious to
#         // callers, hopefully.
#     }

#     let serverAndMediaId = mxc.slice(6); // strips mxc://
#     let prefix: string;
#     if (useAuthentication) {
#         prefix = "/_matrix/client/v1/media/download/";
#     } else {
#         prefix = "/_matrix/media/v3/download/";
#     }
#     const params: Record<string, string> = {};

#     if (width) {
#         params["width"] = Math.round(width).toString();
#     }
#     if (height) {
#         params["height"] = Math.round(height).toString();
#     }
#     if (resizeMethod) {
#         params["method"] = resizeMethod;
#     }
#     if (Object.keys(params).length > 0) {
#         // these are thumbnailing params so they probably want the
#         // thumbnailing API...
#         if (useAuthentication) {
#             prefix = "/_matrix/client/v1/media/thumbnail/";
#         } else {
#             prefix = "/_matrix/media/v3/thumbnail/";
#         }
#     }

#     if (typeof allowRedirects === "boolean") {
#         // We add this after, so we don't convert everything to a thumbnail request.
#         params["allow_redirect"] = JSON.stringify(allowRedirects);
#     }

#     const fragmentOffset = serverAndMediaId.indexOf("#");
#     let fragment = "";
#     if (fragmentOffset >= 0) {
#         fragment = serverAndMediaId.slice(fragmentOffset);
#         serverAndMediaId = serverAndMediaId.slice(0, fragmentOffset);
#     }

#     const urlParams = Object.keys(params).length === 0 ? "" : "?" + encodeParams(params);
#     return baseUrl + prefix + serverAndMediaId + urlParams + fragment;
# }

def mxc_to_http_url(mxc_url : str, base_url : str = cfg.base_url):
    server_and_media_id = mxc_url[6:]
    #too lazy to implement the spec, should work 99% of the time anyway
    #see above for standard impl
    prefix = "/_matrix/media/v3/download/"
    return base_url + prefix + server_and_media_id



def is_encrypted_file(event : dict) -> bool:
    if "file" in event["content"]:
        return True
    return False
def mxc_url_from_event(event : dict) -> str:
    if(is_encrypted_file(event)):
        return event["content"]["file"]["url"]
    return event["content"]["url"]

def http_url_from_event(event : dict) -> str:
    return mxc_to_http_url(mxc_url_from_event(event))

def get_filename_from_event(event : dict) -> str:
    return event["content"]["body"]

def decode_base_64(base64s : str) -> bytes:
    paddedBase64 = base64s + "=" * ((4 - len(base64s) % 4) % 4)
    return base64.b64decode(paddedBase64)


def decrypt_buffer(event : dict, data : bytes) -> bytes:
    file_meta = event["content"]["file"]

    aes_key = decode_base_64(file_meta["key"]["k"])
    iv_array = decode_base_64(file_meta["iv"])

    cipher = AES.new(aes_key, AES.MODE_CTR, initial_value=iv_array, nonce=b'')
    return cipher.decrypt(data)