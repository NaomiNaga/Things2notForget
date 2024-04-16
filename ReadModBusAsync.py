import asyncio

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer, 
    ModbusException,
    # pymodbus_apply_logging_config,
)

import sys

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

    await client.connect()
    # test client is connected
    assert client.connected

    try:
        # See all calls in client_calls.py
        rr = await client.read_coils(Coil, 1, slave=1)
        print(rr.bits[0])
        result = await client.read_holding_registers(HR,1,1)
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

