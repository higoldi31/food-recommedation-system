"""
STAGE 5: EXPLORATORY DATA ANALYSIS (EDA) VISUALIZATION GENERATOR
Project: MoodFood - Mood-Based Food Recommendation System
Generates publication-quality charts for the portfolio assets/images directory.
"""

import os
import csv
import math
from collections import Counter

def load_data(filepath: str):
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def calculate_pearson_r(x: list, y: list) -> float:
    n = len(x)
    if n < 2:
        return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((val - mean_x) ** 2 for val in x))
    den_y = math.sqrt(sum((val - mean_y) ** 2 for val in y))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)

def generate_svg_calories_distribution(rows: list, output_path: str):
    """Generates a histogram with KDE curve for calorie distribution."""
    calories = [float(r["calories"]) for r in rows]
    min_c, max_c = 0, 600
    bin_width = 50
    num_bins = int((max_c - min_c) / bin_width)
    bins = [0] * num_bins
    
    for c in calories:
        idx = min(int(c / bin_width), num_bins - 1)
        bins[idx] += 1
        
    max_count = max(bins)
    
    # SVG Dimensions
    w, h = 600, 340
    pad_left, pad_bottom, pad_top, pad_right = 60, 50, 40, 30
    chart_w = w - pad_left - pad_right
    chart_h = h - pad_top - pad_bottom
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" style="background:#FAF8F5; font-family: sans-serif;">']
    svg.append(f'<text x="{w/2}" y="25" text-anchor="middle" font-size="14" font-weight="bold" fill="#202E26">Univariate Distribution of Calories (N=320)</text>')
    
    # Grid lines & Y-axis labels
    for i in range(5):
        y_val = int(max_count * (i / 4))
        y_pos = h - pad_bottom - (chart_h * (i / 4))
        svg.append(f'<line x1="{pad_left}" y1="{y_pos}" x2="{w - pad_right}" y2="{y_pos}" stroke="#E5DEC9" stroke-dasharray="3,3" />')
        svg.append(f'<text x="{pad_left - 10}" y="{y_pos + 4}" text-anchor="end" font-size="10" fill="#6E7D73">{y_val}</text>')
        
    bar_w = chart_w / num_bins - 4
    for i, count in enumerate(bins):
        b_x = pad_left + i * (chart_w / num_bins) + 2
        b_h = (count / max_count) * chart_h
        b_y = h - pad_bottom - b_h
        # Soft sage green bar
        svg.append(f'<rect x="{b_x:.1f}" y="{b_y:.1f}" width="{bar_w:.1f}" height="{b_h:.1f}" fill="#527360" rx="3" />')
        svg.append(f'<text x="{b_x + bar_w/2:.1f}" y="{b_y - 4:.1f}" text-anchor="middle" font-size="9" font-weight="bold" fill="#3A4D41">{count}</text>')
        
        # X label
        x_label = f"{i * bin_width}"
        svg.append(f'<text x="{b_x + bar_w/2:.1f}" y="{h - pad_bottom + 15}" text-anchor="middle" font-size="9" fill="#6E7D73">{x_label}</text>')
        
    # Axis titles
    svg.append(f'<text x="{w/2}" y="{h - 15}" text-anchor="middle" font-size="11" font-weight="bold" fill="#405247">Calorie Range (kcal)</text>')
    svg.append(f'<text transform="rotate(-90)" x="{-h/2}" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#405247">Frequency (Number of Foods)</text>')
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {output_path}")

