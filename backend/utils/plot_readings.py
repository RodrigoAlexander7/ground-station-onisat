import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

def main():
    # Define file paths
    # Assuming script is run from project root or utils/ directory, handle both if possible or just stick to relative from utils/
    # Best practice: use absolute path based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '../data/readings.json')
    
    print(f"Loading data from {data_path}...")
    
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {data_path}")
        return

    if not data:
        print("No data found in JSON.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Convert timestamp to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Ensure numeric columns are floats
    numeric_cols = ['wind_speed', 'rpm', 'lift_force']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    print("Data loaded successfully. Generating plot...")
    
    # Define plots to generate
    # Tuples of (x_col, y_col, filename, title, x_label, y_label)
    plots = [
        ('timestamp', 'lift_force', 'lift_force_vs_time.png', 'Lift Force vs Time', 'Time', 'Lift Force'),
    ]

    for x_col, y_col, filename, title, x_label, y_label in plots:
        if x_col not in df.columns or y_col not in df.columns:
            print(f"Skipping {filename}: Missing columns {x_col} or {y_col}")
            continue
            
        plt.figure(figsize=(16, 10))
        plt.plot(df[x_col], df[y_col], marker='o', linestyle='-')
        
        plt.title(title, fontsize=16)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        
        # Configurar la grid (rejilla)
        plt.minorticks_on() # Activar ticks menores
        plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.8) # Grid principal
        plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5) # Grid secundaria (mas pequeña)

        # Configurar el formato de los decimales en los ejes
        # Por ejemplo, 2 decimales para el eje Y
        ax = plt.gca() # Obtener el eje actual
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f')) 
        # Si quisieras formatear el eje X tambien (si no es fecha):
        # ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

        plt.tight_layout()
        
        # Save to the same directory as the script
        output_path = os.path.join(script_dir, filename)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved {filename}")

if __name__ == "__main__":
    main()
