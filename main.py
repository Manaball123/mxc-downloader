import mxc_utils
import json
import requests



def main():
    with open("sample.json", "r") as f:
        event = json.loads(f.read())
    url = mxc_utils.http_url_from_event(event)
    resp = requests.get(url)
    filename = mxc_utils.get_filename_from_event(event)
    if not mxc_utils.is_encrypted_file(event):
        with open(filename, "wb") as f:
            f.write(resp.content)
        return
    data = mxc_utils.decrypt_buffer(event, resp.content)
    with open(filename, "wb") as f:
        f.write(data)




if __name__ == "__main__":
    main()