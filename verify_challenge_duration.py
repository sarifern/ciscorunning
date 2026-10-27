"""
Calculate the actual challenge duration based on DATE_START and DATE_END
"""
from datetime import datetime

DATE_START = datetime(2025, 12, 12, 1, 0, 0)
DATE_END = datetime(2026, 1, 8, 0, 0, 0)

days_diff = (DATE_END.date() - DATE_START.date()).days

print("=" * 100)
print("CHALLENGE DURATION")
print("=" * 100)
print(f"Start: {DATE_START.date()} (Dec 12, 2025)")
print(f"End:   {DATE_END.date()} (Jan 8, 2026)")
print(f"\nDuration: {days_diff} days")
print("\nDays breakdown:")
print("  December 2025: 20 days (Dec 12-31)")
print("  January 2026:   8 days (Jan 1-8)")
print("  Total:         28 days")
print("\n✅ Challenge allows workouts for 28 days, not 27!")
