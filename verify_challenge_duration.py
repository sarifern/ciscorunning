"""
Calculate the actual challenge duration based on DATE_START and DATE_END
"""
from datetime import datetime

DATE_START = datetime(2026, 12, 11, 0, 0, 0)
DATE_END = datetime(2027, 1, 7, 0, 0, 0)

days_diff = (DATE_END.date() - DATE_START.date()).days

print("=" * 100)
print("CHALLENGE DURATION")
print("=" * 100)
print(f"Start: {DATE_START.date()} (Dec 11, 2026)")
print(f"End:   {DATE_END.date()} (Jan 7, 2027)")
print(f"\nDuration: {days_diff} days")
print("\nDays breakdown:")
print("  December 2026: 21 days (Dec 11-31)")
print("  January 2027:   7 days (Jan 1-7)")
print("  Total:         28 days")
print("\n✅ Challenge allows workouts for 28 days, not 27!")
