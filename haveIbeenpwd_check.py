
import time
import requests

########################
# Requires requests
# Requires time
#########################
base_url = "https://haveibeenpwned.com/api/v2/breachedaccount/"
end_url = "?truncateResponse=true"  # remove this if you want more info about the breaches
input_filename = "emails.txt"


def count_lines(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def my_strip(s, chars):
    return ''.join(c for c in s if c not in chars).split(",")

def check_email(email):
    full_url = base_url + email.strip("\n") + end_url
    try:
        response = requests.get(url=full_url)
        if "429" in response:
            print("[-] Rate limit reached, sleeping for 3 seconds before retrying")
            time.sleep(3)
            check_email(email)
        else:
            res = str([s.replace("Name:", "") for s in my_strip(response.content.decode(), '"[]{}')])
            if res != "['']":
                print(email.strip('\n') + ' | Breaches: ' + res)
    except Exception as e:
        print("[-] ERROR when processing email: "+email+".\n Error: " + e)


def main():
    print("[!] The script sleeps for 1600 ms between calls to comply with rate limiting")
    nb_lines = count_lines(input_filename)
    print("[!] Approximate total duration: " + str(int(nb_lines) * 1.6) + "s. (" + str(nb_lines) + " emails)")
    print("[+] Starting: ")
    with open(input_filename, 'r') as emails_list:
        for email in emails_list:
            check_email(email)
            time.sleep(1.60)
        print("[+] All done.")

if __name__ == "__main__":
    main()
