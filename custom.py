import base64
import termcolor
import datetime
import re
def decimal_to_ip_address(x):
    # new empty string for ip address
    ip = ""
    # loop for the four octets
    for i in range(4):
        # variable to hold the binary ip
        ip1=""
        # loop through each bit of the octet
        for j in range(8):
            # modulo to convert to binary and add to variable 
            ip1= str(x %2)+ip1
            # shift the bits to the right to work on the next digit
            x = x >> 1
        # convert binary back to int adding decimal concatenating each loop
        ip = str(int(ip1,2))+ "." + ip
    # return ip after stripping off tailing .
    return ip.strip(".")
def decimal_to_utc_timestamp(y):
    # change bytes to hex and then to int (base 16 to base 10)
    ts = int(y.hex(),16)
    # convert decimal to datetime object utc and save as string
    utc_ts = str(datetime.datetime.fromtimestamp(ts,datetime.timezone.utc))
    return utc_ts

# open binary file
with open('custom.sky', 'rb') as f:
    data = f.read()
    
    # code to get header information and set cursor locations
    magic_bytes = data[0:8].hex()
    version_number =data[8]
    timestamp = data[9:13].hex()
    decimal_timestamp =int(timestamp, 16)
    datetime_timestamp= datetime.datetime.fromtimestamp(decimal_timestamp, datetime.timezone.utc)
    hostname_length = int(data[13:17].hex(), 16)
    hostname = data[17:17+hostname_length].decode('utf=8')
    end_of_hostname= 17+hostname_length
    flag_length= int(data[end_of_hostname:end_of_hostname+4].hex(), 16)
    end_of_flag_len=end_of_hostname+4
    
    flag = base64.b64decode(data[end_of_flag_len:end_of_flag_len+flag_length]).decode('utf-8')
    start_of_num_entries = end_of_flag_len+flag_length
    num_entries = int(data[start_of_num_entries:start_of_num_entries+4].hex(), 16)
    end_of_header = start_of_num_entries+4
    # remove the header and create list of lists, one for each of the 162 entries
    body = data[end_of_header:]
    # create list of lists 
    list_of_lists = []
    cursor = 0
    for i in range(0,num_entries):
        temp_list= []
        source_ip = body[cursor:cursor+4]
        cursor +=4
        dest_ip = body[cursor:cursor+4]
        cursor +=4
        timestamp_log= body[cursor:cursor+4]
        cursor +=4
        if i != 162:
            bytes_transferred = body[cursor:cursor+4]
            cursor += 4
        else:
            bytes_transferred = body[cursor:]
        temp_list.append(decimal_to_ip_address(int(source_ip.hex(),16)))
        temp_list.append(decimal_to_ip_address(int(dest_ip.hex(),16)))
        temp_list.append(decimal_to_utc_timestamp(timestamp_log))
        temp_list.append(int(bytes_transferred.hex(), 16))
        list_of_lists.append(temp_list)
print(termcolor.colored("[+] magic bytes ",'green') + magic_bytes)
print(termcolor.colored("[+] version number ",'green') + str(version_number))
print(termcolor.colored("[+] utc timestamp ", 'green') + str(datetime_timestamp))
print(termcolor.colored("[+] hostname len ",'green')+ str(hostname_length))
print(termcolor.colored("[+] hostname ",'green') + hostname)
print(termcolor.colored("[+] flag length ", 'green')+ str(flag_length))
print(termcolor.colored("[+] flag ", 'green') + flag)
print(termcolor.colored("[+] number of entries ", 'green') + str(num_entries))
total_bytes = 0
for list in list_of_lists:
    total_bytes += list[3]
print(termcolor.colored("[+] total_bytes transferred ",'green')+ str(total_bytes))
# create a list of all ip addresses senders and recievers and create list with unique ips and count
ip_addresses =[]
for list in list_of_lists:
    ip_addresses.append(list[0])
    ip_addresses.append(list[1])

unique_ips = []
for y in ip_addresses:
    if y not in unique_ips:
        unique_ips.append(y)
print(termcolor.colored("[+] total unique ip addresses (senders and recievers) ", 'green')+ str(len(unique_ips)))
# get tally of total bytes from each ip in unique 
total_bytes_dict = {}
for unique in unique_ips:
    total_bytes_dict[unique] = 0
for list in list_of_lists:
    for unique in unique_ips:
        if unique == list[0]:
          total_bytes_dict[unique] += list[3]
highest_bytes_transferred = 0
ip_with_highest_bytes_transferred = ""
for key in total_bytes_dict.keys():
    if total_bytes_dict[key] > highest_bytes_transferred:
        highest_bytes_transferred = total_bytes_dict[key]
        ip_with_highest_bytes_transferred = key


print(termcolor.colored('[+] ip with most bytes transferred ', 'green' )+ f"{ip_with_highest_bytes_transferred}" + termcolor.colored(" total bytes ", 'green')+f"{highest_bytes_transferred}")

# busiest day with most bytes transferred
# create list of unique dates, create dictionary of dates with keys dates values total bytes
date_list = []
unique_date_list = []
for list in list_of_lists:
    day = re.search(r"(\d+-\d+-\d+).*?", list[2])
    date_list.append(day.group(1))
for date in date_list:
    if date not in unique_date_list:
        unique_date_list.append(date) 
bytes_per_day = {}
for date in unique_date_list:
    bytes_per_day[date] = 0

for list in list_of_lists:
    for unique_date in unique_date_list:
         day = re.search(r"(\d+-\d+-\d+).*?", list[2])
         if day:
            extracted_day = day.group(1)
            if unique_date == extracted_day:
                bytes_per_day[unique_date] += list[3] 

day_with_highest_bytes_transferred = ""
busiest_day_bytes_transferred = 0
for key in bytes_per_day.keys():
    if bytes_per_day[key] > busiest_day_bytes_transferred:
        busiest_day_bytes_transferred = bytes_per_day[key]
        day_with_highest_bytes_transferred = key     

print(termcolor.colored('[+] busiest date ', 'green' )+ f"{day_with_highest_bytes_transferred}" + termcolor.colored(" total bytes ", 'green')+f"{busiest_day_bytes_transferred}")
    