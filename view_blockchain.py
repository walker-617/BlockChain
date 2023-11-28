from rich.console import Console
from rich.table import Table
import sys
from firebase import get_data

blocks=get_data()
console = Console()

for block_num,block in blocks.items():
    console.print(block_num.upper(),style="bold blue")
    console.print("Previous hash:",style="bold")
    console.print("  "+block["prev_hash"])
    console.print("Current hash:",style="bold")
    console.print("  "+block["current_hash"])
    ip_columns=['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Headache','Fatigue ', 'Gastrointestinal ', 'Abroad travel','Contact with COVID Patient', 'Attended Large Gathering','Visited Public Exposed Places',"timestamp","has Covid"]
    table = Table(show_header=True, header_style="bold magenta")
    for col in ip_columns:
        table.add_column(col)
    
    if block_num!="Block-0":
        for data in block["data"]:
            row=[]
            for col in ip_columns:
                row.append(data[col])
            table.add_row(*row)
        console.print(table)
    else:
        console.print("Genisis block",style="bold green")
    print()

original_stdout = sys.stdout
with open('blockchain.txt', 'w') as file:
    sys.stdout = file

    for block_num,block in blocks.items():
        print(block_num.upper())
        print("Previous hash:")
        print("  "+block["prev_hash"])
        print("Current hash:")
        print("  "+block["current_hash"])
        ip_columns=['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Headache','Fatigue ', 'Gastrointestinal ', 'Abroad travel','Contact with COVID Patient', 'Attended Large Gathering','Visited Public Exposed Places',"timestamp","has Covid"]
        table = Table(show_header=False)
        # for col in ip_columns:
        #     table.add_column(col)
        table.add_row(*ip_columns)
        if block_num!="Block-0":
            for data in block["data"]:
                row=[]
                for col in ip_columns:
                    row.append(data[col])
                table.add_row(*row)
            console.print(table)
        else:
            print("Genisis block")
        print()
    sys.stdout = original_stdout
