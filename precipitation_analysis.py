"""
KNMI Precipitation Data Analysis
==================================
Analyses daily precipitation from KNMI Rotterdam Airport (STN 344)
for the period between the dry (30 April) and wet (22 May) surveys.

Data source: KNMI (2026). Daily weather data - Rotterdam Airport.
             https://www.knmi.nl/nederland-nu/klimatologie/daggegevens

Usage:
    python precipitation_analysis.py <knmi_data_file.txt>

Author: Julian van der Kuil - BEP TU Delft
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse


def load_knmi_data(filepath):
    """Load daily precipitation from KNMI etmgeg file."""
    rows = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('344'):
                parts = [p.strip() for p in line.split(',')]
                try:
                    date = pd.to_datetime(parts[1], format='%Y%m%d')
                    rh = parts[21].strip()
                    rh = 0 if rh == '' or rh == '-1' else float(rh)
                    rh_mm = max(0, rh / 10.0)  # convert 0.1mm to mm
                    rows.append({'date': date, 'RH_mm': rh_mm})
                except (ValueError, IndexError):
                    pass

    df = pd.DataFrame(rows)
    print(f"Loaded {len(df)} records: "
          f"{df['date'].min().date()} to {df['date'].max().date()}")
    return df


def plot_precipitation(df, output_file='precipitation_april_may_2026.png'):
    """Plot daily precipitation for April-May 2026."""

    df_period = df[(df['date'] >= '2026-04-01') &
                   (df['date'] <= '2026-05-31')].copy()

    survey1 = pd.Timestamp('2026-04-30')
    survey2 = pd.Timestamp('2026-05-22')
    total_between = df[(df['date'] >= survey1) &
                       (df['date'] <= survey2)]['RH_mm'].sum()

    fig, ax = plt.subplots(figsize=(12, 5))

    colors = ['#1C7293' if survey1 <= d <= survey2 else '#B0C4D8'
              for d in df_period['date']]
    ax.bar(df_period['date'], df_period['RH_mm'],
           color=colors, width=0.8, alpha=0.9)

    ax.axvline(survey1, color='#02C39A', linewidth=2.5,
               linestyle='--', label='Survey 1 - Dry (30 April 2026)')
    ax.axvline(survey2, color='#E74C3C', linewidth=2.5,
               linestyle='--', label='Survey 2 - Wet (22 May 2026)')
    ax.axvspan(survey1, survey2, alpha=0.08, color='#1C7293',
               label='Period between surveys')

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Precipitation (mm)', fontsize=12)
    ax.set_title('Daily Precipitation - KNMI Weather Station '
                 'Rotterdam Airport (STN 344)\nApril-May 2026',
                 fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)

    ax.text(0.5, 0.92,
            f'Total precipitation between surveys: {total_between:.1f} mm',
            transform=ax.transAxes, ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='#E8F4F8',
                      edgecolor='#1C7293'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    print(f"Total precipitation between surveys: {total_between:.1f} mm")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='KNMI precipitation analysis')
    parser.add_argument('filename', help='Path to KNMI etmgeg data file')
    parser.add_argument('--output', type=str,
                        default='precipitation_april_may_2026.png')
    args = parser.parse_args()

    df = load_knmi_data(args.filename)
    plot_precipitation(df, args.output)
