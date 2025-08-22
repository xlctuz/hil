import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import crc16 # 用于计算CRC16，虽然ModbusClient通常会处理

class ZSDigitalIOModule:
    """
    中盛科技数字量输入输出模块的 Python 控制模块。
    支持 Modbus RTU 协议，通过串口与模块通信。
    """

    # 默认通信参数 [cite: 201, 202, 203, 204, 205]
    DEFAULT_SLAVE_ID = 1
    DEFAULT_BAUDRATE = 38400
    DEFAULT_BYTESIZE = 8
    DEFAULT_PARITY = 'N'  # None
    DEFAULT_STOPBITS = 1
    DEFAULT_TIMEOUT = 1.0 # 串口超时时间 (秒)

    # 寄存器地址定义 (协议地址)
    # 线圈寄存器 (可读写，控制输出) [cite: 217, 218, 220]
    COIL_OUTPUT_CONTROL_BASE = 0x0000 # 通道1控制 [cite: 221]

    # 离散输入状态寄存器 (只读，输入状态) [cite: 222, 223, 225]
    DISCRETE_INPUT_STATUS_BASE = 0x0000 # 通道1输入状态 [cite: 225]

    # 输入寄存器 (只读，输入状态，包含按位表示状态) [cite: 237, 239, 241]
    INPUT_REGISTER_STATUS_BASE = 0x0000 # 通道1输入状态 [cite: 243]
    INPUT_REGISTER_STATUS_CH1_16_BIT = 0x0032 # 按位表示通道1~16输入状态 [cite: 243]
    INPUT_REGISTER_STATUS_CH17_32_BIT = 0x0033 # 按位表示通道17~32输入状态 [cite: 244]
    INPUT_REGISTER_STATUS_CH33_48_BIT = 0x0034 # 按位表示通道33~48输入状态 [cite: 248]

    # 保持寄存器 (可读写，设置参数、输出控制模式、输出开关) [cite: 250, 251, 252, 253]
    HOLDING_REGISTER_CHANNEL_CONTROL_BASE = 0x0000 # 通道1控制模式
    HOLDING_REGISTER_COMM_DETECT_TIME = 0x0030 # 通讯检测时间设置
    HOLDING_REGISTER_ACTIVE_UPLOAD_CONTROL = 0x0031 # 输入口状态主动上传控制
    HOLDING_REGISTER_RS485_ADDRESS = 0x0032 # RS485 总线地址/站号
    HOLDING_REGISTER_BAUDRATE_SETTING = 0x0033 # 波特率设置
    HOLDING_REGISTER_BATCH_CONTROL = 0x0034 # 批量控制 (全关/全开)
    HOLDING_REGISTER_BIT_CONTROL_CH1_16 = 0x0035 # 按位控制通道1~16
    HOLDING_REGISTER_BIT_CONTROL_CH17_32 = 0x0036 # 按位控制通道17~32
    HOLDING_REGISTER_BIT_CONTROL_CH33_48 = 0x0037 # 按位控制通道33~48
    HOLDING_REGISTER_PARITY_SETTING = 0x003D # 奇偶校验设置
    HOLDING_REGISTER_CHANNEL_MODE_BASE = 0x0096 # 通道1控制模式设置 (更详细模式，如联动、点动等) [cite: 268]

    def __init__(self, port, slave_id=DEFAULT_SLAVE_ID, baudrate=DEFAULT_BAUDRATE,
                 bytesize=DEFAULT_BYTESIZE, parity=DEFAULT_PARITY,
                 stopbits=DEFAULT_STOPBITS, timeout=DEFAULT_TIMEOUT):
        """
        初始化中盛科技数字量输入输出模块控制器。

        Args:
            port (str): 串口端口名称 (例如: 'COM1' 或 '/dev/ttyUSB0')。
            slave_id (int): Modbus 从站地址 (1-255)，默认为 1。
            baudrate (int): 波特率，默认为 38400。 [cite: 202]
            bytesize (int): 数据位，默认为 8。 [cite: 203]
            parity (str): 奇偶校验 ('N'/'E'/'O')，默认为 'N' (无校验)。 [cite: 205]
            stopbits (int): 停止位，默认为 1。 [cite: 204]
            timeout (float): 串口通信超时时间 (秒)。
        """
        self.port = port
        self.slave_id = slave_id
        self.modbus_client = ModbusClient(
            host=port, # 在RTU模式下，host参数是串口名
            port=baudrate, # 在RTU模式下，port参数是波特率
            unit_id=slave_id,
            timeout=timeout,
            # RTU 模式特定的参数
            # ModbusClient 内部会处理 bytesize, parity, stopbits
            # 但如果你需要手动控制，可以在ModbusClient.serial_port初始化后设置
        )
        # 手动设置 pyModbusTCP 的 serial_port 参数
        self.modbus_client.serial_settings(
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        self.is_connected = False

    def connect(self):
        """尝试连接到 Modbus RTU 模块。"""
        if self.modbus_client.open():
            self.is_connected = True
            logger.info(f"成功连接到模块: {self.port} (ID: {self.slave_id})")
            return True
        else:
            self.is_connected = False
            logger.info(f"错误: 无法连接到模块 {self.port}")
            return False

    def disconnect(self):
        """断开与 Modbus RTU 模块的连接。"""
        if self.is_connected:
            self.modbus_client.close()
            self.is_connected = False
            logger.info("模块连接已断开。")
            return True
        return False

    def _check_connection(self):
        """内部方法：检查连接状态。"""
        if not self.is_connected:
            logger.info("错误: 模块未连接。请先调用 .connect() 方法。")
            return False
        return True

    def _read_coils(self, address, count=1):
        """读取线圈状态 (功能码 0x01)。"""
        if not self._check_connection():
            return None
        coils = self.modbus_client.read_coils(address, count)
        if coils is None:
            logger.info(f"读取线圈 (地址: {hex(address)}, 数量: {count}) 失败。")
        return coils

    def _write_single_coil(self, address, value):
        """写入单个线圈 (功能码 0x05)。"""
        if not self._check_connection():
            return False
        success = self.modbus_client.write_single_coil(address, value)
        if not success:
            logger.info(f"写入单个线圈 (地址: {hex(address)}, 值: {value}) 失败。")
        return success

    def _write_multiple_coils(self, address, values):
        """写入多个线圈 (功能码 0x0F)。"""
        if not self._check_connection():
            return False
        success = self.modbus_client.write_multiple_coils(address, values)
        if not success:
            logger.info(f"写入多个线圈 (地址: {hex(address)}, 值: {values}) 失败。")
        return success

    def _read_discrete_inputs(self, address, count=1):
        """读取离散输入状态 (功能码 0x02)。"""
        if not self._check_connection():
            return None
        inputs = self.modbus_client.read_discrete_inputs(address, count)
        if inputs is None:
            logger.info(f"读取离散输入 (地址: {hex(address)}, 数量: {count}) 失败。")
        return inputs

    def _read_input_registers(self, address, count=1):
        """读取输入寄存器 (功能码 0x04)。"""
        if not self._check_connection():
            return None
        registers = self.modbus_client.read_input_registers(address, count)
        if registers is None:
            logger.info(f"读取输入寄存器 (地址: {hex(address)}, 数量: {count}) 失败。")
        return registers

    def _read_holding_registers(self, address, count=1):
        """读取保持寄存器 (功能码 0x03)。"""
        if not self._check_connection():
            return None
        registers = self.modbus_client.read_holding_registers(address, count)
        if registers is None:
            logger.info(f"读取保持寄存器 (地址: {hex(address)}, 数量: {count}) 失败。")
        return registers

    def _write_single_holding_register(self, address, value):
        """写入单个保持寄存器 (功能码 0x06)。"""
        if not self._check_connection():
            return False
        success = self.modbus_client.write_single_register(address, value)
        if not success:
            logger.info(f"写入单个保持寄存器 (地址: {hex(address)}, 值: {value}) 失败。")
        return success

    def _write_multiple_holding_registers(self, address, values):
        """写入多个保持寄存器 (功能码 0x10)。"""
        if not self._check_connection():
            return False
        success = self.modbus_client.write_multiple_registers(address, values)
        if not success:
            logger.info(f"写入多个保持寄存器 (地址: {hex(address)}, 值: {values}) 失败。")
        return success

    # --- 输出控制 (通过线圈寄存器 0x0000H - 0x002FH) [cite: 218, 221] ---
    def set_output_state(self, channel, state):
        """
        设置单个输出通道的开关状态。

        Args:
            channel (int): 输出通道号 (1-48)。
            state (bool): True 为开启 (写1), False 为关闭 (写0)。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 1 <= channel <= 48:
            logger.info("错误: 通道号必须在 1 到 48 之间。")
            return False

        # 协议地址 = 0x0000H + (通道号 - 1) [cite: 221]
        address = self.COIL_OUTPUT_CONTROL_BASE + (channel - 1)
        return self._write_single_coil(address, state)

    def set_multiple_outputs_state(self, start_channel, states):
        """
        批量设置多个输出通道的开关状态。

        Args:
            start_channel (int): 起始输出通道号 (1-48)。
            states (list of bool): 包含 True/False 的列表，对应每个通道的开关状态。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 1 <= start_channel <= 48:
            logger.info("错误: 起始通道号必须在 1 到 48 之间。")
            return False
        if not all(isinstance(s, bool) for s in states):
            logger.info("错误: 状态列表必须只包含布尔值 (True/False)。")
            return False

        # 协议地址 = 0x0000H + (起始通道号 - 1) [cite: 221]
        address = self.COIL_OUTPUT_CONTROL_BASE + (start_channel - 1)
        return self._write_multiple_coils(address, states)

    def get_output_states(self, start_channel, count):
        """
        获取多个输出通道的开关状态。

        Args:
            start_channel (int): 起始输出通道号 (1-48)。
            count (int): 要读取的通道数量。
        Returns:
            list of bool or None: 布尔值列表表示通道状态，失败返回 None。
        """
        if not (1 <= start_channel <= 48 and 1 <= start_channel + count - 1 <= 48):
            logger.info("错误: 通道范围超出限制 (1-48)。")
            return None

        # 协议地址 = 0x0000H + (起始通道号 - 1) [cite: 221]
        address = self.COIL_OUTPUT_CONTROL_BASE + (start_channel - 1)
        return self._read_coils(address, count)

    # --- 输入状态读取 (通过离散输入状态寄存器 0x0000H - 0x002FH) [cite: 223, 225] ---
    def get_input_state(self, channel):
        """
        获取单个输入通道的触发状态。

        Args:
            channel (int): 输入通道号 (1-48)。
        Returns:
            bool or None: True 为已触发 (1), False 为未触发 (0)，失败返回 None。 [cite: 225]
        """
        if not 1 <= channel <= 48:
            logger.info("错误: 通道号必须在 1 到 48 之间。")
            return None

        # 协议地址 = 0x0000H + (通道号 - 1) [cite: 225]
        address = self.DISCRETE_INPUT_STATUS_BASE + (channel - 1)
        states = self._read_discrete_inputs(address, 1)
        return states[0] if states is not None else None

    def get_all_input_states(self, count=48):
        """
        获取所有或指定数量输入通道的触发状态。

        Args:
            count (int): 要读取的通道数量 (1-48)，默认为 48。
        Returns:
            list of bool or None: 布尔值列表表示通道状态，失败返回 None。
        """
        if not 1 <= count <= 48:
            logger.info("错误: 读取通道数量必须在 1 到 48 之间。")
            return None

        return self._read_discrete_inputs(self.DISCRETE_INPUT_STATUS_BASE, count)

    # --- 输入状态读取 (通过输入寄存器 0x0000H - 0x0034H) [cite: 239, 243, 244, 248] ---
    def get_input_status_by_register(self, channel):
        """
        通过输入寄存器获取单个输入通道的触发状态。

        Args:
            channel (int): 输入通道号 (1-48)。
        Returns:
            bool or None: True 为已触发 (1), False 为未触发 (0)，失败返回 None。 [cite: 243]
        """
        if not 1 <= channel <= 48:
            logger.info("错误: 通道号必须在 1 到 48 之间。")
            return None

        # 协议地址 = 0x0000H + (通道号 - 1) [cite: 243]
        address = self.INPUT_REGISTER_STATUS_BASE + (channel - 1)
        registers = self._read_input_registers(address, 1)
        return (registers[0] == 1) if registers is not None else None

    def get_input_status_bit_packed(self):
        """
        获取按位表示的通道1~48输入口状态。

        Returns:
            dict or None: 包含 'ch1_16', 'ch17_32', 'ch33_48' 键的字典，
                          每个键对应一个表示通道状态的整数 (0:未触发, 1:已触发)。
                          失败返回 None。
        """
        # 读取 0x0032H 到 0x0034H 这3个寄存器
        registers = self._read_input_registers(self.INPUT_REGISTER_STATUS_CH1_16_BIT, 3)
        if registers and len(registers) == 3:
            return {
                'ch1_16': registers[0],   # 最低位表示通道1输入口状态，最高位表示通道16 [cite: 243]
                'ch17_32': registers[1],  # 最低位表示通道17输入口状态，最高位表示通道32 [cite: 244]
                'ch33_48': registers[2]   # 最低位表示通道33输入口状态，最高位表示通道48 [cite: 248]
            }
        return None

    # --- 模块参数和高级输出控制 (通过保持寄存器) [cite: 250, 251, 252, 253] ---
    def set_communication_detection_time(self, seconds):
        """
        设置通讯检测时间。模块在通讯断开 N*0.1 秒后关闭所有输出。

        Args:
            seconds (float): 检测时间 (秒)。0 为不检测。
                             指令中的 N = seconds * 10。 (N*0.1 单位:S)
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if seconds < 0:
            logger.info("错误: 检测时间不能为负。")
            return False

        # N = seconds / 0.1 = seconds * 10
        value = int(seconds * 10)
        return self._write_single_holding_register(self.HOLDING_REGISTER_COMM_DETECT_TIME, value)

    def get_communication_detection_time(self):
        """
        获取通讯检测时间设置。

        Returns:
            float or None: 检测时间 (秒)，0 为不检测，失败返回 None。
        """
        registers = self._read_holding_registers(self.HOLDING_REGISTER_COMM_DETECT_TIME, 1)
        if registers is not None and len(registers) > 0:
            return registers[0] * 0.1 # N*0.1 单位:S
        return None

    def set_active_upload_control(self, mode_or_interval=0):
        """
        设置输入口状态主动上传控制。

        Args:
            mode_or_interval (int):
                0: 不主动上传 (出厂默认)。
                1: 任一输入口状态发生变化时主动上传。
                >1: 主动上传间隔时间 (N-1)*0.01 秒。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not isinstance(mode_or_interval, int) or mode_or_interval < 0:
            logger.info("错误: 上传控制模式或间隔必须是非负整数。")
            return False
        return self._write_single_holding_register(self.HOLDING_REGISTER_ACTIVE_UPLOAD_CONTROL, mode_or_interval)

    def get_active_upload_control(self):
        """
        获取输入口状态主动上传控制设置。

        Returns:
            int or None: 设置值 (0:不上传, 1:变化上传, >1:间隔值N)，失败返回 None。
        """
        registers = self._read_holding_registers(self.HOLDING_REGISTER_ACTIVE_UPLOAD_CONTROL, 1)
        return registers[0] if registers is not None and len(registers) > 0 else None

    def set_rs485_address(self, address):
        """
        设置 RS485 总线地址/站号 (1-255)。
        注: 此参数掉电保存，修改后重新上电即可生效。

        Args:
            address (int): 新的站号 (1-255)。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 1 <= address <= 255:
            logger.info("错误: RS485 地址必须在 1 到 255 之间。")
            return False
        # 注意: 成功写入后，下次通信需要使用新的地址。
        success = self._write_single_holding_register(self.HOLDING_REGISTER_RS485_ADDRESS, address)
        if success:
            # 成功设置后，更新ModbusClient的unit_id
            self.modbus_client.unit_id = address
            self.slave_id = address
            logger.info(f"RS485 地址已更新为: {address}。请注意，新地址将在模块重新上电后生效。")
        return success

    def get_rs485_address(self):
        """
        获取当前的 RS485 总线地址/站号。

        Returns:
            int or None: 当前站号，失败返回 None。
        """
        registers = self._read_holding_registers(self.HOLDING_REGISTER_RS485_ADDRESS, 1)
        return registers[0] if registers is not None and len(registers) > 0 else None

    def set_baudrate(self, baudrate_code):
        """
        设置波特率。
        注: 此参数掉电保存，修改后重新上电即可生效。

        Args:
            baudrate_code (int): 波特率代码 (0-7)。
                0: 4800, 1: 9600, 2: 14400, 3: 19200, 4: 38400 (默认),
                5: 56000, 6: 57600, 7: 115200
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 0 <= baudrate_code <= 7:
            logger.info("错误: 波特率代码必须在 0 到 7 之间。")
            return False

        success = self._write_single_holding_register(self.HOLDING_REGISTER_BAUDRATE_SETTING, baudrate_code)
        if success:
            # 理论上应该根据代码更新 self.modbus_client 的 baudrate，但通常需要重启模块才能生效
            baudrate_map = {
                0: 4800, 1: 9600, 2: 14400, 3: 19200, 4: 38400,
                5: 56000, 6: 57600, 7: 115200
            }
            new_baudrate = baudrate_map.get(baudrate_code, self.DEFAULT_BAUDRATE)
            logger.info(f"波特率已设置为代码 {baudrate_code} ({new_baudrate}bps)。请注意，新波特率将在模块重新上电后生效。")
        return success

    def get_baudrate_setting(self):
        """
        获取当前的波特率设置代码。

        Returns:
            int or None: 波特率代码 (0-7)，失败返回 None。
        """
        registers = self._read_holding_registers(self.HOLDING_REGISTER_BAUDRATE_SETTING, 1)
        return registers[0] if registers is not None and len(registers) > 0 else None

    def set_batch_control_all_outputs(self, turn_on_all):
        """
        批量控制所有输出。

        Args:
            turn_on_all (bool): True 为全开 (1), False 为全关 (0)。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        value = 1 if turn_on_all else 0
        return self._write_single_holding_register(self.HOLDING_REGISTER_BATCH_CONTROL, value)

    def set_outputs_bit_by_batch(self, start_channel, states_int):
        """
        按位批量控制通道 1~16, 17~32, 或 33~48 的输出。

        Args:
            start_channel (int): 起始通道号 (1, 17, 33)。
            states_int (int): 一个 16 位整数，每一位代表一个通道的状态 (0:关闭, 1:开启)。
                              最低位对应起始通道，最高位对应起始通道 + 15。
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        address = None
        if start_channel == 1:
            address = self.HOLDING_REGISTER_BIT_CONTROL_CH1_16
        elif start_channel == 17:
            address = self.HOLDING_REGISTER_BIT_CONTROL_CH17_32
        elif start_channel == 33:
            address = self.HOLDING_REGISTER_BIT_CONTROL_CH33_48
        else:
            logger.info("错误: start_channel 必须是 1, 17 或 33。")
            return False

        if not 0 <= states_int <= 0xFFFF: # 16位无符号整数
            logger.info("错误: states_int 必须是 0 到 65535 之间的整数。")
            return False

        return self._write_single_holding_register(address, states_int)

    def set_parity(self, parity_code):
        """
        设置奇偶校验。
        注: 此参数掉电保存，修改后重新上电即可生效。

        Args:
            parity_code (int): 校验代码。
                0: 无校验 (默认)
                1: 奇校验
                2: 偶校验
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 0 <= parity_code <= 2:
            logger.info("错误: 奇偶校验代码必须在 0 到 2 之间。")
            return False

        success = self._write_single_holding_register(self.HOLDING_REGISTER_PARITY_SETTING, parity_code)
        if success:
            parity_map = {0: 'N', 1: 'O', 2: 'E'}
            new_parity_char = parity_map.get(parity_code, self.DEFAULT_PARITY)
            # self.modbus_client.serial_settings(parity=new_parity_char) # 通常也需要重启模块
            logger.info(f"奇偶校验已设置为代码 {parity_code} ({new_parity_char})。请注意，新设置将在模块重新上电后生效。")
        return success

    def get_parity_setting(self):
        """
        获取当前的奇偶校验设置代码。

        Returns:
            int or None: 奇偶校验代码 (0-2)，失败返回 None。
        """
        registers = self._read_holding_registers(self.HOLDING_REGISTER_PARITY_SETTING, 1)
        return registers[0] if registers is not None and len(registers) > 0 else None

    def set_channel_control_mode(self, channel, mode_code):
        """
        设置单个通道的工作模式。
        注: 此参数掉电保存，修改后重新上电即可生效。 [cite: 268]

        Args:
            channel (int): 通道号 (1-48)。
            mode_code (int): 模式代码。
                0: 普通模式 (0:关闭, 1:开启, >1:延时开关)
                1: 联动模式
                2: 点动模式
                3: 开关循环模式
                4: 开固定时长模式
        Returns:
            bool: True 表示成功，False 表示失败。
        """
        if not 1 <= channel <= 48:
            logger.info("错误: 通道号必须在 1 到 48 之间。")
            return False
        if not 0 <= mode_code <= 4: # 根据文档，目前定义了0-4模式
            logger.info("错误: 模式代码必须在 0 到 4 之间。")
            return False

        # 协议地址 = 0x0096H + (通道号 - 1) [cite: 268]
        address = self.HOLDING_REGISTER_CHANNEL_MODE_BASE + (channel - 1)
        return self._write_single_holding_register(address, mode_code)

    def get_channel_control_mode(self, channel):
        """
        获取单个通道的工作模式设置。

        Args:
            channel (int): 通道号 (1-48)。
        Returns:
            int or None: 模式代码，失败返回 None。
        """
        if not 1 <= channel <= 48:
            logger.info("错误: 通道号必须在 1 到 48 之间。")
            return None

        address = self.HOLDING_REGISTER_CHANNEL_MODE_BASE + (channel - 1)
        registers = self._read_holding_registers(address, 1)
        return registers[0] if registers is not None and len(registers) > 0 else None

# --- 使用示例 ---
if __name__ == "__main__":
    # 根据你的操作系统和模块连接的实际串口号进行修改
    # Windows: 'COMx' 例如 'COM3'
    # Linux/macOS: '/dev/ttyUSBx' 或 '/dev/ttyACM0'
    SERIAL_PORT = '/dev/ttyUSB0'
    MODULE_ID = 1 # 模块的 Modbus 从站地址，默认是 1

    # 初始化模块控制器
    module = ZSDigitalIOModule(SERIAL_PORT, slave_id=MODULE_ID)

    if module.connect():
        logger.info("\n--- 读取输入状态 ---")
        # 读取通道1的离散输入状态
        input1_state = module.get_input_state(1)
        if input1_state is not None:
            logger.info(f"通道1输入状态 (离散输入): {'已触发' if input1_state else '未触发'}")

        # 读取所有离散输入状态
        all_inputs = module.get_all_input_states()
        if all_inputs is not None:
            logger.info(f"所有离散输入状态: {all_inputs}")

        # 通过输入寄存器读取通道2状态
        input2_reg_state = module.get_input_status_by_register(2)
        if input2_reg_state is not None:
            logger.info(f"通道2输入状态 (输入寄存器): {'已触发' if input2_reg_state else '未触发'}")

        # 获取按位表示的输入状态
        bit_packed_status = module.get_input_status_bit_packed()
        if bit_packed_status:
            logger.info(f"按位表示的输入状态 (Ch1-16): {bin(bit_packed_status['ch1_16'])}")
            logger.info(f"按位表示的输入状态 (Ch17-32): {bin(bit_packed_status['ch17_32'])}")
            logger.info(f"按位表示的输入状态 (Ch33-48): {bin(bit_packed_status['ch33_48'])}")


        logger.info("\n--- 控制输出 ---")
        # 设置通道1输出为开启
        logger.info("设置通道1输出为开启...")
        if module.set_output_state(1, True):
            logger.info("通道1输出开启成功。")
        else:
            logger.info("通道1输出开启失败。")
        time.sleep(1) # 等待1秒

        # 设置通道1输出为关闭
        logger.info("设置通道1输出为关闭...")
        if module.set_output_state(1, False):
            logger.info("通道1输出关闭成功。")
        else:
            logger.info("通道1输出关闭失败。")
        time.sleep(1)

        # 批量设置通道2和通道3输出为开启
        logger.info("批量设置通道2和3输出为开启...")
        if module.set_multiple_outputs_state(2, [True, True]):
            logger.info("通道2和3批量开启成功。")
        else:
            logger.info("通道2和3批量开启失败。")
        time.sleep(1)

        # 获取输出状态
        output_states = module.get_output_states(1, 3) # 获取通道1到3的状态
        if output_states is not None:
            logger.info(f"通道1-3输出状态: {output_states}")


        logger.info("\n--- 模块参数设置和查询 ---")
        # 查询当前波特率设置
        current_baud_code = module.get_baudrate_setting()
        if current_baud_code is not None:
            baudrate_map_rev = {0: 4800, 1: 9600, 2: 14400, 3: 19200, 4: 38400, 5: 56000, 6: 57600, 7: 115200}
            logger.info(f"当前波特率设置代码: {current_baud_code} ({baudrate_map_rev.get(current_baud_code, '未知')})")

        # 尝试设置 RS485 地址为 2 (注意：此操作需谨慎，因为设置后下次通信要用新地址)
        # logger.info("\n尝试设置 RS485 地址为 2 (此操作将改变模块地址，谨慎操作！)...")
        # if module.set_rs485_address(2):
        #     logger.info("RS485 地址设置成功。")
        #     # 如果成功设置并生效，你需要更新 module 对象的 slave_id 或重新创建对象
        #     # module.slave_id = 2 # 如果设置立即生效，则需要更新
        #     # 或者 for next test: module = ZSDigitalIOModule(SERIAL_PORT, slave_id=2)
        # else:
        #     logger.info("RS485 地址设置失败。")
        # time.sleep(1)

        # 设置通讯检测时间为 5 秒 (即 50 * 0.1 = 5秒)
        logger.info("设置通讯检测时间为 5 秒...")
        if module.set_communication_detection_time(5.0):
            logger.info("通讯检测时间设置成功。")
        else:
            logger.info("通讯检测时间设置失败。")
        time.sleep(1)
        detected_time = module.get_communication_detection_time()
        if detected_time is not None:
            logger.info(f"当前通讯检测时间设置: {detected_time} 秒")

        # 设置通道1为点动模式 (模式代码 2)
        logger.info("设置通道1为点动模式...")
        if module.set_channel_control_mode(1, 2):
            logger.info("通道1模式设置成功。")
        else:
            logger.info("通道1模式设置失败。")
        time.sleep(1)

        mode = module.get_channel_control_mode(1)
        if mode is not None:
            logger.info(f"通道1当前工作模式代码: {mode}")

    else:
        logger.info("无法连接到中盛科技数字量输入输出模块。请检查串口配置、模块连接和电源。")

    module.disconnect()