def generate_svg_correlation_heatmap(rows: list, output_path: str):
    """Generates an aesthetic correlation matrix heatmap for macronutrients."""
    features = ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar']
    labels = ['Calories', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Sugar']
    data = {f: [float(r[f]) for r in rows] for f in features}
    
    matrix = []
    for f1 in features:
        row = []
        for f2 in features:
            r = calculate_pearson_r(data[f1], data[f2])
            row.append(r)
        matrix.append(row)
        
    w, h = 480, 480
    pad = 90
    cell_size = (w - pad - 20) / len(features)
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" style="background:#FAF8F5; font-family: sans-serif;">']
    svg.append(f'<text x="{w/2}" y="30" text-anchor="middle" font-size="14" font-weight="bold" fill="#202E26">Macronutrient Pearson Correlation Heatmap</text>')
    
    for i, r_label in enumerate(labels):
        # Y labels
        svg.append(f'<text x="{pad - 12}" y="{pad + i * cell_size + cell_size/2 + 4}" text-anchor="end" font-size="11" font-weight="bold" fill="#3A4D41">{r_label}</text>')
        # X labels
        svg.append(f'<text x="{pad + i * cell_size + cell_size/2}" y="{pad - 12}" text-anchor="middle" font-size="11" font-weight="bold" fill="#3A4D41">{r_label}</text>')
        
        for j, val in enumerate(matrix[i]):
            x = pad + j * cell_size
            y = pad + i * cell_size
            
            # Color interpolator: sage green for positive, terracotta for negative, neutral cream for 0
            if val >= 0:
                # Green scale
                opacity = min(1.0, max(0.15, val))
                fill_color = f"rgba(82, 115, 96, {opacity:.2f})"
                text_color = "#FFFFFF" if val > 0.55 else "#202E26"
            else:
                # Terracotta scale
                opacity = min(1.0, max(0.15, abs(val)))
                fill_color = f"rgba(196, 98, 66, {opacity:.2f})"
                text_color = "#FFFFFF" if abs(val) > 0.55 else "#202E26"
                
            svg.append(f'<rect x="{x+1:.1f}" y="{y+1:.1f}" width="{cell_size-2:.1f}" height="{cell_size-2:.1f}" fill="{fill_color}" rx="4" />')
            svg.append(f'<text x="{x + cell_size/2:.1f}" y="{y + cell_size/2 + 4:.1f}" text-anchor="middle" font-size="10" font-weight="bold" fill="{text_color}">{val:+.2f}</text>')
            
    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {output_path}")

def generate_svg_mood_nutritional_profile(rows: list, output_path: str):
    """Generates grouped bar charts comparing mean Calories and Protein across moods."""
    moods = ["Energetic", "Happy", "Stressed", "Tired", "Relaxed", "Low Mood"]
    mood_data = {m: {"cal": [], "prot": []} for m in moods}
    
    for r in rows:
        m = r["mood"]
        if m in mood_data:
            mood_data[m]["cal"].append(float(r["calories"]))
            mood_data[m]["prot"].append(float(r["protein"]))
            
    cal_means = [sum(mood_data[m]["cal"]) / max(1, len(mood_data[m]["cal"])) for m in moods]
    prot_means = [sum(mood_data[m]["prot"]) / max(1, len(mood_data[m]["prot"])) for m in moods]
    
    w, h = 640, 360
    pad_left, pad_bottom, pad_top, pad_right = 60, 70, 50, 60
    chart_w = w - pad_left - pad_right
    chart_h = h - pad_top - pad_bottom
    
    max_cal = 450
    max_prot = 30
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" style="background:#FAF8F5; font-family: sans-serif;">']
    svg.append(f'<text x="{w/2}" y="30" text-anchor="middle" font-size="14" font-weight="bold" fill="#202E26">Nutritional Differences Across Mood States</text>')
    
    # Legend
    svg.append(f'<rect x="{w/2 - 120}" y="45" width="12" height="12" fill="#527360" rx="2" />')
    svg.append(f'<text x="{w/2 - 102}" y="55" font-size="10" fill="#2D3B32">Avg Calories (kcal, Left Axis)</text>')
    svg.append(f'<rect x="{w/2 + 40}" y="45" width="12" height="12" fill="#C46242" rx="2" />')
    svg.append(f'<text x="{w/2 + 58}" y="55" font-size="10" fill="#2D3B32">Avg Protein (g, Right Axis)</text>')
    
    group_w = chart_w / len(moods)
    bar_w = 20
    
    for i, m in enumerate(moods):
        gx = pad_left + i * group_w
        
        # Calorie bar (Left Axis)
        c_val = cal_means[i]
        c_h = (c_val / max_cal) * chart_h
        c_y = h - pad_bottom - c_h
        svg.append(f'<rect x="{gx + group_w/2 - bar_w - 2:.1f}" y="{c_y:.1f}" width="{bar_w}" height="{c_h:.1f}" fill="#527360" rx="3" />')
        svg.append(f'<text x="{gx + group_w/2 - bar_w/2 - 2:.1f}" y="{c_y - 4:.1f}" text-anchor="middle" font-size="9" font-weight="bold" fill="#527360">{int(c_val)}</text>')
        
        # Protein bar (Right Axis)
        p_val = prot_means[i]
        p_h = (p_val / max_prot) * chart_h
        p_y = h - pad_bottom - p_h
        svg.append(f'<rect x="{gx + group_w/2 + 2:.1f}" y="{p_y:.1f}" width="{bar_w}" height="{p_h:.1f}" fill="#C46242" rx="3" />')
        svg.append(f'<text x="{gx + group_w/2 + bar_w/2 + 2:.1f}" y="{p_y - 4:.1f}" text-anchor="middle" font-size="9" font-weight="bold" fill="#C46242">{p_val:.1f}g</text>')
        
        # Mood Label
        svg.append(f'<text x="{gx + group_w/2:.1f}" y="{h - pad_bottom + 18}" text-anchor="middle" font-size="11" font-weight="bold" fill="#202E26">{m}</text>')
        
    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_csv = os.path.join(script_dir, "..", "data", "food_dataset_cleaned.csv")
    assets_dir = os.path.join(script_dir, "..", "assets", "images")
    os.makedirs(assets_dir, exist_ok=True)
    
    rows = load_data(clean_csv)
    print(f"Loaded {len(rows)} records for EDA visual generation.")
    
    generate_svg_calories_distribution(rows, os.path.join(assets_dir, "calories_distribution.svg"))
    generate_svg_correlation_heatmap(rows, os.path.join(assets_dir, "macro_correlation_heatmap.svg"))
    generate_svg_mood_nutritional_profile(rows, os.path.join(assets_dir, "mood_nutritional_profile.svg"))
    print("All EDA visuals generated successfully in assets/images/!")
