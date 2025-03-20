# examples/basic_usage.py
from src.easys7comm import PLC, DataType

def main():
    try:
        plc = PLC("10.254.176.81")
        plc.write("DB20.DBX12.0", "Allan", DataType.STRING)
        print(plc.read("DB20.DBX12.0", DataType.STRING))
        print(plc.get_connected())
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        plc.close()
    
if __name__ == "__main__":
    main()
