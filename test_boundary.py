"""Test script to verify REBIO boundary loading."""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the boundary loading function
from cs_map import load_rebio_boundary, get_rebio_boundary

print("=" * 60)
print("Testing REBIO Boundary Loading")
print("=" * 60)

# Test loading
coords = load_rebio_boundary()

if coords:
    print("\n✓ Boundary loaded successfully!")
    print(f"  Total coordinates: {len(coords)}")
    
    # Extract lat/lon ranges
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    
    print(f"\n  Longitude range: {min(lons):.6f} to {max(lons):.6f}")
    print(f"  Latitude range:  {min(lats):.6f} to {max(lats):.6f}")
    
    print(f"\n  First 5 coordinates:")
    for i, coord in enumerate(coords[:5]):
        print(f"    {i+1}. Lon: {coord[0]:.6f}, Lat: {coord[1]:.6f}")
    
    print(f"\n  Last 5 coordinates:")
    for i, coord in enumerate(coords[-5:]):
        print(f"    {len(coords)-4+i}. Lon: {coord[0]:.6f}, Lat: {coord[1]:.6f}")
        
    # Check if coordinates are in expected Brazil region
    expected_lon_range = (-48.5, -48.3)
    expected_lat_range = (-27.3, -27.2)
    
    print("\n  Validation:")
    lon_ok = expected_lon_range[0] <= min(lons) and max(lons) <= expected_lon_range[1]
    lat_ok = expected_lat_range[0] <= min(lats) and max(lats) <= expected_lat_range[1]
    
    if lon_ok and lat_ok:
        print("  ✓ Coordinates are in expected REBIO Arvoredo region")
    else:
        print("  ⚠ Coordinates may be outside expected region:")
        print(f"    Expected lon: {expected_lon_range}")
        print(f"    Expected lat: {expected_lat_range}")
else:
    print("\n✗ Failed to load boundary!")

print("\n" + "=" * 60)
