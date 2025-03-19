import os, sys, struct, binascii
import math, time
from datetime import datetime, timedelta


def Perfact_Reverse_forfloat_encoding(hex_str, debug=False):
    # 把十六进制字符串倒过来分组逆序后= 14f1bf71 newstr= 71bff114
    # 每两个字符分组
    if isinstance(hex_str, bytes):
        if debug:
            print("输入的是bytes")
        hex_str = binascii.hexlify(hex_str).decode()
    else:
        if debug:
            print("输入的不是bytes")
    hex_str_groups = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = "".join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += "0"
    return hex_str_reversed


def perfact_hex2float(hex_str, debug=False):
    if debug:
        print("welcomeperfact_hex2float")
    if isinstance(hex_str, bytes):
        if debug:
            print("输入的是bytes")
        hex_str = binascii.hexlify(hex_str).decode()
        if debug:
            print(f"输入的是bytes，最初二进制数据为{hex_str}，经过hexlify后的hex_str=", hex_str)
    else:
        if debug:
            print("输入的不是bytes")

    hex_str = Perfact_Reverse_forfloat_encoding(hex_str)

    if debug:
        print(f"转换类似“4479fff0”这样的十六进制字符串为浮点数,参数为：{hex_str}")
    # hex_str= 4479fff0
    int_value = int(hex_str, 16)
    if debug:
        print("int_value=", int_value)
    a = struct.pack(">I", int_value)
    if debug:
        print("a=", a)
    b = struct.unpack(">f", a)
    f = b[0]
    if debug:
        print("perfact_hex2float, result=", f)
    return f


def wm_hex_to_date(hex_str, debug=False):
    # ['ED', '8B', '34', '01']
    if debug:
        print("welcome wm_hext-date,输入参数为：", hex_str)
    if isinstance(hex_str, bytes):
        if debug:
            print("输入的是bytes")
        hex_str = binascii.hexlify(hex_str).decode()
        print(f"输入的是bytes，最初二进制数据为{hex_str}，经过hexlify后的hex_str=", hex_str)
    else:
        if debug:
            print("输入的不是bytes")

    reversed_hex = Perfact_Reverse_forfloat_encoding(hex_str, debug=debug)

    if debug:
        print("result=", reversed_hex, type(reversed_hex))
    if debug:
        print("reversed_hex=", reversed_hex)
    reversed_hex = str(reversed_hex)
    date = int(reversed_hex, 16)  # 将十六进制字符串转换为整数
    date_str = str(date)

    return date_str


def wm_hex_to_date_str(hex_str):
    hex_str = hex_str[::-1]  # 反转列表中的元素顺序=

    date = int(hex_str, 16)  # 将十六进制字符串转换为整数
    date_str = str(date)

    # 在需要的位置插入分隔符，例如 "20220909" 转换为 "2022-09-09"
    date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    return date_str


def wm_float_to_hex(f):
    # print("welcome to wm_float_to_hex, input f=", f)
    # 将浮点数转换为十六进制字符串
    hex_str = hex(struct.unpack(">I", struct.pack(">f", f))[0])[2:]

    # 每两个字符分组
    hex_str_groups = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = "".join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += "0"

    # 将十六进制字符串转换为二进制数据
    binary = bytes.fromhex(hex_str_reversed)
    # 如果二进制数据长度小于4字节，进行左填充零字节，使长度保持为4字节
    if len(binary) < 4:
        binary = b"\x00" * (4 - len(binary)) + binary

    return binary


def decode_tdx_binary_data(binary_data, debug=False):
    decoded_data = []
    for i in range(0, len(binary_data), 8):
        # 每批8字节，每次4字节，分2部分解析
        # 解析日期
        date_bytes = binary_data[i : i + 4]
        if debug:
            print("tdx start, original date_bytes=", date_bytes)  # b'\xe5\x8b4\x01'
        dateint = wm_hex_to_date(date_bytes, debug=debug)
        if debug:
            print("int_date_==", dateint)
        decoded_data.append(dateint)
        # 解析定点数

        fixed_point_bytes = binary_data[i + 4 : i + 8]
        if debug:
            print("original fixed_point_bytes=", fixed_point_bytes)
        hex_string = "".join([f"{byte:02x}" for byte in fixed_point_bytes])
        if debug:
            print("converted hex=", hex_string)  # 00008040，顺序同二进制存放，所以要先分组逆序
        resvered_hex_string = Perfact_Reverse_forfloat_encoding(hex_string, debug=debug)
        if debug:
            print("resvered hex string = ", resvered_hex_string)

        end_number = perfact_hex2float(resvered_hex_string, debug=debug)
        if debug:
            print("result=", result)
        decoded_data.append(round(end_number, 3))

    return decoded_data


