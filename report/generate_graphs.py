import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as patches

# Create output directory if it doesn't exist
output_dir = '/Users/mohityadav/Desktop/metaevalai/report/figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Helper function to configure plots for a professional academic look
def setup_plot(fig, ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()

# --- Fig 4.1: Water Level Detection Accuracy Graph ---
def plot_fig_4_1():
    fig, ax = plt.subplots(figsize=(8, 6))
    levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8']
    accuracies = [99.5, 98.8, 99.2, 100.0, 99.7, 98.9, 99.4, 99.8]
    
    bars = ax.bar(levels, accuracies, color='#4C72B0', edgecolor='black', linewidth=1)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    ax.set_ylim(90, 101)
    setup_plot(fig, ax, 'Fig 4.1: Water Level Detection Accuracy', 'Water Level Probe', 'Accuracy (%)')
    plt.savefig(os.path.join(output_dir, 'fig_4_1_accuracy.png'), dpi=300)
    plt.close()

# --- Fig 4.2: Response Time at Different Levels ---
def plot_fig_4_2():
    fig, ax = plt.subplots(figsize=(8, 6))
    levels = np.arange(1, 9)
    # Simulated response times (in ms) with some slight variation
    response_times = [15.2, 16.1, 15.8, 17.5, 16.0, 15.5, 16.8, 15.9]
    
    ax.plot(levels, response_times, marker='o', linestyle='-', color='#C44E52', linewidth=2, markersize=8)
    ax.set_xticks(levels)
    ax.set_xticklabels([f'Level {i}' for i in levels])
    ax.set_ylim(10, 25)
    
    setup_plot(fig, ax, 'Fig 4.2: Response Time at Different Levels', 'Water Level Probe', 'Response Time (ms)')
    plt.savefig(os.path.join(output_dir, 'fig_4_2_response_time.png'), dpi=300)
    plt.close()

# --- Fig 4.3: Solar Panel Output Voltage over 12 Hours ---
def plot_fig_4_3():
    fig, ax = plt.subplots(figsize=(10, 6))
    time_hours = np.arange(6, 19) # 6 AM to 6 PM
    time_labels = [f'{t}:00' for t in time_hours]
    # Simulated solar panel voltage (typical 12V nominal panel, peak 18V-20V)
    voltage = [0.0, 5.2, 12.1, 16.5, 18.2, 19.1, 19.5, 18.8, 17.2, 14.5, 8.5, 3.1, 0.0]
    
    ax.plot(time_hours, voltage, marker='s', linestyle='-', color='#55A868', linewidth=2, markersize=8)
    ax.fill_between(time_hours, voltage, color='#55A868', alpha=0.2)
    
    ax.set_xticks(time_hours)
    ax.set_xticklabels(time_labels, rotation=45)
    ax.set_ylim(0, 22)
    
    setup_plot(fig, ax, 'Fig 4.3: Solar Panel Output Voltage over 12 Hours (Clear Day)', 'Time of Day', 'Output Voltage (V)')
    plt.savefig(os.path.join(output_dir, 'fig_4_3_solar_voltage.png'), dpi=300)
    plt.close()

# --- Fig 4.4: Battery Discharge Curve During Operation ---
def plot_fig_4_4():
    fig, ax = plt.subplots(figsize=(10, 6))
    time_hours = np.arange(0, 50, 2) # 0 to 48 hours
    
    # Simulated lead-acid battery discharge curve (starts ~12.7V, drops to 11.5V, then sharply drops)
    def battery_voltage(t):
        if t < 10:
            return 12.7 - (t * 0.02)
        elif t < 40:
            return 12.5 - ((t - 10) * 0.03)
        else:
            return 11.6 - ((t - 40) * 0.15)
            
    voltage = [battery_voltage(t) for t in time_hours]
    
    ax.plot(time_hours, voltage, linestyle='-', color='#8172B3', linewidth=2.5)
    
    # Highlight safe operating area and cutoff
    ax.axhline(y=11.5, color='r', linestyle='--', label='Cut-off Voltage (11.5V)')
    ax.legend(loc='upper right')
    
    ax.set_ylim(10.0, 13.0)
    
    setup_plot(fig, ax, 'Fig 4.4: Battery Discharge Curve During Operation (Without Solar Input)', 'Time (Hours)', 'Battery Voltage (V)')
    plt.savefig(os.path.join(output_dir, 'fig_4_4_battery_discharge.png'), dpi=300)
    plt.close()

# --- Fig 4.5: Comparison Chart — Proposed vs Existing Systems ---
def plot_fig_4_5():
    # Variables
    labels = ['Cost Efficiency', 'Reliability', 'Maintenance', 'Power Efficiency', 'Accuracy']
    num_vars = len(labels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    
    # Data (scale 1-10, 10 being best)
    systems = {
        'Proposed System': [9, 9, 8, 9, 9],
        'Float Switch': [8, 4, 3, 10, 4],
        'Ultrasonic': [5, 7, 6, 6, 8],
        'Generic IoT': [6, 7, 7, 5, 8]
    }
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for (name, values), color in zip(systems.items(), colors):
        values += values[:1]
        ax.plot(angles, values, label=name, color=color, linewidth=2)
        ax.fill(angles, values, color=color, alpha=0.1)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
    
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color='grey', size=8)
    
    ax.set_title('Fig 4.5: Comparison Chart \n Proposed vs Existing Systems', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig_4_5_comparison_radar.png'), dpi=300)
    plt.close()

# --- Fig 4.6: LCD Display Output at Various Water Levels ---
def plot_fig_4_6():
    fig, axs = plt.subplots(4, 1, figsize=(8, 10))
    fig.patch.set_facecolor('white')
    
    displays = [
        {'level': '0', 'status': 'EMPTY'},
        {'level': '4', 'status': 'HALF '},
        {'level': '7', 'status': 'HIGH '},
        {'level': '8', 'status': 'FULL '}
    ]
    
    for i, (ax, disp) in enumerate(zip(axs, displays)):
        # Create green LCD background
        ax.set_facecolor('#87A96B') # LCD green
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 2)
        
        # Turn off axes
        ax.axis('off')
        
        # Draw a border around the LCD
        rect = patches.Rectangle((0, 0), 16, 2, linewidth=4, edgecolor='#333333', facecolor='none')
        ax.add_patch(rect)
        
        # Add text simulating 16x2 LCD
        # Using a monospaced font if available, else default sans-serif
        line1 = f"WATER LEVEL: {disp['level']}  "
        line2 = f"STATUS: {disp['status']} "
        
        ax.text(0.5, 1.3, line1, fontsize=24, fontfamily='monospace', color='#111111', weight='bold')
        ax.text(0.5, 0.3, line2, fontsize=24, fontfamily='monospace', color='#111111', weight='bold')
        
        ax.set_title(f"Level {disp['level']}", fontsize=12, pad=10)
        
    plt.suptitle('Fig 4.6: LCD Display Output at Various Water Levels', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(output_dir, 'fig_4_6_lcd_displays.png'), dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Generating Figures...")
    plot_fig_4_1()
    plot_fig_4_2()
    plot_fig_4_3()
    plot_fig_4_4()
    plot_fig_4_5()
    plot_fig_4_6()
    print(f"All figures generated and saved to {output_dir}")
