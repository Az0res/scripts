import shodan
import sys
import datetime

SHODAN_API_KEY = "YOUR API KEY HERE"
api = shodan.Shodan(SHODAN_API_KEY)

# uncomment this and comment the following if you want the query to be passed by argument to the progam
# querystr = sys.argv[1]
querystr = "QUERY HERE"

# available fields (not a full list, it depends on the query):
# os, org, asn, domains, data, ip_str, hostnames, _shodan, timestamp, location, transport, port, isp
# more info on possible field when  decommenting the line "print(str(result) + "\n")"
needed_fields = ['os', 'devicetype', 'product', 'info', 'org', 'asn', 'hostnames', 'isp', 'data']


def write_headers(out, results):
    out.write(
        'Results found: %s' % results['total'] + ". Time of the query: " + str(datetime.datetime.now()) + "\nFormat: ")
    for field in needed_fields:
        out.write(field + ", ")
    out.write("\n\n")


def main(argv):
    try:
        with open("output.txt", "w") as out:
            # Search Shodan
            results = api.search(querystr)

            write_headers(out, results)
            # Show the results
            for result in results['matches']:

                if 'SMB Version: 1' in result['data']:  # TODO adapt this if
                    out.write('IP: %s' % result['ip_str'] + ", ")

                for field in needed_fields:
                    if field in result:
                        out.write(field + ": " + str(result[field]).replace('\n', '\\n ') + ", ")

                out.write("\n")
                # print(str(result) + "\n")
    except shodan.APIError as e:
        print('Error: %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
