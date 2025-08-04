import serial
import time

class RM550Controller:
    """
    用于控制 RM550 程控电阻模块的 Python 类。
    通过串口发送 AT 指令并解析响应。
    """

    def __init__(self, port, baudrate=115200, timeout=1):
        """
        初始化 RM550 控制器。

        Args:
            port (str): 串口端口名称 (例如: 'COM1' 或 '/dev/ttyUSB0')。
            baudrate (int): 波特率，默认为 115200。
            timeout (int): 串口读取超时时间 (秒)，默认为 1 秒。
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port = None

    def _open_serial(self):
        """尝试打开串口连接。"""
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=8,
                timeout=self.timeout
            )
            if self.serial_port.is_open:
                print(f"成功打开串口: {self.port}")
                # 清除可能存在的串口缓冲
                self.serial_port.flushInput()
                self.serial_port.flushOutput()
                return True
            return False
        except serial.SerialException as e:
            print(f"错误: 无法打开串口 {self.port} - {e}")
            self.serial_port = None
            return False

    def connect(self):
        """建立与 RM550 模块的串口连接。"""
        if self.serial_port and self.serial_port.is_open:
            print("串口已连接。")
            return True
        return self._open_serial()

    def disconnect(self):
        """断开与 RM550 模块的串口连接。"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("串口已断开。")
            self.serial_port = None
            return True
        return False

    def _send_at_command(self, command, expected_ok=True, response_prefix=None, custom_sn=None):
        """
        发送 AT 指令并等待模块响应。

        Args:
            command (str): 要发送的 AT 指令 (不包含结束符)。
            expected_ok (bool): 是否期望返回 '+OK.'，默认为 True。
            response_prefix (str, optional): 期望响应的前缀，用于解析特定数据。
            custom_sn (str, optional): 可选的序列号，用于 'AT+XXX@<S/N>' 形式的指令。

        Returns:
            str: 模块的响应字符串，如果超时或出错则返回 None。
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("错误: 串口未打开。请先调用 .connect() 方法。")
            return None

        full_command = command
        if custom_sn:
            full_command = f"{command}@{custom_sn}"

        # 尝试使用 '\r' 作为结束符，因为文档提到了 '\r' 或 '\n'
        # 实际测试中，使用 '\r\n' 兼容性最好，但文档指定 '\r' 或 '\n' 或 '/' 或 '\'
        # 为了兼容性，我们只发送指令，然后让模块自己处理其认可的结束符。
        # 这里我们按照通常的AT指令习惯，补上 \r\n。如果模块只认 \r 或 \n，
        # 则需要在发送时只加一个。但考虑到文档中指令结尾是 \r 或 \n 或字符’/’ 或字符’\’，
        # 我们可以只发送指令本身，让模块自己识别。
        # 但通常约定是 \r\n，所以这里我们用 \r\n
        cmd_bytes = (full_command + '\r\n').encode('ascii') # 大多数AT模块使用ASCII编码

        try:
            self.serial_port.write(cmd_bytes)
            # print(f"发送: {cmd_bytes.decode().strip()}") # 调试用

            response_buffer = b''
            start_time = time.time()

            # 读取直到超时或接收到预期响应的一部分
            while time.time() - start_time < self.timeout:
                if self.serial_port.in_waiting > 0:
                    response_buffer += self.serial_port.read(self.serial_port.in_waiting)

                    # 检查是否接收到完整的行结束符或特定响应前缀
                    # 文档指出响应是 +OK. 或 +RES.SP=xxx 等，通常以 \r\n 结尾
                    if b'\r\n' in response_buffer or \
                       (response_prefix and response_prefix.encode('ascii') in response_buffer) or \
                       (expected_ok and b'+OK.' in response_buffer):
                        break
                time.sleep(0.01) # 短暂延时，避免CPU空转

            response_str = response_buffer.decode('ascii', errors='ignore').strip()
            # print(f"接收: {response_str}") # 调试用

            if expected_ok and "+OK." not in response_str:
                print(f"警告: 指令 '{command}' 未返回 '+OK.'。 接收到: '{response_str}'")
                return None

            if response_prefix:
                if response_prefix in response_str:
                    return response_str
                else:
                    print(f"警告: 指令 '{command}' 未找到预期前缀 '{response_prefix}'。接收到: '{response_str}'")
                    return None

            return response_str

        except serial.SerialException as e:
            print(f"串口通信错误: {e}")
            return None
        except Exception as e:
            print(f"发送AT指令时发生未知错误: {e}")
            return None

    ## --- ① 基础指令 ---
    def connect_main_path_relay(self, sn=None):
        """
        干路 OPEN 继电器闭合。
        注：OPEN 继电器为常开（Normal Open），因此需要在每次上电后将之闭合才能正常输出电阻。
        """
        return self._send_at_command("AT+RES.CONNECT", custom_sn=sn)

    def disconnect_main_path_relay(self, sn=None):
        """
        干路 OPEN 继电器断开。
        注：该指令实现输出电阻开路。
        """
        return self._send_at_command("AT+RES.DISCONNECT", custom_sn=sn)

    def connect_short_relay(self, sn=None):
        """
        干路 SHORT 继电器闭合。
        注：该指令仅仅将 SHORT 继电器闭合。要实现输出电阻短路，必须将 OPEN 继电器也闭合。
        """
        return self._send_at_command("AT+RES.SHORT", custom_sn=sn)

    def disconnect_short_relay(self, sn=None):
        """
        干路 SHORT 继电器断开。
        注：该指令将 SHORT 继电器断开，恢复常态。
        """
        return self._send_at_command("AT+RES.UNSHORTEN", custom_sn=sn)

    def query_setpoint_resistance(self, sn=None):
        """
        查询当前设定的目标电阻值 (SP)。

        Returns:
            float or None: 设定的电阻值 (Ω)，如果失败则返回 None。
        """
        response = self._send_at_command("AT+RES.SP?", expected_ok=False, response_prefix="+RES.SP=", custom_sn=sn)
        if response:
            try:
                # 示例: +RES.SP=100.000
                value_str = response.split('=')[-1].strip()
                return float(value_str)
            except (ValueError, IndexError):
                print(f"错误: 无法解析 SP 查询响应: {response}")
        return None

    def set_setpoint_resistance(self, resistance, sn=None):
        """
        设置目标电阻值 (SP)。

        Args:
            resistance (float or int): 要设置的电阻值 (Ω)。

        Returns:
            dict or None: 包含设置后SP, PV, UMax, RLimit, TAmb 的字典，如果失败则返回 None。
        """
        command = f"AT+RES.SP={resistance}"
        response = self._send_at_command(command, expected_ok=True, custom_sn=sn)
        return self._parse_multi_line_response(response)

    def increase_setpoint_resistance(self, increment, sn=None):
        """
        递增目标电阻值 (SP)。

        Args:
            increment (float or int): 要增加的电阻值 (Ω)。

        Returns:
            dict or None: 包含设置后SP, PV, UMax, RLimit, TAmb 的字典，如果失败则返回 None。
        """
        command = f"AT+RES.SP+={increment}"
        response = self._send_at_command(command, expected_ok=True, custom_sn=sn)
        return self._parse_multi_line_response(response)

    def decrease_setpoint_resistance(self, decrement, sn=None):
        """
        递减目标电阻值 (SP)。

        Args:
            decrement (float or int): 要减少的电阻值 (Ω)。

        Returns:
            dict or None: 包含设置后SP, PV, UMax, RLimit, TAmb 的字典，如果失败则返回 None。
        """
        command = f"AT+RES.SP-={decrement}"
        response = self._send_at_command(command, expected_ok=True, custom_sn=sn)
        return self._parse_multi_line_response(response)

    def query_min_output_limit(self, sn=None):
        """
        查询最小输出限制值 (RLIMIT)。

        Returns:
            float or None: 最小输出限制值 (Ω)，如果失败则返回 None。
        """
        response = self._send_at_command("AT+RES.RLIMIT?", expected_ok=False, response_prefix="+RES.RLIMIT=", custom_sn=sn)
        if response:
            try:
                # 示例: +RES.RLIMIT=0.0
                value_str = response.split('=')[-1].strip()
                return float(value_str)
            except (ValueError, IndexError):
                print(f"错误: 无法解析 RLIMIT 查询响应: {response}")
        return None

    def set_min_output_limit(self, limit, sn=None):
        """
        设置最小输出限制值 (RLIMIT)。

        Args:
            limit (float or int): 要设置的最小电阻限制值 (Ω)。

        Returns:
            dict or None: 包含设置后SP, PV, UMax, RLimit, TAmb 的字典，如果失败则返回 None。
        """
        command = f"AT+RES.RLIMIT={limit}"
        response = self._send_at_command(command, expected_ok=True, custom_sn=sn)
        return self._parse_multi_line_response(response)

    def get_ambient_temperature(self, sn=None):
        """
        获取环境温度。

        Returns:
            float or None: 环境温度 (°C)，如果失败则返回 None。
        """
        response = self._send_at_command("AT+RES.T_AMBIENT?", expected_ok=False, response_prefix="+RES.T_AMBIENT=", custom_sn=sn)
        if response:
            try:
                # 示例: +RES.T_AMBIENT=27.84
                value_str = response.split('=')[-1].replace('C', '').strip() # 移除单位
                return float(value_str)
            except (ValueError, IndexError):
                print(f"错误: 无法解析环境温度响应: {response}")
        return None

    def get_output_resistance_info(self, sn=None):
        """
        获取输出电阻详细信息。

        Returns:
            dict or None: 包含 SP, PV, UMax, RLimit, TAmb, TCal 的字典。
        """
        response = self._send_at_command("AT+RES.INFO?", expected_ok=False, response_prefix="+RES.INFO:", custom_sn=sn)
        if response:
            data = {}
            # 示例响应:
            # +RES.INFO:
            # .SP(R)=200.000
            # .PV(R)=500.200
            # ...
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if '.SP(R)=' in line: data['SP(R)'] = float(line.split('=')[-1])
                elif '.PV(R)=' in line: data['PV(R)'] = float(line.split('=')[-1])
                elif '.UMax(V)=' in line: data['UMax(V)'] = float(line.split('=')[-1])
                elif '.RLimit(R)=' in line: data['RLimit(R)'] = float(line.split('=')[-1])
                elif '.TAmb(C)=' in line: data['TAmb(C)'] = float(line.split('=')[-1])
                elif '.TCal(C)=' in line: data['TCal(C)'] = float(line.split('=')[-1])
            return data
        return None

    ## --- ① 模块信息查询 ---
    def query_relay_usage_count(self, sn=None):
        """
        查询继电器使用次数。

        Returns:
            int or None: 继电器使用次数，如果失败则返回 None。
        """
        response = self._send_at_command("AT+DEV.RL_CNT?", expected_ok=False, response_prefix="+DEV.RL_CNT=", custom_sn=sn)
        if response:
            try:
                # 示例: +DEV.RL_CNT=100
                value_str = response.split('=')[-1].strip()
                return int(value_str)
            except (ValueError, IndexError):
                print(f"错误: 无法解析继电器使用次数响应: {response}")
        return None

    def query_error_code(self, sn=None):
        """
        查询错误代码。

        Returns:
            str or None: 错误代码字符串，例如 '<null>'。
        """
        response = self._send_at_command("AT+DEV.ERRCODE?", expected_ok=False, response_prefix="+DEV.ERRCODE=", custom_sn=sn)
        if response:
            try:
                # 示例: +DEV.ERRCODE=<null>
                return response.split('=')[-1].strip()
            except IndexError:
                print(f"错误: 无法解析错误代码响应: {response}")
        return None

    def query_module_info(self, sn=None):
        """
        查询模块综合信息。

        Returns:
            dict or None: 包含模块信息的字典。
        """
        response = self._send_at_command("AT+DEV.INFO?", expected_ok=False, response_prefix="+DEV.INFO:", custom_sn=sn)
        if response:
            data = {}
            # 示例响应:
            # +DEV.INFO:
            # .SN=00000003
            # .TYPE=RM550-1M2-R1
            # ...
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if '.SN=' in line: data['SN'] = line.split('=')[-1].strip()
                elif '.TYPE=' in line: data['TYPE'] = line.split('=')[-1].strip()
                elif '.PRDSTEP=' in line: data['PRDSTEP'] = line.split('=')[-1].strip()
                elif '.FW=' in line: data['FW'] = float(line.split('=')[-1])
                elif '.HW=' in line: data['HW'] = float(line.split('=')[-1].replace('H', '')) # 移除 'H'
                elif '.TCR(ppm)=' in line: data['TCR(ppm)'] = int(line.split('=')[-1])
                elif '.PWR(W)=' in line: data['PWR(W)'] = float(line.split('=')[-1])
                elif '.MAXU(V)=' in line: data['MAXU(V)'] = float(line.split('=')[-1])
                elif '.PROD=' in line: data['PROD'] = line.split('=')[-1].strip()
                elif '.RL_CNT=' in line: data['RL_CNT'] = int(line.split('=')[-1])
                elif '.ERRCODE=' in line: data['ERRCODE'] = line.split('=')[-1].strip()
            return data
        return None

    def _parse_multi_line_response(self, response_str):
        """
        解析设置SP/RLIMIT等指令返回的多行响应。
        示例：
        +OK.
        +SP(R)=200.000
        +PV(R)=200.200
        +UMax(V)=19.2
        +RLimit(R)=0.0
        +TAmb(C)=28.04
        """
        if not response_str or "+OK." not in response_str:
            return None

        data = {}
        lines = response_str.split('\n')
        for line in lines:
            line = line.strip()
            if '.SP(R)=' in line: data['SP(R)'] = float(line.split('=')[-1])
            elif '.PV(R)=' in line: data['PV(R)'] = float(line.split('=')[-1])
            elif '.UMax(V)=' in line: data['UMax(V)'] = float(line.split('=')[-1])
            elif '.RLimit(R)=' in line: data['RLimit(R)'] = float(line.split('=')[-1])
            elif '.TAmb(C)=' in line: data['TAmb(C)'] = float(line.split('=')[-1])
            elif '.CalSrc=' in line: data['CalSrc'] = line.split('=')[-1].strip() # 仅限RLIMIT设置指令
        return data


# --- 使用示例 ---
if __name__ == "__main__":
    # 根据你的操作系统和模块连接的实际串口号进行修改
    # Windows: 'COMx' 例如 'COM3'
    # Linux/macOS: '/dev/ttyUSBx' 或 '/dev/ttyACMx' 例如 '/dev/ttyUSB0'
    SERIAL_PORT = '/dev/ttyUSB0'
    MODULE_SN = "00000003" # 如果你的模块支持带S/N的指令，请替换为实际的序列号

    rm550 = RM550Controller(SERIAL_PORT)

    if rm550.connect():
        print("\n--- 测试基础指令 ---")
        # 1. 干路 OPEN 继电器闭合
        print("闭合 OPEN 继电器:", rm550.connect_main_path_relay())
        time.sleep(0.1)

        # 2. 查询 SP (设置点)
        sp = rm550.query_setpoint_resistance()
        print(f"当前 SP: {sp} Ω")
        time.sleep(0.1)

        # 3. 设置 SP 为 100 Ω
        print("设置 SP 为 100 Ω...")
        response_set_sp = rm550.set_setpoint_resistance(100)
        print("设置 SP 响应:", response_set_sp)
        time.sleep(1) # 给模块一些时间响应和稳定

        # 4. 递增 SP 50 Ω
        print("递增 SP 50 Ω...")
        response_inc_sp = rm550.increase_setpoint_resistance(50)
        print("递增 SP 响应:", response_inc_sp)
        time.sleep(1)

        # 5. 递减 SP 20 Ω
        print("递减 SP 20 Ω...")
        response_dec_sp = rm550.decrease_setpoint_resistance(20)
        print("递减 SP 响应:", response_dec_sp)
        time.sleep(1)

        # 6. 查询最小输出限制值
        rlimit = rm550.query_min_output_limit()
        print(f"当前最小输出限制值 (RLIMIT): {rlimit} Ω")
        time.sleep(0.1)

        # 7. 设置最小输出限制值 为 500 Ω
        print("设置最小输出限制值 为 500 Ω...")
        response_set_rlimit = rm550.set_min_output_limit(500)
        print("设置 RLIMIT 响应:", response_set_rlimit)
        time.sleep(1)

        # 8. 获取环境温度
        temp = rm550.get_ambient_temperature()
        print(f"环境温度: {temp} °C")
        time.sleep(0.1)

        # 9. 获取输出电阻详细信息
        res_info = rm550.get_output_resistance_info()
        print("输出电阻详细信息:", res_info)
        time.sleep(0.1)

        print("\n--- 测试模块信息查询 ---")
        # 10. 查询继电器使用次数
        relay_count = rm550.query_relay_usage_count()
        print(f"继电器使用次数: {relay_count}")
        time.sleep(0.1)

        # 11. 查询错误代码
        err_code = rm550.query_error_code()
        print(f"错误代码: {err_code}")
        time.sleep(0.1)

        # 12. 查询模块综合信息
        module_info = rm550.query_module_info()
        print("模块综合信息:", module_info)
        time.sleep(0.1)

        print("\n--- 测试带序列号的指令 (如果模块支持且 S/N 正确) ---")
        # 示例：假设模块序列号是 MODULE_SN，尝试发送带 S/N 的指令
        if MODULE_SN:
            print("尝试带 S/N 闭合 OPEN 继电器...")
            response_sn = rm550.connect_main_path_relay(sn=MODULE_SN)
            print("带 S/N 闭合响应:", response_sn)
            time.sleep(0.1)

            print("尝试带 S/N 查询 SP...")
            sp_sn = rm550.query_setpoint_resistance(sn=MODULE_SN)
            print(f"带 S/N 的 SP: {sp_sn} Ω")

    else:
        print("无法连接到 RM550 模块。请检查串口配置和连接。")

    rm550.disconnect()
