import matplotlib.pyplot as plt

def plot_solution(data, x):
    # Collect item assignments and bin values
    bin_contents = {}
    bin_values = {}
    bin_weights = {}
    for j in data['bins']:
        items_in_bin = []
        total_value = 0
        total_weight = 0
        for i in data['items']:
            if x[i, j].solution_value() > 0:
                w, v = data['weights'][i], data['values'][i]
                items_in_bin.append((i, w, v))
                total_value += v
                total_weight += w
        bin_contents[j] = items_in_bin
        bin_values[j] = total_value
        bin_weights[j] = total_weight

    # Sort bins by total packed value (ascending)
    sorted_bins = sorted(data['bins'], key=lambda j: bin_values[j])

    fig, ax = plt.subplots(figsize=(10, 6))

    # Define a colormap excluding gray (manually choose colors)
    base_colors = plt.cm.get_cmap('tab20', len(data['items']) + 1)
    colors = [base_colors(i) for i in range(len(data['items']))]  # skip gray tone
    gray_color = '#d3d3d3'  # light gray for unused capacity

    for idx, j in enumerate(sorted_bins):
        items = bin_contents[j]
        y = [idx] * len(items)
        widths = [w for _, w, _ in items]
        lefts = [sum(widths[:k]) for k in range(len(widths))]
        item_labels = [f"Item {i}\nW:{w} V:{v}" for i, w, v in items]

        # Plot used capacity segments
        for k, (i, w, v) in enumerate(items):
            ax.barh(y[k], widths[k], left=lefts[k], height=0.8,
                    color=colors[i], edgecolor='black')
            ax.text(lefts[k] + widths[k]/2, y[k], item_labels[k],
                    ha='center', va='center', fontsize=8)

        # Plot unused capacity in gray
        used_weight = bin_weights[j]
        total_capacity = data['bin_capacities'][j]
        if used_weight < total_capacity:
            ax.barh(idx, total_capacity - used_weight, left=used_weight, height=0.8,
                    color=gray_color, edgecolor='black', hatch='//', alpha=0.5)

    ax.set_yticks(range(len(sorted_bins)))
    ax.set_yticklabels([f'Bin {j} (Value={bin_values[j]})' for j in sorted_bins])
    ax.set_xlabel('Weight')
    ax.set_title('Bins Sorted by Total Packed Value (Gray = Unused Capacity)')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
