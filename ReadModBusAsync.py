import asyncio

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer, 
    ModbusException,
    # pymodbus_apply_logging_config,
)

import sys

import struct

################# End of Imports and Start of Functions #####################

async def run_async_simple_client(comm, host, port, framer=Framer.SOCKET):
    client = ModbusClient.AsyncModbusTcpClient(
        host,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # retry_on_empty=False,
        # source_address=("localhost", 0),
    )

    try:
        await client.connect()
        # test client is connected
        assert client.connected
    except ConnectionRefusedError:
        print("Error: Connection refused. Check if the Modbus server is running.")
    except TimeoutError:
        print("Error: Connection timed out. Check the timeout setting.")
    except OSError as e:
        print(f"I/O Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    try:
        # See all calls in client_calls.py
        rr = await client.read_coils(Coil, 1, slave=1)
        print(rr.bits[0])
        result = await client.read_holding_registers(HR,2,1)
        print(result.registers[0])
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()

    # print("close connection")
    client.close()

async def async_aplication_multi(host, port, readCoil, readHR, framer=Framer.SOCKET):
    client = ModbusClient.AsyncModbusTcpClient(
        host,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # retry_on_empty=False,
        # source_address=("localhost", 0),
    )

    try:
        await client.connect()
        # test client is connected
        assert client.connected
    except ConnectionRefusedError:
        print("Error: Connection refused. Check if the Modbus server is running.")
    except TimeoutError:
        print("Error: Connection timed out. Check the timeout setting.")
    except OSError as e:
        print(f"I/O Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    try:
        for Coil in readCoil:
            Coil_number = int(Coil["number"])
            Coil_name = Coil["name"]
            rr = await client.read_coils(Coil_number, 1, slave=1)
            print(Coil_name,":", str(rr.bits[0]))
        for HR in readHR:
            HR_number = int(HR["number"])
            HR_name = HR["name"]
            HR_type = int(HR["type"])
            result = await client.read_holding_registers(HR_number, HR_type, 1)
            if HR_type == 2:
                bytes_lista = struct.pack('!HH',*result.registers)
                print(HR_name,":", struct.unpack('!f', bytes_lista)[0])
            else:
                print(HR_name,":", result.registers[0])
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    except Exception as e:
        print(f"Erro inesperado: {e}")
    if rr.isError() or result.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
    if isinstance(result, ExceptionResponse):
        print(f"Received Modbus library exception ({result})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
    

    # print("close connection")
    client.close()

####################### Application being called #########################

if __name__ != "__main__":
    Coil = 1
    HR = 1

####################### Stand-alone aplication #########################

if __name__ == "__main__":
    
    IP = input("Enter the device IP: ")
    Coil = int(input("Enter the COIL register to be read: "))
    HR = int(input("Enter the holding register to be read: "))

    while True:
        asyncio.run(
        run_async_simple_client("tcp", IP, 502)
        )
        resposta = input("Do you want to close the terminal? (Y/N): ").strip().lower()
        if resposta == 'y':
            print("Closing the terminal...")
            sys.exit()  # Close the terminal
        elif resposta == 'n':
            print("Continuing program execution...")
        else:
            print("Invalid option! Please enter 'Y' for yes or 'N' for no.")