def 反日期(hex_str):
    # 把十六进制字符串倒过来分组逆序后= 14f1bf71 newstr= 71bff114
    # 每两个字符分组
    hex_str_groups = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = "".join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += "0"
    return hex_str_reversed


def date_to_hex(date_str):
    date_int = int(date_str)
    hex_code = hex(date_int)[2:].zfill(8).upper()  # 将日期转换为十六进制并填充为8位
    hex_code = "".join([hex_code[i : i + 2] for i in range(6, -2, -2)])  # 逆序每两个字符分组
    binary_data = bytes.fromhex(hex_code)
    return binary_data


def tdx_signal_file_name(code, tdx_path=r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999"):
    market = int(code.startswith("6"))
    tdx_signal_file_name = tdx_path + f"/{market}_{code}.dat"
    return tdx_signal_file_name


def read_tdx_signal(code, tdx_path=r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999", debug=False):
    market = int(code.startswith("6"))
    tdx_file = os.path.join(tdx_path, f"{market}_{code}.dat")
    print("tdx_file=", tdx_file)
    # 生成文件路径

    with open(tdx_file, "rb") as file:
        # 读取原始数据
        binary_data = file.read()
        print("读取的通达信文件的原始数据：")
        print(binary_data)
        result = decode_tdx_binary_data(binary_data, debug=False)
        print("result=", result)
        return result


def get_file_modified_datetime(file_path):
    import time

    # 获取文件的修改时间戳
    timestamp = os.path.getmtime(file_path)

    # 将时间戳转换为时间元组
    modified_time = time.localtime(timestamp)

    # 提取日期和小时
    date = int(time.strftime("%Y%m%d", modified_time))
    hour = modified_time.tm_hour

    return date, hour


def get_lastdate_tdx_sinal(code, signal=999, tdx_path=r"D:\SOFT\_Stock\Tdx_202311", debug=False):
    # D:\Soft\_Stock\Tdx_202311\T0002\signals\signals_user_999\0_000001.dat
    # print("enter get_lastdate_tdx_sinal")
    market = int(code.startswith("6"))
    tdx_file = os.path.join(tdx_path, rf"T0002\signals\signals_user_{signal}", f"{market}_{code}.dat")
    # print("xxtdx_file=", tdx_file)
    if not os.path.isfile(tdx_file):
        return None

    file_size = os.path.getsize(tdx_file)
    if file_size == 0:
        return None
    # print("openfile")
    with open(tdx_file, "rb+") as file:
        # print("try seek to last, file_size=", file_size)
        file.seek(-8, os.SEEK_END)
        # print("try to read")
        last_8_bytes = file.read(8)
        # print("last_8_bytes=", last_8_bytes)
        result = decode_tdx_binary_data(last_8_bytes, debug=debug)
        # ['20231101', 0.3]
        date_int_to_return = int(result[0])

        if result:
            file_modify_date, file_modify_hour = get_file_modified_datetime(tdx_file)
            modifty_and_not_complete = date_int_to_return == file_modify_date and file_modify_hour < 15
            if not modifty_and_not_complete:
                return date_int_to_return
            else:
                print("message from get_lastdate_tdx_sinal: file not complete, try to del current and read ahead")
                file.seek(-8, os.SEEK_END)
                file.truncate()
                file.seek(-8, os.SEEK_END)
                last_8_bytes = file.read(8)
                date_int_to_return, _ = decode_tdx_binary_data(last_8_bytes, debug=debug)
                return date_int_to_return


import lyytools


@lyytools.get_time  # 单日期写一次，时间多0.2
def add_data_if_new_than_local(target_tdxfile, data_dict, lastdateint, debug=False):
    # print("enter add_data_if_new_than_local")
    full_item_bin = b""
    for key in data_dict.keys():
        # print("debug:", key, lastdateint)
        if int(key) > lastdateint:
            # print("new data enter")
            date_bin = date_to_hex(key)
            cg_bin = wm_float_to_hex(data_dict[key])
            # print("add new data. date_bin=",date_bin,",cg_bin=",cg_bin)

            # print("recovery date,<<<<<", wm_hex_to_date(date_bin,debug=debug))
            # print("recovery cg=======",perfact_hex2float(cg_bin))
            full_item_bin += date_bin + cg_bin

    if os.path.exists(target_tdxfile):  # 检查文件是否存在
        open_mode = "ab"
    else:
        print("File does not exist. Creating new file.")
        open_mode = "wb"

    with open(target_tdxfile, open_mode) as file:  # 创建新文件并写入数据
        file.write(full_item_bin)


def cyminiute_reader(tdx_path, code):
    market_dict = {0: "sz", 1: "sh"}
    market_code = int(code.startswith("6"))
    mark = market_dict[market_code]
    fname = f"lyy{mark}{code}.lc1"
    ofile = open(tdx_path + os.sep + fname, "rb")
    print("ofile=", ofile)
    buf = ofile.read()
    ofile.close()

    num = len(buf)
    no = num / 32
    b = 0
    e = 32

    t = datetime.strptime("2012-11-11 00:00:00", "%Y-%m-%d %H:%M:%S")

    for i in range(int(no)):
        # a=unpack('IIIIIfII',buf[b:e])
        a = struct.unpack("HHfffffii", buf[b:e])

        year = math.floor(a[0] / 2048) + 2004
        month = math.floor((a[0] % 2048) / 100)
        day = (a[0] % 2048) % 100
        hm = (t + timedelta(minutes=a[1])).strftime("%H:%M")
        line = str(year) + "{:02}".format(month) + "{:02}".format(day) + "," + hm + "," + "{:.2f}".format(a[2]) + "," + "{:.2f}".format(a[3]) + "," + "{:.2f}".format(a[4]) + "," + "{:.2f}".format(a[5]) + "," + "{:.2f}".format(a[6]) + "," + str(a[7]) + "\n"

        # line = str(year)+'{:02}'.format(month)+'{:02}'.format(day)+','+str(a[1])+','+'{:.2f}'.format(a[2])+','+'{:.2f}'.format(a[3])+','+'{:.2f}'.format(a[4])+','+'{:.2f}'.format(a[5])+','+'{:.2f}'.format(a[6])+','+str(a[7])+'\n'
        # line =str(a[0]) +','+str(a[1])+','+'{:.2f}'.format(a[2])+','+'{:.2f}'.format(a[3])+','+'{:.2f}'.format(a[4])+','+'{:.2f}'.format(a[5])+','+'{:.2f}'.format(a[6])+','+str(a[7])+'\n'
        print(line)
        b = b + 32
        e = e + 32


def minute_writer(tdx_path, code, data):
    market_dict = {0: "sz", 1: "sh"}
    market_code = int(code.startswith("6"))
    mark = market_dict[market_code]
    fname = f"lyy{mark}{code}.lc1"
    fname = tdx_path + os.sep + fname

    print("flname=", fname)

    if os.path.isfile(fname):
        mode = "wb"

    with open(fname, "wb") as f:
        for _, row in df.iterrows():
            year, month, day = row["date"].year, row["date"].month, row["date"].day
            a0 = (year - 2004) * 2048 + month * 100 + day
            time = datetime.strptime(row["time"], "%H:%M")
            a1 = time.hour * 60 + time.minute
            a2, a3, a4, a5, a6 = row["open"], row["high"], row["low"], row["close"], row["amount"]
            a7 = int(row["vol"])
            # print( a0, a1, a2, a3, a4, a5, a6, a7)
            buf = struct.pack("HHfffffixxxx", a0, a1, a2, a3, a4, a5, a6, a7)
            # print(buf,len(buf))
            f.write(bytearray(buf))
            # print(bytearray(buf), len(bytearray(buf)))


def dayfile_from_vipdoc(tdx_vipdoc_path, code, debug=False):
    market_dict = {0: "sz", 1: "sh"}
    market_code = int(code.startswith("6"))
    mark = market_dict[market_code]
    fname = f"{mark}{code}.day"
    fname = tdx_vipdoc_path + os.sep + mark + os.sep + "lday" + os.sep + fname

    if debug:
        print("flname=", fname)
    return fname


def get_lastdate_from_dayline(dayfile, debug=False):
    file_size = os.path.getsize(dayfile)
    with open(dayfile, "rb") as f:
        f.seek(file_size - 32)
        last_8_bytes = f.read(4)
        result = wm_hex_to_date(last_8_bytes, debug=debug)
        print("inget_lastdate_from_dayline, result=", result)
        return result


def get_lastdate_from_dayline_remove_notfull(dayfile, remove_notfull=True, debug=False):
    file_size = os.path.getsize(dayfile)
    localtime = time.localtime(os.path.getmtime(dayfile))
    last_modified_int = int(time.strftime("%Y%m%d", localtime))
    with open(dayfile, "rb") as f:
        f.seek(file_size - 32)
        last_8_bytes = f.read(4)
        lastdate_in_dayfile = wm_hex_to_date(last_8_bytes, debug=debug)
        print("inget_lastdate_from_dayline, result=", result)
    if last_modified_int == int(lastdate_in_dayfile) and localtime.tm_min < 15:
        print("文件时间不可信，删除最后32字节")
        with open(dayfile, "rb+") as f:
            f.seek(-32, os.SEEK_END)
            f.truncate()
        return get_lastdate_from_dayline_remove_notfull(dayfile, remove_notfull=True)


# day, time,o,h,l,c,a,v,
def df_to_dayline(df, binary_file_name):
    # code = "000001"
    # tdx_vipdoc_path = f"D:/Soft/_Stock/通达信开心果202310/vipdoc"
    # dayfile = dayfile_from_vipdoc(tdx_vipdoc_path, code)
    binary_data_list = []
    for _, row in df.iterrows():
        rowdate = row["date"]
        if isinstance(rowdate, rowdate):
            日期 = int(rowdate.strftime("%Y%m%d"))
        elif isinstance(rowdate, str):
            日期 = int(datetime.strptime(row["date"], "%Y-%m-%d").strftime("%Y%m%d"))
        else:
            print("else", type(rowdate))
        if not 日期 == 20231108:
            continue
        print(rowdate)
        # print(', '.join(map(str, row.values)))

        开盘价 = int(row["open"] * 100)
        最高价 = int(row["high"] * 100)
        最低价 = int(row["low"] * 100)
        收盘价 = int(row["close"] * 100)
        成交额 = int(row["amount"])
        成交量 = int(row["vol"])
        前日收盘价 = 65536
        # 前日收盘价 = 0
        print("beforew=", 日期, 开盘价, 最高价, 最低价, 收盘价, 成交额, 成交量, 前日收盘价)
        # 打包所有的数据为一个二进制字符串
        binary_data = struct.pack("IIIIIfII", 日期, 开盘价, 最高价, 最低价, 收盘价, 成交额, 成交量, 前日收盘价)
        binary_data_list.append(binary_data)
    print(binary_data_list)
    # 一次性写入到文件中
    with open(binary_file_name, "wb") as f:
        f.writelines(binary_data_list)


if __name__ == "__main__":
    print("tdxadd=", wm_hex_to_date("00000100"))
    print("result= ", perfact_hex2float("00000100"))
    print("65536二进制为", wm_float_to_hex(65536))
    print(date_to_hex("20220901"))
    path = r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999"
    code = "000001"
    print(get_lastdate_tdx_sinal(code))
    sys.exit()

    # in_day_file = "f0ff7944"

    # hex_str_reversed = Perfact_Reverse_forfloat_encoding(in_day_file)

    # print("sample 1",hex_str_reversed)

    # print(perfact_hex2float(hex_str_reversed))

    # print("-"*40)
    print("sample 2 通达信数据读取")
    path = r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999"
    code = "000001"
    market = int(code.startswith("6"))
    tdx_file = path + f"/{market}_{code}.dat"
    print("tdx file= ", tdx_file)
    with open(tdx_file, "rb") as file:
        # 读取原始数据
        binary_data = file.read()
        print("读取的通达信文件的原始数据：")
        print(binary_data)
        result = decode_tdx_binary_data(binary_data)
        print("result=", result)
