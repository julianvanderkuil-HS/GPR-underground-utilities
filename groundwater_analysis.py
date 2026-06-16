"""
BRO Groundwater Level Analysis
================================
Analyses daily groundwater levels from BRO station GLD000000027712
for the survey period. Uses 2025 data as proxy since 2026 data
was unavailable for the April-May period.

Data source: BRO (Basisregistratie Ondergrond)

Usage:
    python groundwater_analysis.py <groundwater_data.csv>

Author: Julian van der Kuil - BEP TU Delft
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse


def load_groundwater_data(filepath):
    """Load groundwater level data from BRO CSV export."""
    rows = []
    with open(filepath, 'r') as f:
        in_data = False
        for line in f:
            line = line.strip()
            if 'tijdstip meting' in line:
                in_data = True
                continue
            if in_data and line and not line.startswith('"observatie'):
                parts = [p.strip().strip('"') for p in line.split(',')]
                if len(parts) >= 2 and parts[0] and parts[1]:
                    try:
                        dt = pd.to_datetime(
                            parts[0], utc=True).tz_localize(None)
                        level = float(parts[1])
                        rows.append({'datetime': dt, 'level_m': level})
                    except (ValueError, IndexError):
                        pass

    df = pd.DataFrame(rows)
    df = df.sort_values('datetime').reset_index(drop=True)
    print(f"Loaded {len(df)} records: "
          f"{df['datetime'].min().date()} to {df['datetime'].max().date()}")
    print(f"Water level range: "
          f"{df['level_m'].min():.3f} to {df['level_m'].max():.3f} m NAP")
    return df


def plot_groundwater(df, output_file='groundwater_level_2025.png'):
    """Plot groundwater levels for 2025 with survey date equivalents."""

    # Daily averages for 2025
    df_2025 = df[(df['datetime'] >= '2025-01-01') &
                 (df['datetime'] <= '2025-12-31')].copy()
    df_2025_daily = df_2025.set_index('datetime').resample(
        'D')['level_m'].mean().reset_index()

    # April-May 2025
    df_apr_may = df_2025_daily[
        (df_2025_daily['datetime'] >= '2025-04-01') &
        (df_2025_daily['datetime'] <= '2025-05-31')]

    # Survey equivalent dates
    s1 = df_2025_daily[df_2025_daily['datetime'].dt.date ==
                        pd.Timestamp('2025-04-30').date()]
    s2 = df_2025_daily[df_2025_daily['datetime'].dt.date ==
                        pd.Timestamp('2025-05-22').date()]

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Top: full 2025
    ax1.plot(df_2025_daily['datetime'], df_2025_daily['level_m'],
             color='#1C7293', linewidth=1.2)
    ax1.fill_between(df_2025_daily['datetime'],
                     df_2025_daily['level_m'],
                     df_2025_daily['level_m'].min(),
                     alpha=0.2, color='#1C7293')
    ax1.set_ylabel('Water level (m NAP)', fontsize=11)
    ax1.set_title('Groundwater Level - BRO Station GLD000000027712\n'
                  'Full year 2025', fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.axvspan(pd.Timestamp('2025-04-01'), pd.Timestamp('2025-05-31'),
                alpha=0.15, color='#E74C3C', label='Apr-May period')
    ax1.legend(fontsize=9)

    # Bottom: April-May zoomed
    ax2.plot(df_apr_may['datetime'], df_apr_may['level_m'],
             color='#1C7293', linewidth=2, marker='o', markersize=3)
    ax2.fill_between(df_apr_may['datetime'], df_apr_may['level_m'],
                     df_apr_may['level_m'].min() - 0.02,
                     alpha=0.2, color='#1C7293')

    ax2.axvline(pd.Timestamp('2025-04-30'), color='#02C39A',
                linewidth=2.5, linestyle='--',
                label='Equiv. Survey 1 (30 Apr)')
    ax2.axvline(pd.Timestamp('2025-05-22'), color='#E74C3C',
                linewidth=2.5, linestyle='--',
                label='Equiv. Survey 2 (22 May)')
    ax2.axvspan(pd.Timestamp('2025-04-30'), pd.Timestamp('2025-05-22'),
                alpha=0.08, color='#1C7293',
                label='Period between surveys')

    ax2.set_ylabel('Water level (m NAP)', fontsize=11)
    ax2.set_xlabel('Date', fontsize=11)
    ax2.set_title('Groundwater Level - April-May 2025 '
                  '(nearest available to survey period)', fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax2.legend(fontsize=9)
    plt.xticks(rotation=45)

    # Annotate survey date levels
    if len(s1) > 0:
        ax2.annotate(f"{s1['level_m'].values[0]:.3f} m NAP",
                     xy=(pd.Timestamp('2025-04-30'),
                         s1['level_m'].values[0]),
                     xytext=(10, 10), textcoords='offset points',
                     fontsize=9, color='#02C39A')
    if len(s2) > 0:
        ax2.annotate(f"{s2['level_m'].values[0]:.3f} m NAP",
                     xy=(pd.Timestamp('2025-05-22'),
                         s2['level_m'].values[0]),
                     xytext=(10, -20), textcoords='offset points',
                     fontsize=9, color='#E74C3C')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='BRO groundwater level analysis')
    parser.add_argument('filename',
                        help='Path to BRO groundwater CSV file')
    parser.add_argument('--output', type=str,
                        default='groundwater_level_2025.png')
    args = parser.parse_args()

    df = load_groundwater_data(args.filename)
    plot_groundwater(df, args.output)
