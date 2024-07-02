import mxc_utils
import json
import requests
import sys



def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <event json filename>")
        return

    events_json_name = sys.argv[1]
    with open(events_json_name, "r") as f:
        event = json.loads(f.read())
    url = mxc_utils.http_url_from_event(event)
    resp = requests.get(url)
    filename = mxc_utils.get_filename_from_event(event)
    if not mxc_utils.is_encrypted_file(event):
        with open(filename, "wb") as f:
            f.write(resp.content)
        print(f"File was unencrypted, saved as {filename}")
        return
    data = mxc_utils.decrypt_buffer(event, resp.content)
    with open(filename, "wb") as f:
        f.write(data)
    print(f"File was encrypted, saved as {filename}")



if __name__ == "__main__":
    main()