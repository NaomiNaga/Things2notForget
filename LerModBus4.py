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

def fechar_terminal():
    resposta = input("Deseja fechar o terminal? (Y/N): ").strip().lower()
    if resposta == 'y':
        return True
    elif resposta == 'n':
        return False
    else:
        print("Opção inválida! Por favor, insira 'Y' para sim ou 'N' para não.")
        return fechar_terminal()
    

if __name__ == "__main__":
    
    IP = input("Digite o IP do dispositivo: ")
    Coil = int(input("Digite o registrador COIL a ser lido: "))
    HR = int(input("Digite o holding register a ser lido: "))

    while True:
        asyncio.run(
        run_async_simple_client("tcp", IP, 502)
        )
        resposta = input("Deseja fechar o terminal? (Y/N): ").strip().lower()
        if resposta == 'y':
            print("Fechando o terminal...")
            # Coloque aqui qualquer código que você deseja executar antes de fechar o terminal
            sys.exit()  # Fecha o terminal
        elif resposta == 'n':
            print("Continuando a execução do programa...")
            # Coloque aqui qualquer código que você deseja executar se o terminal não for fechado
        else:
            print("Opção inválida! Por favor, insira 'Y' para sim ou 'N' para não.")

    fechar_terminal()








